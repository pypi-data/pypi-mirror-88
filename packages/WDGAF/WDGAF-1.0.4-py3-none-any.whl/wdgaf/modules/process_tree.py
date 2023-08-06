# necessary imports
from lark import Transformer, v_args
import matplotlib.pyplot as plt
import numpy as np

# custom modules
import modules.fu_math as fmath
import modules.fu_plot as fplot
import modules.fu_util as futil
from modules.fu_config import config
from modules.fu_keywords import KEYWORDS

# handles the evaluation using aliases
@v_args(inline=True)
class ProcessTree(Transformer):

	# creates subplots with given values
	def create_subplots(self, rows, cols, attr_list=None):
		self.rows = rows
		self.cols = cols
		self.grid = np.zeros((rows, cols))
		plt.close('all') # important before subplots
		self.fig, self.ax = fplot.subplots(rows, cols, attr_list)

	# constructor
	def __init__(self):
		# start with 1x1 grid
		self.create_subplots(1, 1)
		# start with an empty list of variables
		self.vars = {}



	########################### FIGURE STMT ###########
	# figure statement alias
	# stmt_list is irrelevant here
	# because all statements are processed separately
	def figure_stmt(self, fig_id=None, *stmt_list):
		# fig_id must be provided
		if not fig_id:	raise Exception("FigureId must be provided")
		# generate verbose message
		if config['verbose']: print("figId := {}".format(fig_id))
		# update the title
		self.fig.suptitle("[{}]".format(fig_id))
		# display the plots
		plt.tight_layout()
		plt.legend()
		plt.show()

		# reset-params
		self.create_subplots(1, 1)
		# clear all variables
		self.vars = {}



	########################### SIZE STMT ###########
	# size_row_stmt alias 
	def size_row_stmt(self, rows=None, attr_list=None):
		# parse the rows and cols
		rows, cols = futil.parse_size(rows, None)
		# create subplots
		self.create_subplots(rows, cols, attr_list)
		# generate verbose message
		if config['verbose']:
			print("rows := {}, cols := {}, attr_list := {}".format(rows, 1, attr_list))

	# size_row_col_stmt alias 
	def size_row_col_stmt(self, rows=None, 
							cols=None, attr_list=None):
		# parse the rows and cols
		rows, cols = futil.parse_size(rows, cols)
		# create subplots
		self.create_subplots(rows, cols, attr_list)
		# generate verbose message
		if config['verbose']:
			print("rows := {}, cols := {}, attr_list := {}".format(rows, cols, attr_list))



	########################### EXPRESSIONS ###########
	# expr_alias
	def expr(self, value):
		# grab and return the expression
		return value

	# expr_real alias
	def expr_real(self, number):
		# return the number
		return float(number)

	# expr_const alias
	def expr_const(self, const_item):
		# return the value of the constant
		return fmath.parse_constant(const_item)

	# expr_negation alias
	def expr_negation(self, value):
		# return the negation of expression
		return -1.0 * value
	# expr_positive alias
	def expr_positive(self, value):
		# return the value of expression
		return value

	# nested_expr alias
	def nested_expr(self, value):
		# return the value
		return value

	# expr_id alias
	def expr_id(self, var_id):
		# get the string representation from Token
		var_id = str(var_id)
		# check if this is a constant
		if var_id in fmath.CONSTANTS: return fmath.CONSTANTS[var_id]
		# check if value exist
		if var_id not in self.vars:	raise Exception("Unknown parameter {}".format(var_id))
		# fetch the list of values for this variable
		items = self.vars[var_id]
		# return the values
		return items

	# grab and apply appropriate operation
	def sum_expr(self, expr1, expr2):
		return np.add(expr1, expr2)
	def sub_expr(self, expr1, expr2):
		return np.subtract(expr1, expr2)
	def prd_expr(self, expr1, expr2):
		return np.multiply(expr1, expr2)
	def div_expr(self, expr1, expr2):
		return np.divide(expr1, expr2)
	def floor_div_expr(self, expr1, expr2):
		return np.floor_divide(expr1, expr2)
	def mod_expr(self, expr1, expr2):
		return np.mod(expr1, expr2)
	def exp_expr(self, expr1, expr2):
		return np.power(expr1, expr2)




	########################### RANGE STMT ###########
	# real_points_list alias 
	def real_points_list(self, *points):
		# parse and return the list
		return futil.parse_list(float, points)

	# str_points_list alias 
	def str_points_list(self, *points):
		# parse and return the list
		return futil.parse_list(str, points)

	# range_expr alias
	def range_expr(self, start=None, end=None, step=None):
		# create a range with give bounds
		return futil.create_range(start, end, step)

	# range_stmt alias
	def range_stmt(self, var_id, items=[]):
		# get the string representation from Token
		var_id = str(var_id)
		# add this variable
		self.vars[var_id] = items
		# generate verbose message
		if config['verbose']: print("{} := {}".format(var_id, items))
		# return the tuple containing var_id, items
		return (var_id, items)







	########################### FUNCTION STMT ###########
	# func_call_unary alias 
	def func_call_unary(self, func_name, item):
		# invoke the given function 
		return fmath.invoke_unary_function(func_name, item)

	# func_call_binary alias 
	def func_call_binary(self, func_name, item1, item2):
		# invoke the given function 
		return fmath.invoke_binary_function(func_name, item1, item2)

	# nested_func alias
	def nested_func(self, expression):
		# return the expression
		return expression

	# func_op_func alias
	def func_op_func(self, item1, op, item2=None):
		# evaluate the expression
		return fmath.evaluate_op(item1, op, item2)

	# fun_stmt alias
	def func_stmt(self, var_id, items):
		# get the string representation from Token
		var_id = str(var_id)
		# assign the values to the variable
		self.vars[var_id] = items
		# generate verbose message
		if config['verbose']: print("{} := {}".format(var_id, items))



	########################### PLOTTING ###########
	# print_stmt alias
	def print_stmt(self, *var_ids):
		# iterate through all variables
		for var_id in var_ids:
			# get the string representation from Token
			var_id = str(var_id)
			if var_id in self.vars:
				print("{} = {}".format(var_id, self.vars[var_id]))
			else:
				raise Exception("Unknown parameter {}".format(var_id))


	# plt_stmt alias	
	def plt_stmt(self, x_id, y_id, *attr_list):
		# get the string representation from Token
		x_id = str(x_id)
		y_id = str(y_id)
		# validate values
		if x_id not in self.vars:	raise Exception("Unknown parameter {}".format(x_id))
		if y_id not in self.vars:	raise Exception("Unknown parameter {}".format(y_id))
		# fetch values
		xs = self.vars[x_id]
		ys = self.vars[y_id]
		props = {}
		for item in attr_list: props = item
		fplot.create_plot(self.ax, self.grid, xs, ys, None, props, category='plot')


	########################### CONTOUR ###########
	def contour_grid(self, id_x, id_y, startx, endx, starty, endy):
		startx = float(startx)
		starty = float(starty)
		endx = float(endx)
		endy = float(endy)
		if startx > endx: raise Exception("startx must be at least endx for countour")
		if starty > endy: raise Exception("starty must be at least endy for countour")
		x = np.arange(startx, endx, 0.01)
		y = np.arange(starty, endy, 0.01)
		X, Y = np.meshgrid(x, y)
		self.vars[id_x] = X
		self.vars[id_y] = Y
		# generate verbose message
		if config['verbose']: print("{} := {}\n {} := {}".format(id_x, X, id_y, Y))

	def contour_stmt(self, x_id, y_id, items, *attr_list):
		# get the string representation from Token
		x_id = str(x_id)
		y_id = str(y_id)
		# validate values
		if x_id not in self.vars:	raise Exception("Unknown parameter {}".format(x_id))
		if y_id not in self.vars:	raise Exception("Unknown parameter {}".format(y_id))
		# fetch values
		xs = self.vars[x_id]
		ys = self.vars[y_id]
		props = {}
		for item in attr_list: props = item
		fplot.create_plot(self.ax, self.grid, xs, ys, items, props, category='contour')
		# generate verbose message
		if config['verbose']: print("eqn := {}".format(items))



	########################### OPERATOR ###########
	# grabs and returns the operator
	def operator(self, op):
		return op


	########################### ATTR LIST ###########
	# grabs and returns the attr_list
	def attr_list(self, *attrs):
		return dict(attrs)

	# grabs and returns the attribute
	def attribute(self, key, value):
		key, value = str(key), str(value)
		try: return (key, float(value))
		except: return (key, value[1:-1])



	########################### IDETIFIERS ###########
	# grabs the identifier and validate it
	def identifier(self, var_id):
		# check if this variable is a keyword
		if var_id in KEYWORDS:
			raise Exception("Illegal use of reserved word {}".format(var_id))
		# return the variable id
		return var_id

