import typing as t
from enum import Enum

import numpy as np
from pydantic import BaseModel

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.utils import Encodable, EncodingContext


class Actor(Enum):
    USER = 'USER'
    AGENT = 'AGENT'
    HUMAN_AGENT = 'HUMAN_AGENT'


class Tag(BaseModel):
    tagType: str
    value: str


class UserAction(BaseModel, Encodable):
    """Represents any type of UserAction (email, utterance, option, etc).
    """
    intent: t.Optional[str]
    utterance: t.Optional[str]
    tags: t.Optional[t.List[Tag]]

    def encode(self, enc_context: EncodingContext) -> t.Dict[str, np.ndarray]:

        # feature vec
        encoded_intent = enc_context.transform("intent", [None if self.intent == '' else self.intent])
        encoded_tags = enc_context.transform(
            "tags", [[]] if self.tags is None else [[tag.tagType for tag in self.tags]]
        )
        feature_vec = np.concatenate([encoded_intent, encoded_tags], axis=1)
        utterance_encoding = enc_context.transform("utterance", self.utterance)

        return {
            "feature_vec": feature_vec,
            "utterance_ids": utterance_encoding["input_ids"],
            "utterance_mask": utterance_encoding["input_mask"],
        }

    @classmethod
    def get_encoding_shape(cls, enc_context: EncodingContext) -> t.Dict[str, t.Tuple[int, int]]:
        return {
            "feature_vec": (1, enc_context.get_size("intent") + enc_context.get_size("tags")),
            "utterance_ids": (1, MAX_UTTERANCE_LEN),
            "utterance_mask": (1, MAX_UTTERANCE_LEN),
        }


class AgentAction(BaseModel, Encodable):
    """Represents any type of agent action (form, utterance, email, etc.)
    """
    name: str  # the action's name
    utterance: t.Optional[str]

    def encode(self, enc_context: EncodingContext):
        # TODO: include utterance encoding
        return enc_context.transform("action", [self.name])

    def encode_index(self, enc_context: EncodingContext) -> int:
        return enc_context.transform("action_index", [self.name])[0]

    @classmethod
    def get_encoding_shape(cls, enc_context: EncodingContext) -> t.Tuple[int, int]:
        return 1, enc_context.get_size("action")


class HumanAgentAction(BaseModel):
    type: str
    utterance: t.Optional[str]
