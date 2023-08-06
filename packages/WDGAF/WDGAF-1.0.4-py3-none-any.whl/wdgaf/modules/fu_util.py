# necessary imports
import numpy as np

# parses the size
def parse_size(rows=None, cols=None):
	# parse the number of rows
	if rows:
		try: rows = int(rows)
		except: raise Exception("Number of rows must be a positive integer but found {}".format(rows))
		if rows < 1:
			raise Exception("Number of rows must be a positive integer but found {}".format(rows))
	else: rows = 1

	# parse the number of columns
	if cols:
		try: cols = int(cols)
		except: raise Exception("Number of cols must be a positive integer but found {}".format(cols))
		if cols < 1:
			raise Exception("Number of cols must be a positive integer but found {}".format(cols))
	else: cols = 1

	# return the parsed rows and cols
	return (rows, cols)



# parses the given list - (string or real)
def parse_list(type, points):
	# stores the list items
	items = []
	# iterate through every point
	for point in points:	
		# if this is to be converted to string
		# drop out additional quotations
		try:
			items.append(float(point))
		except:
			val = str(point)
			val = val[1:-1]
			items.append(val)
	# return the list
	return np.array(items)



# creates the range with given jump
def create_range_with_jump(start, end, jump, isInt):
	# take decision based on jump
	if not jump:
		# get the boundary
		j = 1 if isInt else 0.01
		# jump is not provided so we create range
		# based on bounds with jumps to be 1
		if start <= end: return np.arange(start, end + j, j)
		else: return np.arange(start, end - j, -j)
	else:
		# get the boundary
		j = 1 if isInt and jump.is_integer() else 0.01
		# jump is provided so we take care of it
		if jump == 0: raise Exception("step must be non-zero for range")
		elif jump < 0:
			# check if bounds are valid
			if start < end: raise Exception("start should be at least end with step {}".format(jump))
			# construct and return the items
			return np.arange(start, end - j, jump)
		else:
			# check if bounds are valid
			if start > end: raise Exception("start should be at most end with step {}".format(jump)) 
			# construct and return the items
			return np.arange(start, end + j, jump)

# creates range with given values
def create_range(start=None, end=None, jump=None):
	if start is None: raise Exception("start must be provided for range")
	if end is None: raise Exception("end must be provided for range")
	if jump == 0: raise Exception("step must be non-zero for range")
	# check if both the bounds are integer
	if start.is_integer() and end.is_integer():
		# create a range with integral bounds
		return create_range_with_jump(start, end, jump, True)
	else:
		# create a range with real bounds
		return create_range_with_jump(start, end, jump, False)


