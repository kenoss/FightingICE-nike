import enum


class MyEnum(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Action(MyEnum):
    NEUTRAL = enum.auto()

    # For visual effcts
    # STAND = enum.auto()
    # AIR = enum.auto()
    # STAND_GUARD_RECOV = enum.auto()
    # CROUCH_GUARD_RECOV = enum.auto()
    # AIR_GUARD_RECOV = enum.auto()
    # STAND_RECOV = enum.auto()
    # CROUCH_RECOV = enum.auto()
    # AIR_RECOV = enum.auto()
    # CHANGE_DOWN = enum.auto()
    # DOWN = enum.auto()
    # RISE = enum.auto()
    # LANDING = enum.auto()
    # THROW_HIT = enum.auto()
    # THROW_SUFFER = enum.auto()

    # For move
    # FORWARD_WALK = enum.auto()
    # DASH = enum.auto()
    # BACK_STEP = enum.auto()
    # CROUCH = enum.auto()
    # JUMP = enum.auto()
    # FOR_JUMP = enum.auto()
    # BACK_JUMP = enum.auto()
    # STAND_GUARD = enum.auto()
    # CROUCH_GUARD = enum.auto()
    # AIR_GUARD = enum.auto()
    MOVE_UB = '7'
    MOVE_U = '8' # == JUMP
    # JUMP = '8'
    MOVE_UF = '9'
    MOVE_B = '4'
    MOVE_F = '6'
    MOVE_DB = '1'
    MOVE_D = '2' # == CRUNCH
    # CRUNCH = '2'
    MOVE_DF = '3'
    MOVE_FF = 'DASH'
    MOVE_BB = 'BACK_STEP'


    THROW_A = enum.auto()
    THROW_B = enum.auto()
    # STAND_A = enum.auto()
    # STAND_B = enum.auto()
    A = enum.auto()
    B = enum.auto()
    STAND_FA = enum.auto()
    STAND_FB = enum.auto()
    # AIR_A = enum.auto() # == A
    # AIR_B = enum.auto() # == B
    AIR_DA = enum.auto()
    AIR_DB = enum.auto()
    AIR_FA = enum.auto()
    AIR_FB = enum.auto()
    AIR_UA = enum.auto()
    AIR_UB = enum.auto()
    CROUCH_A = enum.auto()
    CROUCH_B = enum.auto()
    CROUCH_FA = enum.auto()
    CROUCH_FB = enum.auto()
    STAND_D_DF_FA = enum.auto()
    STAND_D_DF_FB = enum.auto()
    STAND_F_D_DFA = enum.auto()
    STAND_F_D_DFB = enum.auto()
    STAND_D_DB_BA = enum.auto()
    STAND_D_DB_BB = enum.auto()
    AIR_D_DF_FA = enum.auto()
    AIR_D_DF_FB = enum.auto()
    AIR_F_D_DFA = enum.auto()
    AIR_F_D_DFB = enum.auto()
    AIR_D_DB_BA = enum.auto()
    AIR_D_DB_BB = enum.auto()
    # STAND_D_DF_FC = enum.auto()
    PROJECTILE = 'STAND_D_DF_FC'
