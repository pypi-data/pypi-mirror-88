# MTEnv

## Documentation

### How to add new environments

There are two workflows:

* The user have a standard gym environment, which they want to convert into a multitask environment. E.g.: `examples/bandit.py` has a `BanditEnv` which is a standard multi-arm bandit, without any explicit notion of task. The user has the following options:

    * Write a new subclass, say MTBanditEnv (which subclasses MTEnv) as shown in `examples/mtenv_bandit.py`.

    * Use the `MTEnvWrapper` and wrap the existing standard model class. An example is shown in `examples/wrapped_bandit.py`. 

* If the user does not have a standard gym environment to start with, it is recommended that they directly extend the MTEnv class.

### Running examples

* `pip install -r requirements.txt`
* Alternatively, feel free to use my conda env: `source activate source /private/home/sodhani/.conda/envs/mtenv/bin/activate /private/home/sodhani/.conda/envs/mtenv` 
* In the root folder, run `PYTHONPATH=. python examples/<filename>.py`.

## Pending items

1. [Google Doc](https://docs.google.com/document/d/1H98fJ-gI53kF1x99pt-7Gy_HPAE6q9DeLPeT3kBIThQ/edit) to track some ongoing work.