#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
from scipy.stats import norm
norm.cdf(1.96)

def solve(m1,m2,std1,std2):
  a = 1/(2*std1**2) - 1/(2*std2**2)
  b = m2/(std2**2) - m1/(std1**2)
  c = m1**2 /(2*std1**2) - m2**2 / (2*std2**2) - np.log(std2/std1)
  return np.roots([a,b,c])

inputs = ["Mean A: ", "StdDev A: ", "Mean B: ", "StdDev B: "]
ins = []

for i in range( len( inputs ) ):
    ins.append( float( input( inputs[i] ) ) )

one = 0 if ins[0] < ins[2] else 2
two = 2 - one

m1 = ins[one]
std1 = ins[one+1]
m2 = ins[two]
std2 = ins[two+1]
mstd = max(std1, std2)

annotation = "A:  mu=%0.1f, std=%0.1f\n" % (m1, std1)
annotation += "B:  mu=%0.1f, std=%0.1f\n" % (m2, std2)

#Get point of intersect
result = solve(m1,m2,std1,std2)

#Get point on surface
x = np.linspace(m1-3*mstd,m2+3*mstd,10000)
plot1=plt.plot(x,norm.pdf(x,m1,std1))
plot2=plt.plot(x,norm.pdf(x,m2,std2))
plot3=plt.plot(result,norm.pdf(result,m1,std1),'o')

#Plots integrated area
r = result[0]
olap = plt.fill_between(x[x>r], 0, norm.pdf(x[x>r],m1,std1),alpha=0.3)
olap = plt.fill_between(x[x<r], 0, norm.pdf(x[x<r],m2,std2),alpha=0.3)

# integrate
area = norm.cdf(r,m2,std2) + (1.-norm.cdf(r,m1,std1))
annotation += "Overlap is {:.0%}".format(area)
plt.text(0.02,0.98,annotation, transform=ax.transAxes, verticalalignment='top' )

ax.tick_params(labelleft=False)
plt.show()
