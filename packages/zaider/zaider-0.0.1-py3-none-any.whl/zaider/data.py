

class Serializer:

	def __init__(self, destination = None, protocol = 2):
		self.destination = destination
		if type(destination) == str:
			self.format = destination.split('.')[-1]
			if self.format == 'pkl':
				import cPickle as serializer
				if protocol:
					self.protocol = protocol
			elif self.format == 'json':
				import json as serializer
		elif protocol:
			import cPickle as serializer
			self.protocol = protocol
		else:
			import json as serializer
		self.serializer = serializer


	def save(self, data):
		if self.destination:
			with open(self.destination, 'wb') as file:
				if hasattr(self,'protocol'):
					self.serializer.dump(data, file, protocol = self.protocol)
				else:
					self.serializer.dump(data, file)
				file.close()
		else:
			if hasattr(self, 'protocol'):
				self.serial = self.serializer.dumps(data, protocol = self.protocol)
			else:
				self.serial = self.serializer.dumps(data)


	def load(self):
		if self.destination:
			with open(self.destination, 'rb') as file:
				self.data = self.serializer.load(file)
				file.close()
		else:
			self.data = self.serializer.loads(self.serial)


if __name__ == '__main__':
	from zaider import moduleProgramScript
	exec( moduleProgramScript )