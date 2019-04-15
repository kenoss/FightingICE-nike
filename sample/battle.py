import sys
import pathlib
sys.path.append(pathlib.Path(__file__).resolve().parents[1].as_posix())
sys.path.append((pathlib.Path(__file__).resolve().parents[1] / 'team/ut-dl-basics-2019-spring/d4').as_posix())


from fice_nike.action import Action
from fice_nike.agent_base import AgentBase
from fice_nike.environment import Environment


from ut_dl_basics_2019_spring_team_d4.comp.frame import *
from ut_dl_basics_2019_spring_team_d4.comp.policy import *
from ut_dl_basics_2019_spring_team_d4.comp.rulebase_agent import *
from ut_dl_basics_2019_spring_team_d4.comp.rulebase_policy import *


# import re
# 
# 
# def camelize_case(snake_case_string):
#     return re.sub('_(.)', lambda x: x.group(1).upper(), snake_case_string)
# 
# 
# def make_dict_of_camel_method_return(x, methods, prefix='get_'):
#     return dict((k, getattr(x, camelize_case(prefix + k))()) for k in methods)


def main():
    env = Environment()
    # env.play(RulebaseAgentWrfWeepRandomAlpha, RulebaseAgentWrfWeepRandomAlpha)
    # env.play(RulebaseAgentWrfWeepRandomAlpha, RulebaseAgentRandomAlpha)
    # env.play(RulebaseAgentRandomAlpha, RulebaseAgentRandomAlpha)
    # env.play(RulebaseAgentWrfWeepRandomAlpha, RulebaseAgentWrfWeepNoAction)
    # env.play(RulebaseAgentWrfWeepNoAction, RulebaseAgentRandomAlpha)
    # env.play(RulebaseAgentWrfWeepNoAction, RulebaseAgentWepegWeepRandomAlpha)
    env.play(RulebaseAgentWrfWeepRandomAlpha, RulebaseAgentGarnet)
    # env.play(RulebaseAgentGarnet, RulebaseAgentGarnet, player_character='GARNET', opponent_character='GARNET')


if __name__ == '__main__':
    main()
