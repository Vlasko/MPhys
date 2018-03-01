from numpy import cos, inf, zeros, array, exp, conj, nan, isnan, pi, sin

import numpy as np
import time

start_time = time.time()

cos_theta0 = 1
# at first set theta1 to 0
cos_theta1 = 1
# when theta1 is 0, then so too is theta1
cos_theta2 = 1
# when theta1 is 0, then so too is theta2
n_0 = 1
# for air the refractive index is ~1

# refractive index of Cu
n_2 = 0.637

print(n_2)

# we want n to vary between 0 and 3 with a step of 0.1
steps = int(3/0.1) + 1
n = np.empty((steps))
filler = np.arange(0,3.1,0.1)
index_n = np.arange(n.size)
np.put(n,index_n,filler)

# we want k to vary between 0 and 3 with a step of 0.1
k = np.empty((steps))
index_k = np.arange(k.size)
np.put(k,index_k,filler)

n = np.array(n)
k = np.array(k).reshape((-1, 1))
n_com = n + k.repeat(len(n), 1) * 1j

print (n_com)
print ( "time", time.time() - start_time)

r_01 = (cos_theta0 - n_com*cos_theta1)/(cos_theta0 + n_com*cos_theta1)
t_01 = (2*cos_theta0)/(cos_theta0 + n_com*cos_theta1)

# print(r_01)
# print(t_01)

r_12 = (n_com*cos_theta1 - n_2*cos_theta2)/(n_com*cos_theta1 + n_2*cos_theta2)
t_12 = (2*n_com*cos_theta1)/(n_com*cos_theta1 + n_2*cos_theta2)

# print(r_12)
# print(t_12)

lamda = 800 # in units nm
d = 200  # in units nm
beta = ((2*np.pi)/lamda)*n_com*d*cos_theta1

# print("Beta is equal to {}".format(beta))

z = 0 + 1j

block = np.exp(2*z*beta)
# double check whether this is e^+ or e^-

# not sure if this is defo doing what we hope
# but it is cycling through the set because we do have
# values at each "step"

# n is what we are changing

# should I be running over both i and j?

for i in r_01, r_12, block:
    for j in i:
        r_film = (r_01 + (r_12*block))/(1 + r_01*r_12*block)
    # print r_film

print ( "time 2", time.time() - start_time)
# find r_film for all value of n contained in the array

for i in t_01, t_12, block:
    for j in i:
        t_film = (t_01*t_12*block)/(1 + r_01*r_12*block)

# find the absolute value of this and then square it
ABS_R = np.absolute(r_film)
# print(ABS_R)
R = np.power(ABS_R,2)
# find the value of R which is equal to square of absolute value of r

ABS_T = np.absolute(t_film)
# print(ABS_T)
T = n_2*np.power(ABS_T,2)
# find the value of T which is equal to square of absolute value of t

A = 1 - T - R

print ( "time 3", time.time() - start_time)

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
# imports for Plotly

plotly.tools.set_credentials_file(username='luka.j.v', api_key='K1pamGZFvMc64DABuoro')
# username and api_key to host Plotly plots in my account

print ( "time 4", time.time() - start_time)

# Contour plot of Absorption data for Copper
contour = [
    go.Contour(
        z=A,
        x=n,
        y=k,
        colorscale = [[0, 'rgb(255, 145, 97)'], [1, 'rgb(116, 11, 124)']]
        )
]

contour_layout = go.Layout(
    title='Cu Absorption Contour Plot (λ=700nm)',
    height = 800,
    width = 800,
)

fig = go.Figure(data = contour, layout = contour_layout)

py.iplot(fig, filename='Cu Absorption Contour (λ=700nm)')
