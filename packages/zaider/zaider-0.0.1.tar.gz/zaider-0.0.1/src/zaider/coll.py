

def union_intersecting_sets(sets):
	'''
	:param list_of_sets: list of sets
	:return: list of unioned intersecting sets
	'''
	if sets[0] is not set:
		sets[0] = set(sets[0])
	i = 1
	while i < len(sets):
		if sets[i] is not set:
			sets[i] = set(sets[i])
		j = 0
		while j < i:
			if len(sets[i] & sets[j]) > 0:
				sets[j] = sets[i] | sets[j]
				del sets[i]
				i -= 1
				break
			j += 1
		i += 1
	return sets


if __name__ == '__main__':
	from zaider import moduleProgramScript
	exec( moduleProgramScript )