#!/usr/bin/env python
"""
Generates a LaTeX file with a teacher's lesson planner book for multiple
week schedule cycles, prefilled with schedule data read from a csv file.
"""

from __future__ import division, print_function

import os
from itertools import product
import argparse
import pandas as pd
import jinja2 as j2

_SCHED_TMPL = 'lesson_planner.jinja'


def gen_lesson_plan(args):
    """
    Generates a LaTeX file from `_SCHED_TMPL` with the schedule data provided
    in `args.input`
    """
    sdf = pd.read_csv(args.input, sep=',', header=[0,1], index_col=[0,1])
    sdf.index.names = ['Period', 'Item']
    sdf.columns.names = ['Week', 'Period']

    num_periods = sdf.index.levshape[0]
    weeks = ''.join(sdf.columns.levels[0])

    # strip seconds of start and end times
    for i in product(range(1, num_periods + 1), ['Start', 'End']):
        sdf.loc[i] = sdf.loc[i].map(lambda k: k[:5])

    sched = {}
    for wk in weeks:
        sched[wk] = [sdf[wk].loc[i].to_dict()
                     for i in range(1, num_periods + 1)]

    tmplLoader = j2.FileSystemLoader(searchpath=os.getcwd())
    tmplEnv = j2.Environment(
            loader=tmplLoader,
            trim_blocks=True,
            block_start_string='<%',
            block_end_string='%>',
            variable_start_string='<&',
            variable_end_string='&>',
            comment_start_string='<#',
            comment_end_string='#>')

    tmpl = tmplEnv.get_template(_SCHED_TMPL)

    with open(args.output, 'w') as foo:
        foo.write(tmpl.render(cycles=range(args.cycles), weeks=weeks,
                              sched=sched, teacher=args.teacher,
                              school_year=args.year))


def setup_parser(p):
    p.add_argument('--cycles', type=int, required=True, help="""number of
                   schedule cycles to print""")
    p.add_argument('--input', default=None, required=True, help="""csv file
                   with schedule data""")
    p.add_argument('--output', default=None, required=True, help="""LaTeX
                   output file to be generated""")
    p.add_argument('--teacher', default=None, required=True, help="""name of
                   teacher to be printed on front page""")
    p.add_argument('--year', default=None, required=True, help="""school year
                   (as string) to be printed on front page""")


if __name__ == '__main__':

    print(__doc__)

    parser = argparse.ArgumentParser(description=__doc__)
    setup_parser(parser)
    args = parser.parse_args()
    gen_lesson_plan(args)
