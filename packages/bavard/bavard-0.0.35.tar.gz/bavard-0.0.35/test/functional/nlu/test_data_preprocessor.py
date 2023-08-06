from unittest import TestCase
import typing as t

from bavard.nlu.data_preprocessing.nlu_data import NLUDataPreprocessor
from bavard.nlu.data_preprocessing.training_example import Example
from test.utils import load_json_file


class TestDataPreprocessor(TestCase):
    def setUp(self):
        super().setUp()
        self.max_seq_len = 120
        self.nlu_data = load_json_file("test/data/agents/test-agent.json")["nluData"]

    def test_preprocess_text(self) -> None:
        preprocessor = NLUDataPreprocessor(max_seq_len=self.max_seq_len)
        preprocessor.fit(self.nlu_data)
        text_tokens, word_start_mask, word_to_token_map = preprocessor._preprocess_text(
            "What is the cheapest flight?"
        )
        self.assertEqual(
            text_tokens, ["what", "is", "the", "che", "##ap", "##est", "flight", "?"]
        )
        self.assertEqual(word_start_mask, [1, 1, 1, 1, 0, 0, 1, 0])
        self.assertEqual(word_to_token_map, [0, 1, 2, 3, 6])

    def test_preprocess(self) -> None:
        example, _ = self._get_test_example()
        # Check that the tags were identified and aligned correctly.
        self.assertEqual(
            example.token_tags,
            [
                "[CLS]",
                "O",
                "O",
                "O",
                "B-flight_stop",
                "O",
                "O",
                "O",
                "B-fromloc.city_name",
                "I-fromloc.city_name",
                "I-fromloc.city_name",
                "O",
                "B-toloc.city_name",
                "I-toloc.city_name",
                "I-toloc.city_name",
                "O",
                "[SEP]",
            ],
        )
        # Check that the tokens are represented correctly.
        self.assertEqual(
            example.tokens,
            [
                "[CLS]",
                "are",
                "they",
                "all",
                "non",
                "##stop",
                "flights",
                "from",
                "kans",
                "##as",
                "city",
                "to",
                "st",
                ".",
                "pau",
                "##l",
                "[SEP]",
            ],
        )

    def test_to_tensor(self) -> None:
        example, preprocessor = self._get_test_example()
        tensor_dict = example.to_tensors(
            self.max_seq_len,
            preprocessor.tag_encoder,
            preprocessor.intents_encoder,
        )

        # Check that the example was turned into tensors of the correct
        # shapes.
        expected_shapes = {
            "input_ids": (self.max_seq_len,),
            "input_mask": (self.max_seq_len,),
            "word_start_mask": (self.max_seq_len,),
            "intent": (len(preprocessor.intents_encoder.classes_),),
            "tags": (self.max_seq_len, len(preprocessor.tag_encoder.classes_)),
        }
        for key, expected_shape in expected_shapes.items():
            self.assertEqual(tensor_dict[key].numpy().shape, expected_shape)

    def test_excludes_examples_with_unknown_labels(self):
        preprocessor = NLUDataPreprocessor(max_seq_len=self.max_seq_len)
        messy_nlu_data = load_json_file("test/data/agents/invalid-nlu-examples.json")["nluData"]
        preprocessor.fit(messy_nlu_data)
        examples = preprocessor._process_nlu_data(messy_nlu_data)

        # Invalid examples should be filtered out.
        self.assertEqual(len(examples), 2)
        for ex in examples:
            self.assertIn(ex.intent, preprocessor.intents)
            for tag in ex.tags:
                self.assertIn(tag.tag_type, preprocessor.tag_types)


    def _get_test_example(self) -> t.Tuple[Example, NLUDataPreprocessor]:
        preprocessor = NLUDataPreprocessor(max_seq_len=self.max_seq_len)
        preprocessor.fit(self.nlu_data)
        examples = preprocessor._process_nlu_data(self.nlu_data)
        return examples[1], preprocessor
