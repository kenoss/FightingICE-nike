# FightingICE-nike

AI agent for FightingICE

## DISCLAIMER

- Some contents of repo is based on https://github.com/TeamFightingICE/FightingICE and competition code of UT spring seminor.  I do not guarantee quality of those code.
- This repo is abundand.  The original author will not maintain this.


## Initialization

This repository depends on simulator.

```
git submodule update --init --recursive
```

Scripts in this repository uses some environment variables.
If you want to execute them from CLI, use [direnv](https://github.com/direnv/direnv).

```
direnv allow
```

You must ensure that `java` is installed in the environment.


## How to start battles

```
python sample/battle.py
```

This command do

- launch python
- launch simultaor through `script/launch_simulator.sh`
- load agents from `team/ut-dl-basics-2019-spring/d4`

and then play battles.


## fice_nike format of the FightingICE

This is a very rough proposal of format of competition.

Anyone fork this repository and have your competition using forked format.

### How to entry

1. Make your Github repository
2. Send PR to the competition repository that include your repo as submodule in path like `team/ut-dl-basics-2019-spring/d4`. (FORMAT: `team/<competition-name>/<team-name>`)
3. Rewrite `script/launch_simulator.sh` to use your agent, and write your own agent.
4. Update your repo and send PR (code freezing).
