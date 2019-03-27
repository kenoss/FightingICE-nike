import sys
import pathlib
sys.path.append(pathlib.Path(__file__).resolve().parents[2].as_posix())
# sys.path.append((pathlib.Path(__file__).resolve().parents[2] / 'submodule/FightingICE/python').as_posix())
sys.path.append((pathlib.Path(__file__).resolve().parents[2] / 'team/ut-dl-basics-2019-spring/d4').as_posix())


from fice_nike.environment import Environment
from fice_nike.agent_base import AgentBase


from ut_dl_basics_2019_spring_team_d4.comp.policy import *


import re


def camelize_case(snake_case_string):
    return re.sub('_(.)', lambda x: x.group(1).upper(), snake_case_string)


def make_dict_of_camel_method_return(x, methods, prefix='get_'):
    return dict((k, getattr(x, camelize_case(prefix + k))()) for k in methods)




class AgentAlpha(AgentBase):
    _i = 1

    def __init__(self, *args):
        super().__init__(*args)
        self._policy = PolicyChain([
            PolicyWaitRemainingFrame(200),
            PolicyWithEnoughtEneregy(PolicySingleAction('STAND_D_DB_BB'), 50, 0.1, 1.0),
            # PolicyWithEnoughtEneregy(PolicySingleAction('B'), 10, 0.01),
            PolicyCycle([
                PolicySingleAction('A'),
                PolicySingleAction('→'),
            ]),
        ])

    def policy(self, frame_data):
        data = {
            'frame_data': frame_data,
            'player':     self.player,
        }
        return self._policy.update(data)

        # if .getCharacter(self.player).getRemainingFrame() > 0:
        #     return


        # import inspect; import os; frame = inspect.currentframe(); print(f"DEBUG: {os.path.basename(frame.f_code.co_filename)}: {frame.f_lineno}: {self.__class__.__name__}.{frame.f_code.co_name}: called {self._i}")

        # # print(state.getProjectiles())
        # # print(state.getProjectilesByP1())
        # # print(state.getProjectilesByP2())

        # # print(state.getDistanceX())
        # # print(state.getDistanceY())

        # # data = {
        # #     'distance_x': state.getDistanceX(),
        # #     'distance_y': state.getDistanceY(),
        # # }

        # chara = state.getCharacter(self.player)

        # data = {
        #     # 'attack': chara.getAttack(),
        #     # 'attack': {
        #     #     'active':        a.getActive(),
        #     #     'start_up':      a.getStartUp(),
        #     #     'current_frame': a.getCurrentFrame(),
        #     # },
        #     'attack': make_dict_of_camel_method_return(chara.getAttack(), ['active', 'start_up', 'current_frame']),
        #     'chara':  make_dict_of_camel_method_return(chara, ['top', 'bottom', 'center_x', 'center_y', 'remaining_frame']),
        # }

        # from pprint import pprint; pprint(data)

        # self._i += 1
        # if self._i % 2 == 0:
        #     return 'A'
        # else:
        #     return '→'


class AgentBeta(AgentBase):
    def policy(self, state):
        # import inspect; import os; frame = inspect.currentframe(); print(f"DEBUG: {os.path.basename(frame.f_code.co_filename)}: {frame.f_lineno}: {self.__class__.__name__}.{frame.f_code.co_name}: called")
        # return 'B↑A'
        return '↑'


def main():
    env = Environment()
    env.play(AgentAlpha, AgentBeta)


if __name__ == '__main__':
    main()
