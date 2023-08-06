# necessary imports
import math
import numpy as np

# define the constants
CONSTANTS = {
	'PI' : np.pi,
	'EXP': np.e,
	'EULER_GAMMA': np.euler_gamma
}

# invokes the function on given item(s)
def invoke_unary_function(func, item):
	if func == 'random':
		if type(item) != float:
			raise Exception("Invalid parameter {} for random function".format(item))
		if not item.is_integer():
			raise Exception("Invalid parameter {} for random function".format(item))
		if item < 1:
			raise Exception("Invalid parameter {} for random function".format(item))
		return np.random.rand(int(item))

	# take decision based on func
	if 	 func == 'sin':			return np.sin(item)
	elif func == 'cos':			return np.cos(item)
	elif func == 'tan':			return np.tan(item)
	elif func == 'arcsin':		return np.arcsin(item)
	elif func == 'arccos':		return np.arccos(item)
	elif func == 'arctan':		return np.arctan(item)
	elif func == 'sinh':		return np.sinh(item)
	elif func == 'cosh':		return np.cosh(item)
	elif func == 'tanh':		return np.tanh(item)
	elif func == 'arcsinh':		return np.arcsinh(item)
	elif func == 'arccosh':		return np.arccosh(item)
	elif func == 'arctanh':		return np.arctanh(item)
	elif func == 'degrees':		return np.degrees(item)
	elif func == 'radians':		return np.radians(item)
	elif func == 'deg2rad':		return np.deg2rad(item)
	elif func == 'rad2deg':		return np.rad2deg(item)
	elif func == 'floor':		return np.floor(item)
	elif func == 'ceil':		return np.ceil(item)
	elif func == 'trunc':		return np.trunc(item)
	elif func == 'round':		return np.round(item)
	elif func == 'negative':	return np.negative(item)
	elif func == 'absolute':	return np.absolute(item)
	elif func == 'exp':			return np.exp(item)
	elif func == 'exp2':		return np.exp2(item)
	elif func == 'log':			return np.log(item)
	elif func == 'log2':		return np.log2(item)
	elif func == 'log10':		return np.log10(item)
	elif func == 'expm1':		return np.expm1(item)
	elif func == 'log1p':		return np.log1p(item)
	elif func == 'sqrt':		return np.sqrt(item)
	elif func == 'square':		return np.square(item)
	elif func == 'reciprocal':	return np.reciprocal(item)
	else	:					raise Exception("Unknown function {}".format(func))



# invokes the binary function on given item(s)
def invoke_binary_function(func, item1, item2):
	# take decision based on func
	if 	 func == 'add':			return np.add(item1, item2)
	elif func == 'subtract':	return np.subtract(item1, item2)
	elif func == 'multiply':	return np.multiply(item1, item2)
	elif func == 'divide': 		return np.divide(item1, item2)
	elif func == 'floor_divide': return np.floor_divide(item1, item2)
	elif func == 'power':		return np.power(item1, item2)
	elif func == 'mod': 		return np.mod(item1, item2)
	elif func == 'logaddexp':	return np.logaddexp(item1, item2)
	elif func == 'logaddexp2':	return np.logaddexp2(item1, item2)
	elif func == 'gcd': 		return np.gcd(item1, item2)
	elif func == 'lcm': 		return np.lcm(item1, item2)
	elif func == 'arctan2': 	return np.arctan2(item1, item2)
	elif func == 'hypot': 		return np.hypot(item1, item2)
	elif func == 'bitwise_and': return np.bitwise_and(item1, item2)
	elif func == 'bitwise_or':	return np.bitwise_or(item1, item2)
	elif func == 'bitwise_xor': return np.bitwise_xor(item1, item2)
	elif func == 'left_shift': 	return np.left_shift(item1, item2)
	elif func == 'right_shift':	return np.right_shift(item1, item2)
	elif func == 'maximum': 	return np.maximum(item1, item2)
	elif func == 'minimum':		return np.minimum(item1, item2)
	else :	raise Exception("Unknown function {}".format(func))



# parses the constant
def parse_constant(value):
	if value in CONSTANTS:	return CONSTANTS[value]
	else	:	raise Exception("Unknown constant {}".format(value))


# evaluates the reuslt for (item1 op item2)
def evaluate_op(item1, op, item2):
	if 		op == '+':	return np.add(item1, item2)
	elif 	op == "-":	return np.subtract(item1, item2)
	elif 	op == "*":	return np.multiply(item1, item2)
	elif 	op == "/":	return np.divide(item1, item2)
	elif 	op == "%":	return np.mod(item1, item2)
	elif 	op == "^":	return np.power(item1, item2)
	else 	:			raise Exception("Invalid operator {}".format(op))
