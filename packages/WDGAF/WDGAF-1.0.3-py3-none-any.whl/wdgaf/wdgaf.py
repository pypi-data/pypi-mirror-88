# necessary imports
import sys
import os
import logging
import warnings
from pathlib import Path
from lark import Lark
import lark
from modules.process_tree import ProcessTree
from modules.fu_config import config
import argparse

# driver function
def driver():
	# set level to critical
	logging.getLogger().setLevel(logging.CRITICAL)
	warnings.filterwarnings('ignore')

	# Import grammar and create parser
	grammar = Path('./grammar/grammar.lark')
	assert(grammar.is_file())
	with open(grammar,'r') as f: raw_grammar = f.read()
	# create the parser instance 
	parser = Lark(raw_grammar, parser="lalr", transformer=ProcessTree())

	# create argument parser
	args_parser = argparse.ArgumentParser(description='Interpreter for WDGAF language', epilog="And that's how you use the interepreter")
	args_parser.add_argument('src', metavar='src', help='source file path')
	args_parser.add_argument('-v', '--verbose', help="generates verbose output", action="store_true")

	# get the arguments
	args = args_parser.parse_args()

	# configure verbose parametere here!
	# this is used in all other modules!
	config['verbose'] = args.verbose

	# check if source file is provided
	if args.src: source = Path(args.src)
	else: print("Usage:\npython wdgaf.py <filename>"); sys.exit();

	# assert that file exist and it's *.fu file
	assert(source.is_file() and source.suffix == '.fu')
	# read the source file
	with open(source,'r') as f: code_raw = f.read()

	# execute user code
	try:
		parser.parse(code_raw)

	# catch syntax errors
	except lark.exceptions.UnexpectedToken as e:
		token = e.token
		print("\033[91mSytnax Error: \033[00m", end='')
		print("unexpected token '{}' at line {}, column {}".format(token, token.line, token.column))
		print("process terminated")

	# these exceptions will generally be well-defined
	except Exception as ex:
		print("\033[91mError: \033[00m", end='')
		print(ex)
		print("process terminated")


# invoke the driver function
if __name__ == '__main__':
    driver()
