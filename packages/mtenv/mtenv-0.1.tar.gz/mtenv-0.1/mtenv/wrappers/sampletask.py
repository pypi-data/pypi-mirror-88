from typing import Any, Dict, List, Optional

from mtenv.core import MTEnv
from mtenv.utils.types import ActionType, EnvObsType, StepReturnType, TaskStateType


class SampleTask(MTEnv):
    """
    A wrapper that samples a new task at each env.reset() call
    """

    def __init__(self, env: MTEnv):
        self.env = env
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space

    def reset(self) -> EnvObsType:
        self.env.reset_task_state()
        return self.env.reset()

    def step(self, action: ActionType) -> StepReturnType:
        return self.env.step(action)

    def set_task_state(self, task_state: TaskStateType) -> None:
        self.env.set_task_state(task_state)

    def get_task_state(self) -> TaskStateType:
        return self.env.get_task_state()

    def reset_task_state(self) -> None:
        self.env.reset_task_state()

    def sample_task_state(self) -> TaskStateType:
        return self.env.sample_task_state()

    def seed(self, seed: Optional[int] = None) -> List[int]:
        return self.env.seed(seed)

    def seed_task(self, seed: Optional[int] = None) -> List[int]:
        return self.env.seed_task(seed)
