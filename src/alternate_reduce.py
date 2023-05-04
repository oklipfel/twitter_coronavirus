#!/usr/bin/env python3

import matplotlib
import numpy as np
import json
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
from collections import Counter, defaultdict
from glob import glob

# command args
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', required=True)
parser.add_argument('--keys', nargs='+', required=True)
args = parser.parse_args()
input_files = glob(args.input_dir + '/*')

for key in args.keys:
    y_axis = []
    total = defaultdict(lambda: Counter())

    for path in sorted(input_files):
        with open(path) as f:
            tmp = json.load(f)
            sumofnum = 0
            try:
                for k in tmp[key]:
                    sumofnum += tmp[key][k]
            except:
                pass
            y_axis.append(sumofnum)
    plt.plot(np.arange(len(y_axis)), y_axis, label=key)
plt.xlabel("Date")
plt.ylabel("Vol. of Tweets")
plt.legend()
plt.savefig("alternate_red_plot.png",bbox_inches="tight")
