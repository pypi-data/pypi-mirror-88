import dataclasses
import typing as t
from abc import ABC, abstractmethod
from collections import defaultdict

import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from transformers import DistilBertTokenizerFast

from bavard.dialogue_policy import constants


class LabelBinarizer:
    """
    Version of `sklearn.preprocessing.LabelBinarizer that allows
    being fit to 0 classes, and also always has as many columns
    as there are classes. Also, can handle `None` values in the
    `transform` step.
    """

    def __init__(self, **kwargs) -> None:
        self._encoder = LabelEncoder(**kwargs)
        self._fitted = False

    def fit(self, y: t.List) -> None:
        self._encoder.fit(y)
        self._fitted = True

    def transform(self, y: t.List) -> np.ndarray:
        assert self._fitted

        if len(y) == 0:
            return np.zeros((len(y), self.n_classes), np.int32)

        # Only encode the non-null values; leave the nulls as an
        # all zeros encoding.
        non_nulls = []
        non_nulls_i = []
        for i, label in enumerate(y):
            if label is not None:
                non_nulls.append(label)
                non_nulls_i.append(i)

        col_indices = self._encoder.transform(non_nulls).astype(np.int32)
        one_hot = np.zeros((len(y), self.n_classes), np.int32)
        one_hot[non_nulls_i, col_indices] = 1
        return one_hot

    def inverse_transform(self, y: np.ndarray) -> list:
        assert self._fitted
        if not isinstance(y, np.ndarray):
            y = np.array(y)
        if y.size == 0:
            return []
        indices = np.argmax(y, axis=1)
        return self._encoder.inverse_transform(indices)

    @property
    def classes_(self) -> np.ndarray:
        assert self._fitted
        return self._encoder.classes_

    @property
    def n_classes(self) -> int:
        assert self._fitted
        return len(self._encoder.classes_)


class TextEncoder:
    """Converts text into a tokenization.
    """
    def __init__(self):
        self._tokenizer = DistilBertTokenizerFast.from_pretrained(constants.BASE_LANGUAGE_MODEL)

    def fit(self, y: t.Sequence) -> None:
        pass

    def transform(self, text: str) -> t.Dict[str, np.ndarray]:
        if text is None:
            text = ''
        encoding = self._tokenizer(
            text,
            return_tensors="np",
            return_attention_mask=True,
            truncation=True,
            max_length=constants.MAX_UTTERANCE_LEN,
            padding="max_length"
        )
        return {
            "input_ids": encoding.input_ids,
            "input_mask": encoding.attention_mask
        }

    def inverse_transform(self, y: np.ndarray) -> str:
        return self._tokenizer.batch_decode(y)

    @property
    def classes_(self) -> np.ndarray:
        return np.array(list(self._tokenizer.get_vocab().keys()))


Encoder = t.Union[LabelEncoder, LabelBinarizer, MultiLabelBinarizer, TextEncoder]


class EncodingContext:

    def __init__(
        self,
        **encoder_map: Encoder
    ) -> None:
        self._encoder_map = encoder_map

    def get_size(self, encoder_name: str) -> int:
        """Gets the cardinality of an encoder.
        """
        assert encoder_name in self._encoder_map
        return len(self._encoder_map[encoder_name].classes_)

    def fit(self, **data_map: t.Sequence) -> None:
        """Fit on one or more field encoders.
        """
        for encoder_name, data in data_map.items():
            assert encoder_name in self._encoder_map
            self._encoder_map[encoder_name].fit(data)

    def transform(self, encoder_name: str, data: t.Sequence) -> np.ndarray:
        assert encoder_name in self._encoder_map
        return self._encoder_map[encoder_name].transform(data)

    def inverse_transform(self, encoder_name: str, data: np.ndarray) -> t.Sequence:
        assert encoder_name in self._encoder_map
        return self._encoder_map[encoder_name].inverse_transform(data)

    def classes_(self, encoder_name: str) -> t.Sequence:
        assert encoder_name in self._encoder_map
        return self._encoder_map[encoder_name].classes_


@dataclasses.dataclass
class Encodable(ABC):
    """
    Base class for classes that can be encoded into a numpy array. Provides default
    functionality for null numpy encoding.
    """

    @abstractmethod
    def encode(self, enc_context: EncodingContext) \
            -> t.Union[np.ndarray, t.Dict[str, np.ndarray]]:
        """Encodes the class instance into a numpy array representation.
        """
        pass

    @classmethod
    def encode_null(cls, enc_context: EncodingContext) -> t.Union[np.ndarray, t.Dict[str, np.ndarray]]:
        """Returns a null encoding that matches the encoding shape of this class, given an encoding context.
        """
        shape = cls.get_encoding_shape(enc_context)
        if isinstance(shape, tuple):
            return np.zeros(shape)
        elif isinstance(shape, dict):
            return {k: np.zeros(v) for k, v in shape.items()}
        else:
            raise ValueError(f"uknown encoding shape datatype {type(shape)}")

    @staticmethod
    @abstractmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Union[t.Sequence[int], t.Dict[str, t.Sequence[int]]]:
        """Returns the shape of an encoding of this class, given an encoding context.
        """
        pass


def concat_ndarray_dicts(
    dicts: t.Sequence[t.Dict[str, np.ndarray]], axis: int = 0, new_axis: bool = False
) -> t.Dict[str, np.ndarray]:
    """
    Concatenates all the ndarrays in `dicts` by dictionary key.
    """
    # Unpack each dictionary of tensors into a single dictionary
    # containing lists of tensors.
    data = defaultdict(list)
    for d in dicts:
        for key in d:
            if d[key] is None:
                continue
            data[key].append(d[key])

    # Now convert those lists to tensors
    result = {}
    for key in data:
        if new_axis:
            result[key] = np.stack(data[key])
        else:
            result[key] = np.concatenate(data[key], axis)

    return result
