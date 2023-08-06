import numpy as np
import sys

def rec(n):
	"""
	Returns the nth Recaman number
	"""
	c=0
	s=set()
	for i in range(n):
		c -= i
		if c in s or c < 0:
			c += 2*i
		s.add(c)
	return c


def rec2(n):
	"""
	Returns a generator with the first n numbers of the Recaman sequence
	"""
	c=0
	s=set()
	for i in range(n):
		c -= i
		if c in s or c < 0:
			c += 2*i
		yield c
		s.add(c)


def fib(n):
	"""
	Returns the nth Fibonacci number
	"""
	a = b = 1
	for _ in range(n-1):
		a, b = b, a+b
	return a


def fib2(n):
	"""
	Returns a generator with the first n numbers of the Fibonacci sequence
	"""
	a = b = 1
	for _ in range(n-1):
		yield a
		a, b = b, a+b
	yield a


def div2(n=10e4, primes_mask = True, composite_mask = False, highly_composite_mask = True ):
	x = np.arange(1,n+1)
	ma = np.fromfunction(lambda *shape: shape[-2] > shape[-1], (n, n))
	xx = np.ma.array( np.lib.stride_tricks.as_strided(x,shape=(n,n),strides=(x.itemsize,0)), mask=ma )
	y = np.sum( ( x % xx ) == 0, axis = 0 ).view(np.ndarray)
	yield x
	yield y
	if primes_mask: yield y == 2
	if composite_mask: yield y > 2
	if highly_composite_mask:
		ma = np.fromfunction(lambda *shape: shape[-2] >= shape[-1], (n, n))
		yy = np.ma.array(np.lib.stride_tricks.as_strided(y, shape=(n, n), strides=(y.itemsize, 0)), mask=ma)
		yield ~np.any(y <= yy, axis=0)


def primes2(n=10e4):
	x,_,m = div2(n,True,False,False)
	return x[m]


def hcn2(n=10e4):
	"""
	Highly Composite Numbers
	:param n:
	:return:
	"""
	x,y,m = div2(n,False,False,True)
	return x[m],y[m]


if __name__=='__main__':
	from zaider import moduleProgramScript
	exec(moduleProgramScript)