#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--keys',nargs='+',required=True)
args = parser.parse_args()

import os
import glob
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# load each of the input paths
total = defaultdict(lambda: Counter())
for path in glob.glob('outputs/geoTwitter*.lang'):
    with open(path) as f:
        tmp = json.load(f)
        filename = os.path.basename(path)
        date = filename[10:18]
        total[date] = tmp

new_dict = {}

for day in total.keys():
    for key in args.keys:
        if key not in new_dict:
            new_dict[key] = {}
        if day not in new_dict[key]:
            new_dict[key][day] = 0
        try:
            for lang in total[day][key].values():
                new_dict[key][day] += lang
        except KeyError:
            pass

fig, ax = plt.subplots()
for key in new_dict:
    dates = sorted(new_dict[key].keys())
    values = [new_dict[key][date] for date in dates]
    days = [datetime.strptime(date, '%y-%m-%d') for date in dates]
    ax.plot(days, values, label=key)

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))

# Add title and axis labels
ax.set_xlabel('Date')
ax.set_ylabel('Tweet Volume')
ax.legend()

tags = []
for key in args.keys:
    tags.append(key[1:])

plt.savefig('_'.join(tags)+'.png')
