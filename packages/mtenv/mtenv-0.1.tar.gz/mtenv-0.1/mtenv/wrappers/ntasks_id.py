from typing import Any, Dict, List, Optional

from gym.spaces import Discrete
from gym.spaces.dict import Dict as DictSpace
from gym.spaces.space import Space
from gym.utils import seeding

from mtenv.core import MTEnv
from mtenv.utils.types import (
    ActionType,
    EnvObsType,
    ObsType,
    StepReturnType,
    TaskStateType,
)


class NTasksId(MTEnv):
    """
    A wrapper to fix the number of different tasks to n_tasks. Each task is sampled in the fixed set of n_tasks. The agent observes the id of the task.
    """

    def __init__(self, env: MTEnv, n_tasks: int):
        self.env = env
        self.n_tasks = n_tasks
        self.tasks: List[TaskStateType]
        super().__init__(
            self.env.action_space,
            self.env.observation_space["env_obs"],
            Discrete(n_tasks),
        )

    def step(self, action: ActionType) -> StepReturnType:
        o, r, d, i = self.env.step(action)
        o["task_obs"] = self.get_task_obs()
        return o, r, d, i

    def reset(self) -> ObsType:
        o = self.env.reset()
        return o

    def get_task_obs(self) -> TaskStateType:
        return self.task_state

    def get_task_state(self) -> TaskStateType:
        return self.task_state

    def set_task_state(self, task_state: TaskStateType) -> None:
        self.env.set_task_state(self.tasks[task_state])
        self.task_state = task_state

    def sample_task_state(self) -> TaskStateType:
        self._check_task_seed_is_set()
        if self.tasks is None:
            self.tasks = []
            for _ in range(self.n_tasks):
                ts = self.env.sample_task_state()
                self.tasks.append(ts)

        id_task = self.np_random_task.randint(self.n_tasks)
        return id_task

    def seed(self, seed: Optional[int] = None) -> List[int]:
        return self.env.seed(seed)

    def seed_task(self, seed: Optional[int] = None) -> List[int]:
        self.np_random_task, seed = seeding.np_random(seed)
        return self.env.seed_task(seed)


if __name__ == "__main__":
    from mtenv.envs.control.cartpole import MTCartPole

    env = MTCartPole()
    env = NTasksId(env, n_tasks=5)
    env.seed(5)
    env.seed_task(15)
    for k in range(10):
        print("=========")
        env.reset_task_state()
        obs = env.reset()
        print(obs)
        for kk in range(3):
            print(env.step(0))
