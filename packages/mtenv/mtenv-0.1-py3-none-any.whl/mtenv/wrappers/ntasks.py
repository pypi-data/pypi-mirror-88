from gym.spaces import Discrete
from gym.utils import seeding

from mtenv import MTEnv


class NTasks(MTEnv):
    """
    A wrapper to fix the number of different tasks to n_tasks. Each task is sampled in the fixed set of n_tasks.
    """

    def __init__(self, mtenv, n_tasks):
        self.mtenv = mtenv
        self.n_tasks = n_tasks
        self.tasks = None
        super().__init__(
            self.mtenv.action_space,
            self.mtenv.observation_space["env_obs"],
            self.mtenv.observation_space["task_obs"],
        )

    def step(self, action):
        o, r, d, i = self.mtenv.step(action)
        return o, r, d, i

    def reset(self, **args):
        o = self.mtenv.reset()
        return o

    def get_task_obs(self):
        return self.mtenv.get_task_obs()

    def get_task_state(self):
        return self.mtenv.get_task_state()

    def set_task_state(self, task_state):
        self.mtenv.set_task_state(task_state)

    def sample_task_state(self):
        if self.tasks is None:
            self.tasks = []
            for k in range(self.n_tasks):
                ts = self.mtenv.sample_task_state()
                self.tasks.append(ts)

        id_task = self.np_random_task.randint(self.n_tasks)
        return self.tasks[id_task]

    def seed(self, env_seed):
        self.mtenv.seed(env_seed)

    def seed_task(self, seed):
        self.mtenv.seed_task(seed)
        self.np_random_task, seed = seeding.np_random(seed)


if __name__ == "__main__":
    from mtenv.envs.control import MTCartPole

    env = MTCartPole()
    env = NTasks(env, n_tasks=5)
    env.seed(5)
    env.seed_task(15)
    for k in range(10):
        print("======")
        env.reset_task_state()
        obs = env.reset()
        print(obs)
        for kk in range(3):
            print(env.step(0))
