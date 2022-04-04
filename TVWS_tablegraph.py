from audioop import avg
#import pyqtgraph as pg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import TVWS_process
import TVWS_tools1

def tableGraph(directory, filters):
    i = 0 #used to hold index
    data=[] #holds either table or bar data because graphs need an array inside an array to work
    moreFilters = ""
    table_data=[] # table graph data
    avgTotalCount=[]
    multipleDir=[]
    multipleDir.append(directory)
    morethan1dir = ""
    inpt = "" #holds avg total or count current value to test while loop.
    reply = ""

    filters.clear()
    print("Clearing Filters...")

    morethan1dir = input("Would you like to graph data from multiple directorys? (y/n): ").lower()
    if morethan1dir == 'y':
        while reply != "n":
            reply = input("Please enter a directory from which to take data from for graphing or type 'n' to continue: ")
            if reply != "n":
                multipleDir.append(reply)
                reply = ""
    
    while moreFilters != "n":
        moreFilters = input("Enter which filters to add to graph or 'n' to exit: ")
        if moreFilters != "n":
            while inpt not in ("avg","total","count"):
                inpt = input("Would you like to calculate the Average, Total, or individual Count for " + moreFilters + " (avg/total/count): ")
            avgTotalCount.append(inpt)
            inpt = ""
            filters.append(moreFilters)
            moreFilters = ""

    ans = input("Process files? No if already processed. (y/n): ")
    if ans.lower() == "y":
        if morethan1dir == "y":
            for dir in multipleDir:
                dir = multipleDir[i]
                TVWS_process.process(dir, filters, "", "", "")
                i = i + 1
            else:
                TVWS_process.process(directory, filters, "", "", "")

 
    for dir in multipleDir:
        i=0
        for filt in filters:
            filt = filters[i]
            aTC = avgTotalCount[i]
            if morethan1dir == "y":
                dir = multipleDir[i]
                table_data.append(TVWS_tools1.calc(aTC, filt, filters, dir, "1", "", ""))
            else:
                table_data.append(TVWS_tools1.calc(aTC, filt, filters, directory, "1", "", ""))
            print(table_data)
            i = i + 1

    data.append(table_data) # Tables require an array inside an array???
    if morethan1dir == "y":
        data.append(avgTotalCount + avgTotalCount)
    else:
        data.append(avgTotalCount)
    print(data)
    fig, ax = plt.subplots()
    if morethan1dir == "y":
        col = filters + filters
        the_table = ax.table(fontsize=40,cellText=data,colLabels=col, loc="center")
    else:
        the_table = ax.table(fontsize=40,cellText=data,colLabels=filters, loc="center")
    ax.axis('off')
    the_table.set_fontsize(20)
    plt.show()
    table_data.clear()
    data.clear()