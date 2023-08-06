#!/usr/bin/env python3

from FADiff import FADiff as ad    # User needs to import
import Elems as ef           # User needs to import
import numpy as np


# TODO: Debugging, etc. --
print(f'---- DEMOS / DEBUGGING / VERIFY CALCULATIONS ----\n')

ad.set_mode('forward')         # Set the mode to forward

print('Create input vars -->')
print(f'x = FADiff.new_scal(2)')
x = ad.new_scal(2, name='x')
print(f'y = FADiff.new_scal(5)')
y = ad.new_scal(5, name='y')
print(f'z = FADiff.new_scal(3)')
z = ad.new_scal(3, name='z')
print(f'x.val --> '                   
      f'{x.val}')              # Should be [2]
print(f'x._der --> '           # '_der' is a dictionary containing the 
      f'{x._der}')             #   partial derivatives for a var
print(f'x.der --> '            # 'der' (no underscore) returns only the partial
      f'{x.der}')              #   derivatives for input vars used in calculation
print(f'y.val --> '                  
      f'{y.val}')              # Should be [5]
print(f'y._der --> '           # '_der' is a dictionary containing the 
      f'{y._der}')             #   partial derivatives for a var
print(f'y.der --> '
      f'{y.der}')              # Should be [1]
print(f'z.val --> '                  
      f'{z.val}')              # Should be [3]
print(f'z._der --> '           # '_der' is a dictionary containing the 
      f'{z._der}')             #   partial derivatives for a var
print(f'z.der --> '
      f'{z.der}')              # Should be [1]

print(f'\ncheck = x * y + ef.sin(x)')
check = x * y + ef.sin(x)
print(f'check.val --> '
      f'{check.val}')                    # Should be [10.909...]
print(f'check.der --> '
      f'{check.der}')                 # Should be [4.583..., 2]
print(f'check._der.get(x) --> '
      f'{check._der.get(x)}')         # Should be 4.583...
print(f'check._der.get(y) --> '  
      f'{check._der.get(y)}')         # Should be 2

print(f'\ncheck = ef.sin(x + y)')
check = ef.sin(x + y)
print(f'check.val --> ' 
      f'{check.val}')                    # Should be [0.656...]
print(f'check.der --> '
      f'{check.der}')
print(f'check._der.get(x) --> '
      f'{check._der.get(x)}')         # Should be 0.753...
print(f'check._der.get(y) --> '
      f'{check._der.get(y)}')         # Should be 0.753...

print(f'\ncheck = ef.sin(x * y)')
check = ef.sin(x * y)
print(f'check.val --> '
      f'{check.val}')                    # Should be [-0.544..]
print(f'check.der --> '
      f'{check.der}')                    # Should be [-4.195..., -1.678...]
print(f'check._der.get(x) --> '
      f'{check._der.get(x)}')         # Should be -4.195...
print(f'check._der.get(y) --> '
      f'{check._der.get(y)}')         # Should be -1.678...

print(f'\ncheck = 8 * x')
check = 8 * x
print(f'check.val --> '
      f'{check.val}')                    # Should be 16
print(f'check.der --> '
      f'{check.der}')
print(f'check._der.get(x) --> '
      f'{check._der.get(x)}')         # Should be 8

print(f'\ncheck = 8 * y')
check = 8 * y
print(f'check.val --> '
      f'{check.val}')                    # Should be [40]
print(f'check.der --> '
      f'{check.der}')                    # Should be [8]
print(f'check._der.get(y) --> '
      f'{check._der.get(y)}')         # Should be 8

print(f'\ncheck = 8 + x')
check = 8 + x
print(f'check.val --> '
      f'{check.val}')                    # Should be [10]
print(f'check.der --> '
      f'{check.der}')                    # Should be [1]
print(f'check._der.get(x) --> '
      f'{check._der.get(x)}')         # Should be 1

print(f'\ncheck = 8 + y')
check = 8 + y
print(f'check.val --> '
      f'{check.val}')                    # Should be 13
print(f'check.der --> '
      f'{check.der}')
print(f'check._der.get(y) --> '
      f'{check._der.get(y)}')         # Should be 1

print(f'\ncheck = x * y + ef.sin(x) + z')  # Check that uses three input vars
check = x * y + ef.sin(x) + z
print(f'check.val --> '
      f'{check.val}')                    # Should be 13.909...
print(f'check.der --> '
      f'{check.der}')                 # Should be [4.583..., 2, 1]
print(f'check._der.get(x) --> '
      f'{check._der.get(x)}')         # Should be 4.583...
print(f'check._der.get(y) --> '  
      f'{check._der.get(y)}')         # Should be 2
print(f'check._der.get(z) --> '  
      f'{check._der.get(z)}')         # Should be 1

print(f'\nx1 = ad.new_scal(2)\n'
      f'x2 = ad.new_scal(3)\n'
      f'check = x1 * x2 + x1')
x1 = ad.new_scal(2)
x2 = ad.new_scal(3)
check = x1 * x2 + x1
print(f'check.val --> '
      f'{check.val}')                    # Should be [8]
print(f'check.der --> '
      f'{check.der}')                    # Should be [4, 2]

print(f'\ncheck = x1 - x2')
check = x1 - x2
print(f'check.val --> '
      f'{check.val}')
print(f'check.der --> '
      f'{check.der}')

# TODO: VECTOR DEBUGGING --
print()

print(f'x1 = ad.new_vect(np.array([2, 3, 4]))\n'
      f'x2 = ad.new_vect(np.array([3, 2, 1]))')
x1 = ad.new_vect(np.array([2, 3, 4]))
x2 = ad.new_vect(np.array([3, 2, 1]))
print(f'x1.val --> '       
      f'{x1.val}')
print(f'x1.der -->\n'       # Should be array of ones of size x1
      f'{x1.der}')
print(f'x2.val --> '       
      f'{x2.val}')
print(f'x2.der -->\n'       # Should be identity of ones of size x2
      f'{x2.der}')

print(f'\ncheck = x1 - x2')
check = x1 - x2
print(f'check.val --> '
      f'{check.val}')
print(f'check.der -->\n'
      f'{check.der}')
print(f'check.der (pretty printed) -->')
for mat in check.der:
    print(mat)
print(f'check._der.get(x1) -->\n'
      f'{check._der.get(x1)}')
print(f'check._der.get(x2) -->\n'
      f'{check._der.get(x2)}')

# TODO: FUNCTION VECTOR (FuncVect.py) DEBUGGING --

print()

print(f'x1 = ad.new_scal(3)\n'
      f'x2 = ad.new_scal(2)\n'
      f'f1 = x1 * x2 + x1\n'
      f'f2 = 8 * x2')
x1 = ad.new_scal(3)
x2 = ad.new_scal(2)
f1 = x1 * x2 + x1
f2 = 8 * x2

print(f'\nf = ad.new_funcvect([f1, f2])')
f = ad.new_funcvect([f1, f2])
print(f'f.val --> '
      f'{f.val}')
print(f'f.der -->\n'
      f'{f.der}')

print()

print(f'f1 = x1')
f1 = x1

print(f'\nf = ad.new_funcvect([f1, f2])')
f = ad.new_funcvect([f1, f2])
print(f'f.val --> '
      f'{f.val}')
print(f'f.der -->\n'
      f'{f.der}')

print()

print(f'f1 = x1 * x2 + x1\n'
      f'f2 = x1 / x2')
f1 = x1 * x2 + x1
f2 = x1 / x2

print(f'\nf = ad.new_funcvect([f1, f2])')
f = ad.new_funcvect([f1, f2])
print(f'f.val --> '
      f'{f.val}')
print(f'f.der -->\n'
      f'{f.der}')

print()

print(f'x1 = ad.new_vect(np.array([2, 3, 4]))')
# print(f'x2 = ad.new_vect(np.array([1, 3, 2]))')
x1 = ad.new_vect(np.array([2, 3, 4]))
# x2 = ad.new_scal(np.array([1, 3, 2]))
print('f1 = x1 * x1')
f1 = x1 * x1
print('f2 = x1 * 8')
f2 = x1 * 8
print(f'\nf = ad.new_funcvect([f1, f2])')
f = ad.new_funcvect([f1, f2])
print(f'f.val --> '
      f'{f.val}')
print(f'f.der -->\n'
      f'{f.der}')
