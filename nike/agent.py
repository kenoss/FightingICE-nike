import sys
import pathlib
# sys.path.append(pathlib.Path(__file__).resolve().parents[1].as_posix())
# sys.path.append((pathlib.Path(__file__).resolve().parents[1] / 'submodule/FightingICE/python').as_posix())

import numpy as np


# from nike.contest_modified.utils import Environment, Agent
from utils import Agent


class PartialPolicy:
    def __init__(self, state):
        self._orig_state = state

    def policy(self, state):
        raise NotImplementedError()


class PartialPolicyManager:
    def __init__(self, config):
        self._config = config
        self._curr = config['init'](None)
        self._transit_map = self._make_transit_map(config['transit'])
        print(self._transit_map)

    def _make_transit_map(self, transit):
        def make_one(xs):
            dests = [x['dest'] for x in xs]
            weights = np.array([x['weight'] for x in xs])
            assert 1.0 - np.sum(weights) < 1e-5, f"{np.sum(weights)} shuld be equal to 1.0"
            return {
                'dests': dests,
                'weights': weights,
            }

        return dict((k, make_one(v)) for (k, v) in transit.items())

    def get_policy_and_update(self, state):
        res, transit = self._curr.policy(state)
        print(res, transit)

        if transit:
            info = self._transit_map[self._curr.__class__]
            i = np.random.choice(len(info['weights']), p=info['weights'])
            self._curr = info['dests'][i](state)

        return res


class PPOneAction(PartialPolicy):
    def policy(self, state):
        return self.ACTION, True


class PPInit(PPOneAction):
    ACTION = None


class PPGuard(PPOneAction):
    ACTION = '↓'


class PPPunch(PPOneAction):
    ACTION = 'A'


class PPKick(PPOneAction):
    ACTION = 'B'


class PPC(PPOneAction):
    ACTION = 'C'


#     actions = ["↖", "↑", "↗", "←", "→", "↙", "↓", "↘", "A", "B", "C", "_"]
class PPHadoken(PPOneAction):
    ACTION = '↓↘→A'


class PPContinuousAction(PartialPolicy):
    ACTION = None
    N = None

    def __init__(self, state):
        self._n = self.N

    def policy(self, state):
        self._n -= 1
        if self._n < 0:
            return self.ACTION, True
        else:
            return self.ACTION, False


class PPMoveRight10(PPContinuousAction):
    ACTION = '→'
    N = 10


class PPMoveLeft10(PPContinuousAction):
    ACTION = '←'
    N = 10


def _random(p, pps):
    q = p / len(pps)
    return [{'weight': q, 'dest': pp} for pp in pps]


class TeamD4Agent(Agent):
    def __init__(self, environment):
        super().__init__(environment)
        self._pp_manager = PartialPolicyManager({
            'init': PPInit,
            'transit': {
                PPInit: [
                    {'weight': 1.0, 'dest': PPGuard},
                ],
                PPGuard: _random(1.0, [PPPunch, PPKick, PPC, PPHadoken, PPMoveLeft10, PPMoveRight10]),
                PPPunch: [
                    {'weight': 1.0, 'dest': PPGuard},
                ],
                PPKick: [
                    {'weight': 1.0, 'dest': PPGuard},
                ],
                PPC: [
                    {'weight': 1.0, 'dest': PPGuard},
                ],
                PPHadoken: [
                    {'weight': 1.0, 'dest': PPGuard},
                ],
                PPMoveLeft10: [
                    {'weight': 1.0, 'dest': PPGuard},
                ],
                PPMoveRight10: [
                    {'weight': 1.0, 'dest': PPGuard},
                ],
            }
        })

    def policy(self, state):
        try:
            res = self._pp_manager.get_policy_and_update(state)
        except Exception as e:
            print(e)
            raise Exception from e

        return res

    def roundEnd(self, x, y, z):
        print(x)
        print(y)
        print(z)


# def main():
#     class DummyEnv:
#         _gateway = None

#     agent = TeamD4Agent(DummyEnv())
#     state = {}
#     for _ in range(100):
#         agent.policy(state)
#     # import sys; sys.exit('========== END HERE ==========')

#     print('start')
#     env = Environment()
#     env.play(TeamD4Agent, TeamD4Agent)



# if __name__ == '__main__':
#     main()
