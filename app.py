# import pandas lib as pd
import os
import pandas as pd
import re
from tabulate import tabulate
import html
import minify_html
from helper import survey_df, get_value, format_relevant, format_question, style

CODEBOOK_FILE_NAME = os.getenv('CODEBOOK_FILE_NAME')

table = []

p = re.compile('(select_one|select_multiple)\s+')

for index, row in survey_df.iterrows():
    type = str(row['type'])
    if type not in ['nan', 'end group']:

        table.append(["<b style='font-size: 1rem;'>{}</b>".format(format_question(row["label::English (en)"]))])
        table.append(['<div style="padding-left:20px; font-size: 0.9rem; color: #595959;">Name: <b>{}</b></div>'.format(row["name"])])
        table.append(['<div style="padding-left:20px; font-size: 0.9rem; color: #595959;">Question type: <b>{}</b></div>'.format(row["type"])])
        table.append(['<div style="padding-left:20px; font-size: 0.9rem; color: #595959;">Relevant: {}</div>'.format(format_relevant(row["relevant"]))])

        if p.match(type):
            choice_name = p.split(type)
            values = get_value(choice_name[1], choice_name[2])
            # table.append([str(row["name"]), str(row["relevant"]), str(row["label::English (en)"]), tabulate(values, tablefmt="html")])
            
            table.append(['<div style="padding-left:20px; font-size: 0.9rem; color: #595959;">Values: {}</div>'.format(tabulate(values, tablefmt="html"))])
        else:
            # table.append([str(row["name"]), str(row["relevant"]), str(row["label::English (en)"]), str(get_value(type))])
            table.append(['<div style="padding-left:20px; font-size: 0.9rem; color: #595959;">Values: {}</div>'.format(get_value(type))])
        
        table.append([""])


with open(CODEBOOK_FILE_NAME, "w") as f:
    final_html = "{}{}".format(style, tabulate(table, tablefmt='html'))
    f.write(minify_html.minify(html.unescape(final_html)))


