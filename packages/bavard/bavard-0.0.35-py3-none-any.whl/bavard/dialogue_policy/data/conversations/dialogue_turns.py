import typing as t

import numpy as np
from pydantic import BaseModel

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.conversations.actions import Actor, AgentAction, UserAction, HumanAgentAction
from bavard.dialogue_policy.data.utils import Encodable, EncodingContext


class SlotValue(BaseModel):
    name: str
    value: str


class DialogueState(BaseModel, Encodable):
    slotValues: t.List[SlotValue]

    def encode(self, enc_context: EncodingContext) -> np.ndarray:
        # Encodes the names of the slots that are filled.
        encoded_slots = enc_context.transform("slots", [[sv.name for sv in self.slotValues]])
        return encoded_slots

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Tuple[int, int]:
        return 1, enc_context.get_size("slots")


class BaseDialogueTurn(BaseModel):
    state: t.Optional[DialogueState]
    actor: Actor


class UserDialogueTurn(BaseDialogueTurn, Encodable):
    userAction: UserAction
    actor = Actor.USER

    def encode(self, enc_context: EncodingContext) -> t.Dict[str, np.ndarray]:
        encoded_state = self.state.encode(enc_context) if self.state else DialogueState.encode_null(enc_context)
        encoded_action = self.userAction.encode(enc_context=enc_context)
        feature_vec = np.concatenate([encoded_state, encoded_action['feature_vec']], axis=-1)
        return {
            'feature_vec': feature_vec,
            'utterance_ids': encoded_action['utterance_ids'],
            'utterance_mask': encoded_action['utterance_mask'],
        }

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Dict[str, t.Tuple[int, int]]:
        feature_vec_shape = (
            1, DialogueState.get_encoding_shape(enc_context)[1]
            + UserAction.get_encoding_shape(enc_context)['feature_vec'][1]
        )
        return {
            'feature_vec': feature_vec_shape,
            'utterance_ids': (1, MAX_UTTERANCE_LEN),
            'utterance_mask': (1, MAX_UTTERANCE_LEN),
        }


class AgentDialogueTurn(BaseDialogueTurn, Encodable):
    agentAction: AgentAction
    actor = Actor.AGENT

    def encode(self, enc_context: EncodingContext) -> np.ndarray:
        return self.agentAction.encode(enc_context)

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Tuple[int, int]:
        return 1, AgentAction.get_encoding_shape(enc_context)[1]


class HumanAgentDialogueTurn(BaseDialogueTurn):
    humanAgentAction = HumanAgentAction
    actor = Actor.HUMAN_AGENT
