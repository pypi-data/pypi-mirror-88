from DreamDiff import DreamDiff
from DreamDiff import Function
from DreamOptimize import Optimize

# Newton's Method
f = 'x^3 - 3*x^2 + 4'
Optimize.animate_newtons(f, 0.3, 0.000001, max_iters=500, runtime=20)

