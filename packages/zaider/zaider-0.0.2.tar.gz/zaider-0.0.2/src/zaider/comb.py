import numpy as np


def cross_ref(x1, x2=None, reftype='holistic', new_axis=-1, ref_axis=-1, ):
	if x2 is None:
		x2 = x1

	if reftype == 'holistic':
		s1 = x1.shape[ref_axis]
		s2 = x2.shape[ref_axis]
		x1 = np.repeat(np.expand_dims(x1, new_axis), s2, axis=new_axis)
		x2 = np.repeat(np.expand_dims(x2, new_axis), s1, axis=new_axis)
		x1 = np.swapaxes(x1, new_axis - 1, ref_axis)
	elif reftype == 'strict upper triangle':
		pass

	return x1, x2

def test(spefarg=None,*args,**kwargs):
	"""
	Test function
	:param spefarg: specific arg for test
	:param args: args for test
	:param kwargs: kwargs for test
	:return:
	"""
	print(spefarg,type(spefarg))

	for arg in args:
		print(arg,type(arg))

	for k,arg in kwargs.items():
		print(k,arg,type(k),type(arg))

if __name__ == '__main__':
	from zaider import moduleProgramScript
	exec(moduleProgramScript)
	# from zaider import Program
	# Program(globals(), locals()).run()