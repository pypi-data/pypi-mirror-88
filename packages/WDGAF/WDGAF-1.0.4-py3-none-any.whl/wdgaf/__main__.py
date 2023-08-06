import sys
import os
import logging
import warnings
from pathlib import Path
from lark import Lark
import lark


sys.path.append(str(Path(__file__).parent))

from modules.process_tree import ProcessTree
from modules.fu_config import config

import wdgaf.gaf as gaf

import argparse


def main():
    # setup mechanism for any meta-requirements in the close future
    gaf.driver()

if __name__ == '__main__':
    main()
