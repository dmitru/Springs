
class Point:
	def __init__(self, x, y, fixed=False):
		self.x = x
		self.y = y
		self.fixed = fixed
		self.springs = []
	def __str__(self):
		return '%s(%.3f, %.3f)' % ('F' if self.fixed else '', self.x, self.y)
	def __repr__(self):
		return self.__str__()

class Spring:
	def __init__(self, p1, p2, k):
		self.p1 = p1
		self.p2 = p2
		self.k = k
	def __str__(self):
		return '(%s, %s; k = %.3f)' % (self.p1, self.p2, self.k)
	def __repr__(self):
		return self.__str__()
		
class Model:
	def __init__(self, points, springs):
		self.points = points
		self.springs = springs
		
	def __str__(self):
		n = len(self.points)
		xs = [p.x for p in self.points]
		ys = [p.y for p in self.points]
		fixed_points = [i for p, i in zip(self.points, range(1, n + 1)) if p.fixed]
		points_text = '\n'.join(['%f %f' % (x, y) for x, y in zip(xs, ys)])
		springs_text = '\n'.join(['%d %d %f' % (spring.p1 + 1, spring.p2 + 1, spring.k) for spring in self.springs])
		fixeds_text = ' '.join(map(str, fixed_points))
		
		result = '%d\n%s\n%d\n%s\n%d\n%s' % (n, points_text, len(self.springs), springs_text, len(fixed_points), fixeds_text)
		return result
	def __repr__(self):
		return self.__str__()			

def read_model_from_file(filename):
	file = open(filename)
	return read_model(file.read())
	
def read_model(str):
	data = list(map(float, str.split()))
	n = int(data[0])

	pointData = data[1:2 * n + 1]
	points = []
	i = 0
	data_index = 0
	while i < len(pointData):
		x = pointData[i]
		y = pointData[i + 1]
		i += 2
		points.append(Point(x, y))
		
	m = int(data[2 * n + 1])
	springData = data[2 * n + 2 : 2 * n + 2 + 3 * m]
	springs = []
	i = 0
	while i < len(springData):
		a = int(springData[i]) - 1
		b = int(springData[i + 1]) - 1
		k = int(springData[i + 2])
		spring = Spring(a, b, k)
		springs.append(spring)
		points[a].springs.append(spring)
		points[b].springs.append(spring)
		i += 3
		
	k = int(data[2 * n + 2 + 3 * m])
	fixedData = data[2 * n + 2 + 3 * m + 1:]
	i = 0
	while i < len(fixedData):
		 fixedPoint = int(fixedData[i]) - 1
		 points[fixedPoint].fixed = True
		 i += 1
	
	return Model(points, springs)