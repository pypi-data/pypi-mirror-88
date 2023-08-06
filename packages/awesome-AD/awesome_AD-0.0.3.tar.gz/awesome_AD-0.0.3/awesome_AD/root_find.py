import numpy as np
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from awesome_AD.autoDiff import AutoDiff,exp,sin,cos,tan
from awesome_AD.jacobian import Jacobian

# using the example from the class
def f(x):
    return x - exp(-2.0 * sin(4.0*x) * sin(4.0*x))

tol = 1.0e-08 
max_it = 100 
root = None 

print('-------root-finding using forward mode-----')
x = AutoDiff(0.1, der = 1)
for k in range(max_it):
    # using Jacobian function to get Jacobian matrix
    J = Jacobian([f(x)],[x])
    # get[0][0] since one variable and one function, equal to f(x).der
    delta_x = -f(x).val / J[0][0]
    if (abs(delta_x) <= tol):
        root = x + delta_x
        print("Found root at x = {0:17.16f} after {1} iteratons.".format(root.val[0], k+1))
        break
    print("At iteration {0}, Delta x = {1:17.16f}".format(k+1, delta_x[0]))
    x += delta_x


from awesome_AD.autoDiffRev import AutoDiffRev,exp,sin,cos,tan
from awesome_AD.jacobianRev import JacobianRev

print('-------root-finding using reverse mode------')

x = AutoDiffRev(0.1)
for k in range(max_it):
    # using Jacobian function to get Jacobian matrix
    J = JacobianRev([f(x)],[x])
    # get[0][0] since one variable and one function, equal to f(x).der
    delta_x = -f(x).val / J[0][0]
    if (abs(delta_x) <= tol):
        root = x + delta_x
        print("Found root at x = {0:17.16f} after {1} iteratons.".format(root.val[0], k+1))
        break
    print("At iteration {0}, Delta x = {1:17.16f}".format(k+1, delta_x[0]))
    x += delta_x