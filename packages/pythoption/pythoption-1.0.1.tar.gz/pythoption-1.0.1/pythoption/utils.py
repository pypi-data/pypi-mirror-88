from abc import abstractmethod
from numbers import Real



def enum(**enums):
    return type('Enum', (), enums)

OptionType = enum(CALL='call', PUT='put')
OptionExerciseType = enum(EUROPEAN='european', AMERICAN='american')
OptionModel = enum(BLACK_SCHOLES='black_scholes', BINOMIAL_TREE='binomial_tree', MONTE_CARLO='monte_carlo')
OptionMeasure = enum(VALUE='value', DELTA='delta', THETA='theta', RHO='rho', VEGA='vega', GAMMA='gamma')

DEFAULT_BINOMIAL_TREE_NUM_STEPS = 25
DEFAULT_MONTE_CARLO_NUM_STEPS = 50
DEFAULT_MONTE_CARLO_NUM_PATHS = 100


class Instrument(object):
    @abstractmethod
    def run_model(self):
        """Calculate measures (i.e. theoretical value & greeks) for this instrument"""

def is_number(x):
    return isinstance(x, Real)