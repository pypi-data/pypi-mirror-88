from unittest import TestCase

from fastapi.encoders import jsonable_encoder

from bavard.dialogue_policy.data.conversations.actions import UserAction, AgentAction, Tag
from test.functional.dialogue_policy.utils import DummyContext, check_agent_action_feature_vec


class TestActions(TestCase):

    def setUp(self):
        self.ctx = DummyContext()

    def test_user_action_serialization(self):
        user_action = UserAction(
            intent="intent1", utterance="I am uttering.", tags=[Tag(tagType="tagtype1", value="tagvalue")]
        )
        self.assertEqual(user_action, UserAction.parse_obj(jsonable_encoder(user_action)))

    def test_user_action_encoding(self):
        user_action = UserAction(
            intent="intent1",
            utterance="I am uttering.",
            tags=[Tag(tagType="tagtype1", value="tagvalue"), Tag(tagType="tagtype3", value="othervalue")]
        )
        encoding = user_action.encode(enc_context=self.ctx.enc_context)
        # Shape should be correct
        self.assertEqual(encoding['feature_vec'].shape,
                         (1, len(self.ctx.intents)
                          + len(self.ctx.tag_types)))
        # Content should be correct
        enc_intent = encoding["feature_vec"][:, :len(self.ctx.intents)]
        self.assertEqual(self.ctx.enc_context.inverse_transform("intent", enc_intent)[0], "intent1")
        tags_enc = encoding["feature_vec"][:, -len(self.ctx.tag_types):]
        self.assertEqual(self.ctx.enc_context.inverse_transform("tags", tags_enc)[0], ("tagtype1", "tagtype3"))

    def test_agent_action_serialization(self):
        agent_action = AgentAction(name="action2", utterance="I am uttering also.")
        self.assertEqual(agent_action, AgentAction.parse_obj(jsonable_encoder(agent_action)))

    def test_agent_action_encoding(self):
        agent_action = AgentAction(name="action2", utterance="I am uttering also.")
        encoding = agent_action.encode(enc_context=self.ctx.enc_context)
        check_agent_action_feature_vec(encoding, self.ctx, action="action2")
