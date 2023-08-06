from DreamDiff import DreamDiff
from DreamDiff import Function
from DreamOptimize import Optimize

# Too-high ETA
f = 'tan(sin(x) + 3)'
Optimize.animate_grad_desc(f, 4, epsilon=0.00001, max_iters=500, eta=0.3, runtime=20)
