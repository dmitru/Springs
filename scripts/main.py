
from optparse import OptionParser
from datatypes import *
import plotter 
import solver
from sys import argv, exit
 
def read_model_from_file(filename):
	file = open(filename)
	return read_model(file.read())
	
if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-i', '--input', dest='input_file')
	parser.add_option('-o', '--output', dest='output_file', default='solution.txt')
	
	(options, args) = parser.parse_args()
	if len(args) != 0 or options.input_file is None:
		print('Usage: main.py -i | --input <input file> [-o | --output <output file>]')
		exit(1)	
		
	input_file = options.input_file
	try:
		model = read_model_from_file(input_file)
	except Exception as e:
		print(e)
		exit(1)
	
	print('Start solving the model...')
	solved_model = solver.solve(model)
	print('Done!')
	
	f = open(options.output_file, 'w')
	print('Writing model to file %s...' % options.output_file)
	print(str(solved_model), file=f)
	f.close()
	
	