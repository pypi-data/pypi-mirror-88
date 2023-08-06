from DreamDiff import DreamDiff
from DreamDiff import Function
from DreamOptimize import Optimize

# Nesterov's accelerated gradient descent
f = 'tan(sin(x) + 3)'
Optimize.animate_grad_desc(f, 4, epsilon=0.00001, max_iters=500, eta=0.1, runtime=20, method='nesterov')

