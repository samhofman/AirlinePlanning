# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:50:32 2019

@author: woute
"""

import numpy as np
import matplotlib.pyplot as plt
import openpyxl as xl

plt.rcParams.update({'font.size': 18})
plt.rcParams.update({'font.weight': 'normal'})

### READ RESULTS ######################################################

wb = xl.load_workbook("RESULTS.xlsx", read_only=True)
S1 = wb['RESULTS']

results = np.array([[int(i.value) for i in j] for j in S1['F1':'I18']])

#######################################################################
iterations = []
objective  = []
columns    = []
rows       = []
columns_no = []
row_no = []


for i in range(len(results)):
    iterations.append(results[i][0])  
    objective.append(results[i][1])
    columns.append(results[i][2])
    rows.append(results[i][3])
    



#men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
#women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
#
#ind = np.arange(len(columns))  # the x locations for the groups
#width = 0.35  # the width of the bars
#
#fig, ax = plt.subplots()
#rects1 = ax.bar(ind - width/2, columns, width, #yerr=men_std,
#                color='SkyBlue', label='Columns')
#rects2 = ax.bar(ind + width/2, rows, width, #yerr=women_std,
#                color='IndianRed', label='Rows')
#
## Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('Amount')
#ax.set_title('Amount of additions per iteration')
#ax.set_xticks(ind)
#ax.set_xticklabels(iterations)
#ax.legend()
#
#
#def autolabel(rects, xpos='center'):
#    """
#    Attach a text label above each bar in *rects*, displaying its height.
#
#    *xpos* indicates which side to place the text w.r.t. the center of
#    the bar. It can be one of the following {'center', 'right', 'left'}.
#    """
#
#    xpos = xpos.lower()  # normalize the case of the parameter
#    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
#    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
#
#    for rect in rects:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
#                '{}'.format(height), ha=ha[xpos], va='bottom')
#
#
#autolabel(rects1, "left")
#autolabel(rects2, "right")
#
#plt.show()



plt.clf()

# using some dummy data for this example
xs = iterations
ys = objective

# 'bo-' means blue color, round points, solid lines
plt.plot(iterations,objective,'bo-')

# zip joins x and y coordinates in pairs
for x,y in zip(iterations,objective):

    label = "{:.5f}".format(y)

    plt.annotate([columns[x], rows[x]], # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='right') # horizontal alignment can be left, right or center

plt.xticks(iterations)
#plt.yticks(objective)
plt.yticks((3123402, 3408769),('$3123402','$3408769'))
#ax.yaxis.label.set_size(20)

plt.xlabel('Iterations')
plt.ylabel('Objective Value')


plt.show()











