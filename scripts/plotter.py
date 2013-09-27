
from datatypes import *
import matplotlib.pyplot as plt
from optparse import OptionParser

def plot_model(model):
	xs = [p.x for p in model.points]
	ys = [p.y for p in model.points]
	sizes = [80 if p.fixed else 50 for p in model.points]
	colors = ['black' if p.fixed else 'grey' for p in model.points]
	plt.axis([min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1])
	plt.scatter(xs, ys, s=sizes, color=colors)
	
	for spring in model.springs:
		p1 = model.points[spring.p1]
		p2 = model.points[spring.p2]
		plt.plot([p1.x, p2.x], [p1.y, p2.y], color='black', linestyle='-', linewidth=1.5, zorder=-1)
		
def show():
	plt.show()
	
def save_as(file_name):
	fig = plt.gcf()
	fig.set_size_inches(18.5,10.5)
	plt.savefig(file_name, dpi=200)

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-i', '--input', dest='input_file')
	parser.add_option('-o', '--output', dest='output_file', default='plot.png')
	
	(options, args) = parser.parse_args()
	if len(args) != 0 or options.input_file is None:
		print('Usage: plotter.py -i | --input <input file> [-o | --output <output file>]')
		exit(1)	
		
	input_file = options.input_file
	try:
		model = read_model_from_file(input_file)
	except Exception as e:
		print(e)
		exit(1)
	
	plot_model(model)
	
	output_file = options.output_file
	save_as(output_file)
