
from .functions import function, Function


@function('ADD')
class AddFunction(Function):
    MIN_ARGS = 2

    def eval(self) -> float:
        return sum(self.eval_args())


@function('SUB')
class SubFunction(Function):
    MIN_ARGS = MAX_ARGS = 2

    def eval(self) -> float:
        eval_args = self.eval_args()
        return eval_args[0] - eval_args[1]


@function('MUL')
class MulFunction(Function):
    MIN_ARGS = 2

    def eval(self) -> float:
        r = 1
        for e in self.eval_args():
            r *= e

        return r


@function('DIV')
class DivFunction(Function):
    MIN_ARGS = MAX_ARGS = 2

    def eval(self) -> float:
        eval_args = self.eval_args()

        if eval_args[1]:
            return eval_args[0] / eval_args[1]

        else:
            return 0


@function('MOD')
class ModFunction(Function):
    MIN_ARGS = MAX_ARGS = 2

    def eval(self) -> float:
        eval_args = self.eval_args()

        if eval_args[1]:
            return eval_args[0] % eval_args[1]

        else:
            return 0


@function('POW')
class PowFunction(Function):
    MIN_ARGS = MAX_ARGS = 2

    def eval(self) -> float:
        eval_args = self.eval_args()

        return eval_args[0] ** eval_args[1]
