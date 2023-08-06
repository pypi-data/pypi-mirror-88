# necessary imports
from matplotlib.colors import is_color_like
import matplotlib.pyplot as plt
import matplotlib
from modules.fu_config import size_attrs, plot_attrs

# parses the boolean string
def parse_bool(text):
	return (text.lower() == 'true')

# raises exception for illegal attributes
def raise_illegal_attribute_error(attr, value):
	raise Exception("Illegal attribute value {} for attribute {}".format(value, attr))

# creates the subplots and returns the items
def subplots(rows, cols, attr_list=None):
	if attr_list == None:
		# create subplots and return items
		return plt.subplots(rows, cols, 
					num="We Do Give A Figure")


	# make sure all the supplied attributes
	# are currently supported
	for key in attr_list.keys():
		if key not in size_attrs:
			raise Exception("Illegal attribute {} for size-statement".format(key))

	# parse the attributes one by one
	sharex = attr_list.get('sharex', 'none')
	if sharex not in ['true', 'false']:
		raise_illegal_attribute_error('sharex', sharex)

	sharey = attr_list.get('sharey', 'none')
	if sharey not in ['true', 'false']:
		raise_illegal_attribute_error('sharey', sharey)

	width = attr_list.get('width', 6.4)
	if type(width) != float or width <= 0:
		raise_illegal_attribute_error('width', width)
	height = attr_list.get('height', 4.8)
	if type(height) != float or width <= 0:
		raise_illegal_attribute_error('height', height)

	facecolor = attr_list.get('facecolor', 'white')
	if not is_color_like(facecolor):
		raise_illegal_attribute_error('facecolor', facecolor)
	edgecolor = attr_list.get('edgecolor', 'white')
	if not is_color_like(facecolor):
		raise_illegal_attribute_error('edgecolor', edgecolor)


	linewidth = attr_list.get('linewidth', 0.8)
	if type(linewidth) != float or linewidth < 0:
		raise_illegal_attribute_error('linewidth', linewidth)

	# create subplots and return items
	return plt.subplots(rows, cols, 
					num="We Do Give A Figure",
					sharex=parse_bool(sharex), 
					sharey=parse_bool(sharey),
					figsize=(width, height),
					facecolor=facecolor,
					edgecolor=edgecolor,
					linewidth=linewidth)


# returns the first empty-cell (if any otherwise last cell)
# index returned are 1-based
def first_empty_cell(grid, start_row=0, start_col=0):
	# get the number of rows and cols
	rows, cols = grid.shape
	# iterate through all cells
	for i in range(start_row, rows):
		for j in range(start_col, cols):
			# check if this satisify the criteria
			if grid[i][j] == 0:
				return (i + 1, j + 1)
	# return the last cell
	return (rows, cols)



# configures the additional arguments for plot
def configure_plot(ax, props):
	# parse the attributes one by one
	title = props.get('title', None)
	x_label = props.get('xlabel', None)
	y_label = props.get('ylabel', None)

	# parse the scales
	xscale = props.get('xscale', 'linear')
	if xscale not in ['linear', 'log', 'symlog', 'logit']:
		raise_illegal_attribute_error('xscale', xscale)
	yscale = props.get('yscale', 'linear')
	if yscale not in ['linear', 'log', 'symlog', 'logit']:
		raise_illegal_attribute_error('yscale', yscale)

	# parse the margins
	xmargin = props.get('xmargin', 0.1)
	if xmargin <= -0.5:
		raise_illegal_attribute_error('xmargin', xmargin)
	ymargin = props.get('ymargin', 0.1)
	if ymargin <= -0.5:
		raise_illegal_attribute_error('ymargin', ymargin)

	# scales
	xautoscale = props.get('xautoscale', 'true')
	if xautoscale not in ['true', 'false']:
		raise_illegal_attribute_error('xautoscale', xautoscale)
	yautoscale = props.get('yautoscale', 'true')
	if yautoscale not in ['true', 'false']:
		raise_illegal_attribute_error('yautoscale', yautoscale)

	# rotations
	xrotation = props.get('xrotation', 0.0)
	yrotation = props.get('yrotation', 0.0)

	# ticks on axis
	xmajorticks = props.get('xmajorticks', 'true')
	if xmajorticks not in ['true', 'false']:
		raise_illegal_attribute_error('xmajorticks', xmajorticks)
	ymajorticks = props.get('ymajorticks', 'true')
	if ymajorticks not in ['true', 'false']:
		raise_illegal_attribute_error('ymajorticks', ymajorticks)
	xminorticks = props.get('xminorticks', 'true')
	if xminorticks not in ['true', 'false']:
		raise_illegal_attribute_error('xminorticks', xminorticks)
	yminorticks = props.get('yminorticks', 'true')
	if yminorticks not in ['true', 'false']:
		raise_illegal_attribute_error('yminorticks', yminorticks)
	xticklabel = props.get('xticklabel', 'true')
	if xticklabel not in ['true', 'false']:
		raise_illegal_attribute_error('xticklabel', xticklabel)
	yticklabel = props.get('yticklabel', 'true')
	if yticklabel not in ['true', 'false']:
		raise_illegal_attribute_error('yticklabel', yticklabel)

	# gridlines
	gridlines = props.get('gridlines', 'false')
	if gridlines not in ['true', 'false']:
		raise_illegal_attribute_error('gridlines', gridlines)


	# fetch the facecolor
	facecolor = props.get('facecolor', 'white')
	if not is_color_like(facecolor): 
		raise_illegal_attribute_error('facecolor', facecolor)

	# set the properties
	ax.set_title(title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	ax.set_xscale(xscale)
	ax.set_yscale(yscale)
	ax.set_xmargin(xmargin)
	ax.set_ymargin(ymargin)
	ax.set_autoscalex_on(parse_bool(xautoscale))
	ax.set_autoscaley_on(parse_bool(yautoscale))
	ax.tick_params(axis='x',rotation=xrotation)
	ax.tick_params(axis='x',which='major', bottom=parse_bool(xmajorticks))
	ax.tick_params(axis='x',which='minor', bottom=parse_bool(xminorticks))
	ax.tick_params(axis='x',labelbottom=parse_bool(xticklabel))
	ax.tick_params(axis='y',rotation=yrotation)
	ax.tick_params(axis='y',which='major', left=parse_bool(ymajorticks))
	ax.tick_params(axis='y',which='minor', left=parse_bool(yminorticks))
	ax.tick_params(axis='y',labelleft=parse_bool(yticklabel))
	ax.set_facecolor(facecolor)
	if parse_bool(gridlines): ax.grid()

# creates a plot with given values on given axes
def plot(xs, ys, zs, ax, props, category):
	# if no configuration is provided 
	# then use the default ones
	if props == None:
		if zs is not None: ax.contour(xs, ys, zs, [0])
		else:  ax.plot(xs, ys)

	# make sure all the supplied attributes
	# are currently supported
	for key in props.keys():
		if key not in plot_attrs:
			raise Exception("Illegal attribute {} for plot-statement".format(key))


	# take decision based on plot type
	if category == 'plot':
		# validate the additional parameters
		if 'level' in props: raise Exception("Illegal attribute level for plot-statement")
		# get the label for the plot
		label = props.get('label', None)
		# get the color
		color = props.get('color', None)
		if color != None and not is_color_like(color):
			raise_illegal_attribute_error('color', color)
		linestyle = props.get('linestyle', '-')
		if linestyle  not in ['-', '--', '-.', ':']:
			raise_illegal_attribute_error('linestyle', linestyle)
		linewidth = props.get('linewidth', 1.5)
		if linewidth <= 0.0:
			raise_illegal_attribute_error('linewidth', linewidth)
		fillstyle = props.get('fillstyle', 'full')
		if fillstyle  not in ['full', 'left', 'right', 'bottom', 'top', 'none']:
			raise_illegal_attribute_error('fillstyle', fillstyle)
		alpha = props.get('alpha', 1.0)
		if alpha < 0.0 or alpha > 1.0:
			raise raise_illegal_attribute_error('alpha', alpha)

		dashcapstyle = props.get('dashcapstyle', 'butt')
		if dashcapstyle not in ['butt', 'round', 'projecting']:
			raise_illegal_attribute_error('dashcapstyle', dashcapstyle)
		dashjoinstyle = props.get('dashjoinstyle', 'round')
		if dashjoinstyle not in ['miter', 'round', 'bevel']:
			raise_illegal_attribute_error('dashjoinstyle', dashjoinstyle)
		solidcapstyle = props.get('solidcapstyle', 'butt')
		if solidcapstyle not in ['butt', 'round', 'projecting']:
			raise_illegal_attribute_error('solidcapstyle', solidcapstyle)
		solidjoinstyle = props.get('solidjoinstyle', 'round')
		if solidjoinstyle not in ['miter', 'round', 'bevel']:
			raise_illegal_attribute_error('solidjoinstyle', solidjoinstyle)

		drawstyle = props.get('drawstyle', 'default')
		if drawstyle not in ['default', 'steps', 'steps-pre', 'steps-mid', 'steps-post']:
			raise raise_illegal_attribute_error('drawstyle', drawstyle)

		marker = props.get('marker', None)
		if marker and marker not in [".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_"]:
			raise_illegal_attribute_error('marker', marker)

		markeredgecolor = props.get('markeredgecolor', 'white')
		if not is_color_like(markeredgecolor):
			raise_illegal_attribute_error('markeredgecolor', markeredgecolor)
		markeredgewidth = props.get('markeredgewidth', 1.0)
		if markeredgewidth < 0.0:
			raise_illegal_attribute_error('markeredgewidth', markeredgewidth)
		markerfacecolor = props.get('markerfacecolor', 'white')
		if not is_color_like(markerfacecolor):
			raise_illegal_attribute_error('markerfacecolor', markerfacecolor)
		markersize = props.get('markersize', 6.0)
		if markersize < 0.0:
			raise_illegal_attribute_error('markersize', markersize)

		# create plot
		ax.plot(xs, ys, label=label, color=color, 
						linestyle=linestyle, linewidth=linewidth,
						fillstyle=fillstyle, alpha=alpha,
						dash_capstyle=dashcapstyle, dash_joinstyle=dashjoinstyle, 
						solid_capstyle=solidcapstyle, solid_joinstyle=solidjoinstyle, 
						drawstyle=drawstyle,
						marker=marker, markersize=markersize,
						markeredgecolor=markeredgecolor,
						markerfacecolor=markerfacecolor,
						markeredgewidth=markeredgewidth
				)
		# ax.plot(xs, ys)

	# contour plot
	elif category == 'contour':
		# validate the additional parameters
		if 'color' in props: raise Exception("Illegal attribute color for contour-statement")
		if 'label' in props: raise Exception("Illegal attribute label for contour-statement")
		# get the level	
		level = props.get('level', 'single')
		if level not in ['single', 'multiple']:
			raise_illegal_attribute_error('level', level)
		# plot the contour
		if level == "multiple": ax.contour(xs, ys, zs)
		else:	ax.contour(xs, ys, zs, [0])

	# configure the axis
	configure_plot(ax, props)




# creates the plot for the user
def create_plot(ax, grid, xs, ys, zs=None, attr_list=None, category=None):
	# fetch the number or rows and cols
	rows, cols = grid.shape
	# fetch the first non-empty cell
	def_row, def_col = first_empty_cell(grid)
	# fetch the index to plot
	row = attr_list.get('row', None)
	col = attr_list.get('col', None)
	# parse to integers
	if row != None:	row = int(row)
	if col != None: col = int(col)


	# if neither row nor col are provided we scan entire grid
	if row == None and col == None:
		# default ends to last cell
		row = rows; col = cols; found = False;
		# iterate through all cells
		for i in range(rows):
			for j in range(cols):
				if grid[i][j] == 0: col = j + 1; found=True; break;
			if found: row = i + 1; break;


	# if column but not row is provided we scan row
	elif row == None and col != None:		
		# check if column is valid
		if col < 1 or col > cols: 
			raise Exception("Column index out of range")
		# default ends to last row
		row = rows
		# iterate through all rows in this col
		for i in range(rows):
			if grid[i][col - 1] == 0: row = i + 1; break;


	# if row but not col is provided we scan col
	elif row != None and col == None:
		# check if row is valid		
		if row < 1 or row > rows: 
			raise Exception("Row index out of range")
		# default ends to last col
		col = cols
		# iterate through all cols in this row
		for j in range(cols):
			if grid[row - 1][j] == 0: col = j + 1; break;

	# check bounds
	if row < 1 or row > rows: raise Exception("Row index out of range")
	if col < 1 or col > cols: raise Exception("Column index out of range")

	# find appropriate indexing
	if rows == 1 and cols == 1:
		# axis cannot be subscript
		plot(xs, ys, zs, ax, attr_list, category)
	elif rows == 1 or cols == 1:
		# axis can be subscript using one index
		plot(xs, ys, zs, ax[row * col - 1], attr_list, category)
	else:
		# axis can be subscript using both index
		plot(xs, ys, zs, ax[row - 1][col - 1], attr_list, category)

	# occupy this location
	grid[row - 1][col - 1] = 1.0

