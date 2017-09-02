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


def gen_lesson_plan(sched_csv, num_cycles, teacher, year):
    """
    Generates a LaTeX file from `_SCHED_TMPL` with the schedule data provided
    in `sched_csv`. Will print `num_cycles` repitions and print `teacher` and
    `year` on front page.
    """
    sdf = pd.read_csv(sched_csv, sep=',', header=[0,1], index_col=[0,1])
    sdf.index.names = ['Period', 'Item']
    sdf.columns.names = ['Week', 'Period']

    num_periods = sdf.index.levshape[0]
    weeks = ''.join(sdf.columns.levels[0])

    # strip seconds of start and end times
    for i in product(range(1, num_periods + 1), ['Start', 'End']):
        sdf.loc[i] = sdf.loc[i].map(lambda k: '' if pd.isnull(k) else k[:5] )

    # replace NaN by '' so the jinja templae can check for empty strings
    sdf.fillna('', inplace=True)

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

    print(tmpl.render(cycles=range(num_cycles), weeks=weeks,
                      sched=sched, teacher=teacher,
                      school_year=year))


def setup_parser(p):
    p.add_argument('--cycles', type=int, required=True, help="""number of
                   schedule cycles to print""")
    p.add_argument('--input', default='-', help="""csv file with schedule
                   data; will read from stdin in none specified""")
    p.add_argument('--teacher', default=None, required=True, help="""name of
                   teacher to be printed on front page""")
    p.add_argument('--year', default=None, required=True, help="""school year
                   (as string) to be printed on front page""")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    setup_parser(parser)
    args = parser.parse_args()
    gen_lesson_plan(sched_csv=args.input, num_cycles=args.cycles,
                    teacher=args.teacher, year=args.year)
