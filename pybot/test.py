__author__ = 'lope'
import mlp
import numpy as np
# from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show

print("Helly ML!")
myMLP = mlp.MLP(2, 8, 1)
myBack = mlp.Backpropagation(myMLP, 0.3, 0.001)

print("Backpropagation: ------------------------------")
# for i in range(5000):
# myBack.iterate([[0, 0], [0, 1], [1, 0], [1, 1], [0.5, 0.5], [0.75, 0.5], [0.3, 0.5], [0.45, 0.2], [0.2, 0.7]],

# [[0], [1], [1], [0], [0], [1], [1], [0], [1]])
print(myMLP.compute([0, 0]))
print(myMLP.compute([0, 1]))
print(myMLP.compute([1, 0]))
print(myMLP.compute([1, 1]))  # tender a 01 11 11 01
print("------------------------------")
