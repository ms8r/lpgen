import os
from itertools import product
import pandas as pd
import jinja2 as j2

sdf = pd.read_csv('schedule.csv', sep=',', header=[0,1], index_col=[0,1])
sdf.index.names = ['Period', 'Item']
sdf.columns.names = ['Week', 'Period']

for i in product(range(1, 7), ['Start', 'End']):
    sdf.loc[i] = sdf.loc[i].map(lambda k: k[:5])

sched = {}
for wk in 'AB':
    sched[wk] = [sdf[wk].loc[i].to_dict() for i in range(1, 7)]

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

tmpl = tmplEnv.get_template('lesson_planner.jinja')

with open('sched.tex', 'w') as foo:
    foo.write(tmpl.render(cycles=range(3), weeks='AB', sched=sched,
                          teacher='Ms. Slavinski', school_year='2015/2016'))
