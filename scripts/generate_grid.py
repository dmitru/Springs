
from sys import argv
from optparse import OptionParser
from random import randint, shuffle

def generate_model(size, random=False):
	n = size * size
	
	xs = []
	ys = []
	springs = []
	for y in range(size):
		for x in range(size):
			for dx, dy in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
				nx = x + dx
				ny = y + dy
				if nx >= 0 and nx < size and ny >= 0 and ny < size:
					a = y * size + x
					b = ny * size + nx
					k = 1
					if a > b:
						springs.append((a + 1, b + 1, k))
			xs.append(x)
			ys.append(y)	
	
	if random:
		fixed_points = []
		fixed_points += [randint(1, size) for _ in range(randint(1, size / 3))][:randint(1,10)]
		fixed_points += [size * randint(0, size - 1) + 1 for _ in range(randint(1, size / 3))][:randint(1,10)]
		fixed_points += [size * randint(1, size) for _ in range(randint(1, size / 3))][:randint(1,10)]
		fixed_points += [randint(n - size + 1, n) for _ in range(randint(1, size / 3))][:randint(1,10)]
		fixed_points = list(set(fixed_points))
	else:
		fixed_points = [1, size, n - size + 1, n]
	
	points_text = '\n'.join(['%d %d' % (x, y) for x, y in zip(xs, ys)])
	springs_text = '\n'.join(['%d %d %f' % spring for spring in springs])
	fixeds_text = ' '.join(map(str, fixed_points))
	
	result = '%d\n%s\n%d\n%s\n%d\n%s' % (n, points_text, len(springs), springs_text, len(fixed_points), fixeds_text)
	
	return result

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-s', '--size', dest='size', default=20)
	parser.add_option('-o', '--output', dest='output_file', default='model.txt')
	parser.add_option('-r', '--random', dest='random', action='store_true', default=False)
	
	(options, args) = parser.parse_args()
	if len(args) != 0:
		print('Usage: generate_model.py [-s | --size <model size>] [-o | --output <output file>] [-r | --random]')
		exit(1)
	
	size = int(options.size)
	print('Generating model of size %d...' % size)

	model_str = generate_model(size, options.random)
	
	f = open(options.output_file, 'w')
	print('Writing model to file %s...' % options.output_file)
	print(model_str, file=f)
	f.close()
	
	print('Done!')