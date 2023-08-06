import logging
import copy

from ete3 import Tree
from collections import defaultdict

from parebrick.tree.tree_holder import TreeHolder

th = TreeHolder('((A,B),(C,D));', logging.getLogger())

th.count_innovations_fitch({'A': 0, 'B': 1, 'C': 0, 'D': 1})

th2 = copy.deepcopy(th)
th2.prune(['A', 'B'])

th2.draw('tree_test1.pdf', defaultdict(int))

th.draw('tree_test2.pdf', ['White', 'Green'])