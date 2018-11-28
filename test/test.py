from numpy import *


arr = mat([[0,1,3], [1,0,4]])
# arr = array(arr)

def avg(intA):
   return mean(intA[intA==0], 1)[0][0]

avg = float(avg(arr[1,:]))
print avg






