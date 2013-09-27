import numpy as np
from copy import deepcopy
from datatypes import *
	
def _to_linear_system(model):
	'''Transforms a model into a linear system Ax = b.
	Returns a tuple (A, b), where A and b are numpy's matrices'''
	n = len(model.points)
	X = np.zeros((n, n))
	Y = np.zeros((n, n))
	x = np.zeros(n)
	y = np.zeros(n)
	
	for point, i in zip(model.points, range(n)):
		point_row_x = X[i,:]
		point_row_y = Y[i,:]
		ksum = 0
		for spring in point.springs:
			ksum += spring.k
			j = spring.p1 if spring.p1 != i else spring.p2
			point_row_x[j] = -spring.k
			point_row_y[j] = -spring.k
		point_row_x[i] = ksum
		point_row_y[i] = ksum
		
	for point, i in zip(model.points, range(n)):
		point_row_x = X[i,:]
		point_row_y = Y[i,:]
		if point.fixed:
			X[:,i] = np.zeros(n)
			X[i,:] = np.zeros(n)
			point_row_x = X[i,:]
			point_row_x[i] = 1.0
			Y[:,i] = np.zeros(n)
			Y[i,:] = np.zeros(n)
			point_row_y = Y[i,:]
			point_row_y[i] = 1.0
			
			for spring in point.springs:
				j = spring.p1 if spring.p1 != i else spring.p2
				x[j] += spring.k * point.x
				y[j] += spring.k * point.y
				
	for point, i in zip(model.points, range(n)):
		if point.fixed:
			x[i] = point.x 
			y[i] = point.y 
	
	print(X)
	print(Y)
	print(x)
	print(y)
	
	A = np.hstack([
			np.vstack([X, np.zeros((n, n))]), 
			np.vstack([np.zeros((n, n)), Y]) 
		])
		
	b = np.hstack([x, y])
	
	return (A, b)
		

def solve(model):
	A, b = _to_linear_system(model)
	solution = np.linalg.solve(A, b)
	n = len(model.points)
	
	xs = solution[:n]
	ys = solution[n:]
	
	print(xs)
	print(ys)
	
	new_model = deepcopy(model)
	for i, x, y in zip(range(n), xs, ys):
		new_model.points[i].x = x
		new_model.points[i].y = y
		
	return new_model