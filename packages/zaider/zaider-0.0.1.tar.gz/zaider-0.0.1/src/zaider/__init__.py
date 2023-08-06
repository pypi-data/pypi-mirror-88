from zaider.diag import Tracker
import sys

import importlib as importer
import os
from time import time
from pprint import pprint

ZAIDERPATH = os.environ['Zaider']
sys.path.append( ZAIDERPATH + '/envs/py3/Lib/' )
sys.path.append( ZAIDERPATH + '/envs/py3/Lib/site-packages/' )

def impZd(name,package=''):
	if package == '': package = name.split('.')[0]
	zaiderenv = ZAIDERPATH + '/envs/py3/Lib/'
	try:
		sp = importer.import_module( name, zaiderenv+package+'.py' )
		return sp
	except:
		zaiderenv += 'site-packages/'
		return importer.import_module( name, zaiderenv+package+'.py' )


def findZd(name,package=''):
	if package == '': package = name.split('.')[0]
	zaiderenv = ZAIDERPATH + 'envs/py3/Lib/'
	try:
		sp = importer.util.find_spec( name, zaiderenv+package )
		return sp
	except:
		zaiderenv += 'site-packages/'
		return importer.util.find_spec( name, zaiderenv+package )


class Program:
	def __init__(self, globalV, localV):
		# pprint(globalV)
		# pprint(localV)
		self.namespace = [ globalV, localV ]
		args = sys.argv[1:]

		need_help = False
		c = 0
		for arg in args:
			if arg in ('-h','--help'):
				need_help = True
			elif arg in ('-t','--tracker'):
				Tracker.on()

			elif arg.startswith('-p:'):
				self.protocol = arg[3:]
			elif arg.startswith('--protocol:'):
				self.protocol = arg[11:]

			elif arg.startswith('-to:'):
				self.output_to = arg[4:]

			elif arg.startswith('-o:'):
				self.out_type = eval(arg[3:], globalV, localV)
			elif arg.startswith('--output:'):
				self.out_type = eval(arg[8:], globalV, localV)

			elif arg.startswith('-om:'):
				self.out_method = arg[4:]
			elif arg.startswith('--output_method:'):
				self.out_method = arg[17:]

			else:
				break
			c += 1

		try:
			self.func = eval(args[c], globalV, localV)
			c+=1
		except:
			try:
				self.func = eval('main', globalV, localV)
			except:
				if c > len(args)-1:
					sys.exit(f'Cannot find main function')
				else:
					sys.exit(f'Cannot find either {args[c]} or main function')

		if need_help:
			help(self.func)
			sys.exit()

		self.args = [ eval(arg, globalV, localV) for arg in args[c:] if arg.find('=')==-1 ]
		self.kwargs = { eval(a[0],globalV, localV):eval(a[1],globalV, localV) for a in [ arg.split('=',1) for arg in args[c:] if arg.find('=')>0 ] }

		if Tracker.isOn():
			print(f'\nFunction to be executed: {self.func.__name__}')


		if Tracker.isOn():
			print('\nRunning program...\n')
			start = time()

		# for i in range(len(self.args)):
		# 	arg = self.args[i]
		# 	if type(arg) == str:
		# 		try:
		# 			if '"' not in arg:
		# 				self.args[i] = f'"{arg}"'
		# 			elif "'" not in arg:
		# 				self.args[i] = f"'{arg}'"
		# 			else:
		# 				raise
		# 		except:
		# 			print(f'cannot add quotes to argument: {arg}')

		# call = 'self.command( {} )'.format(', '.join(self.args))
		try:
			# out = eval( call )
			out = self.func(*self.args,**self.kwargs)
			# print('out: ',out)
		except Exception as E:
			raise E
			# raise Exception('{}\n{}'.format(E,call))
		try:
			elapsed = time() - start
			cmd_time = f'\nFunction elapse time: {elapsed}'
		except:
			pass


		if out is not None:
			if hasattr(self, 'out_type'):
				if type(out) != self.out_type:
					try:
						out = self.out_type(out)
					except:
						if Tracker.isOn():
							print(f'\nCould not convert output to {self.out_type}\n')

			print('\nOutput:\n')
			if hasattr(self,'out_method'):
				if self.out_method in ('pp', 'pprint'):
					from pprint import pprint
					pprint(out)
				else:
					print(out)

				# else:
				# 	import _pickle as pickle
				# 	print( pickle.dumps(out, eval(self.protocol)) )

		try:
			print(cmd_time)
		except: pass
		# try:
		# 	elapsed = time() - start
		# 	print('\nProgram elapse time: {}'.format(elapsed))
		# except: pass

moduleProgramScript = """
from zaider import Program
Program( globals(), locals() )
"""