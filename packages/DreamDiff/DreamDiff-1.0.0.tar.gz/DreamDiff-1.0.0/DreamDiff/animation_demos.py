from DreamDiff import DreamDiff
from DreamDiff import Function
from DreamOptimize import Optimize

# Newton's Method
#f = 'x^3 - 3*x^2 + 4'
#Optimize.animate_newtons(f, 0.3, 0.000001, max_iters=500, runtime=20)

# Standard gradient descent
#f = 'tan(sin(x) + 3)'
#Optimize.animate_grad_desc(f, 4, epsilon=0.00001, max_iters=500, eta=0.1, runtime=20, method='grad')

# Nesterov's accelerated gradient descent
#f = 'tan(sin(x) + 3)'
#Optimize.animate_grad_desc(f, 4, epsilon=0.00001, max_iters=500, eta=0.1, runtime=20, method='nesterov')

# Too-high ETA
#f = 'tan(sin(x) + 3)'
#Optimize.animate_grad_desc(f, 4, epsilon=0.00001, max_iters=500, eta=0.3, runtime=20)
