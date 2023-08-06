from unittest import TestCase

from fastapi.encoders import jsonable_encoder

from bavard.dialogue_policy.data.conversations.dialogue_turns import (
    UserDialogueTurn, AgentDialogueTurn, DialogueState, SlotValue
)
from bavard.dialogue_policy.data.conversations.actions import UserAction, AgentAction, Tag
from test.functional.dialogue_policy.utils import (
    DummyContext, check_user_dialogue_turn_feature_vec, check_agent_action_feature_vec
)


class TestDialogueTurns(TestCase):

    def setUp(self):
        self.ctx = DummyContext()

    def test_user_dialogue_turn_serialization(self):
        turn = UserDialogueTurn(
            state=DialogueState(
                slotValues=[SlotValue(name="slot3", value="foo"), SlotValue(name="slot1", value="bar")]
            ),
            userAction=UserAction(
                intent="intent2", utterance="I utter.", tags=[Tag(tagType="tagtype1", value="value1")]
            )
        )
        self.assertEqual(turn, UserDialogueTurn.parse_obj(jsonable_encoder(turn)))

    def test_user_dialogue_turn_encoding(self):
        turn = UserDialogueTurn.parse_obj({
            "actor": "USER",
            "userAction": {
                "intent": "intent2",
                "utterance": "This too is an utterance.",
                "tags": [{"tagType": "tagtype1", "value": "value1"}]
            },
            "state": {
                "slotValues": [
                    {"name": "slot3", "value": "foo"},
                    {"name": "slot1", "value": "bar"}
                ]
            }
        })
        encoding = turn.encode(self.ctx.enc_context)

        check_user_dialogue_turn_feature_vec(
            encoding["feature_vec"], self.ctx, slots=("slot1", "slot3"), intent="intent2", tag_types=("tagtype1",)
        )

    def test_agent_dialogue_turn_serialization(self):
        turn = AgentDialogueTurn(
            state=DialogueState(slotValues=[SlotValue(name="slot2", value="foo")]),
            agentAction=AgentAction(name="action2", utterance="I utter also.")
        )
        self.assertEqual(turn, AgentDialogueTurn.parse_obj(jsonable_encoder(turn)))

    def test_agent_dialogue_turn_encoding(self):
        turn = AgentDialogueTurn.parse_obj({
            "actor": "AGENT",
            "agentAction": {
                "name": "action3",
                "utterance": "This too is an utterance."
            },
            "state": {
                "slotValues": [
                    {"name": "slot2", "value": "foo"},
                    {"name": "slot3", "value": "bar"}
                ]
            }
        })
        encoding = turn.encode(self.ctx.enc_context)
        check_agent_action_feature_vec(encoding, self.ctx, action="action3")

    def test_can_handle_no_state(self):
        user_turn = UserDialogueTurn.parse_obj(
            {
                "userAction": {
                    "type": "UTTERANCE_ACTION",
                    "utterance": "Ok thank you, that's great to know. What are your prices like? Are they competitive?",
                    "intent": "ask_pricing",
                    "tags": []
                },
                "actor": "USER"
            }
        )
        self.assertEqual(user_turn.state, None)

    def test_can_handle_no_intent(self):
        user_turn = UserDialogueTurn.parse_obj({
            "actor": "USER",
            "userAction": {
                "type": "UTTERANCE_ACTION",
                "utterance": "What are your prices like?",
                "tags": []
            },
            "timestamp": 1607471164994
        })
        self.assertEqual(user_turn.userAction.intent, None)
