from time import time


SETTINGS = {
	'trace'   : False,
	'inplace' : True,
	'stamps'  : [],
	'headers' : [],
	'logger'  : [],
	'counter' : 0,
}


# class Meta(type):
# 	@staticmethod
# 	def __call__( header = '', logger = None ):
# 		if SETTINGS['trace']:
# 			SETTINGS['stamps'].append(time())
# 			SETTINGS['headers'].append(header)
# 			if SETTINGS['counter'] != 0:
# 				entry = "{!s:>4}  |  {:.3f}  |  {}".format( SETTINGS['counter'], SETTINGS['stamps'][-1] - SETTINGS['stamps'][-2], SETTINGS['headers'][-2] )
# 				if SETTINGS['inplace']:
# 					print(entry)
# 				if logger != None:
# 					SETTINGS['logger'] = logger
# 				SETTINGS['logger'].append(entry)
# 			SETTINGS['counter'] +=1


class Tracker:
	# __metaclass__ = Meta


	def __new__(cls, header='', logger=None):
		if SETTINGS['trace']:
			SETTINGS['stamps'].append(time())
			SETTINGS['headers'].append(header)
			if SETTINGS['counter'] != 0:
				entry = "{!s:>4}  |  {:.3f}  |  {}".format(SETTINGS['counter'],
				                                           SETTINGS['stamps'][-1] - SETTINGS['stamps'][-2],
				                                           SETTINGS['headers'][-2])
				if SETTINGS['inplace']:
					print(entry)
				if logger != None:
					SETTINGS['logger'] = logger
				SETTINGS['logger'].append(entry)
			SETTINGS['counter'] += 1


	@staticmethod
	def off():
		SETTINGS['trace'] = False

	@staticmethod
	def on():
		SETTINGS['trace'] = True

	@staticmethod
	def isOn():
		return SETTINGS['trace']

	@staticmethod
	def log():
		print('\n'.join( SETTINGS['logger'] ))


_STOPWATCH = {
	'last_duration': 0,
	'start':0,
	'duration': 0,
	'end': 0
}

class Stopwatch:

	@staticmethod
	def last():
		return _STOPWATCH['last_duration']

	@staticmethod
	def start():
		_STOPWATCH['last_duration'] = _STOPWATCH['duration']
		_STOPWATCH['start'] = time()
		_STOPWATCH['duration'] = 0
		_STOPWATCH['end'] = 0

	@staticmethod
	def end():
		_STOPWATCH['end'] = time()
		_STOPWATCH['duration'] = _STOPWATCH['end'] - _STOPWATCH['start']


if __name__ == '__main__':
	from zaider import moduleProgramScript
	exec( moduleProgramScript )