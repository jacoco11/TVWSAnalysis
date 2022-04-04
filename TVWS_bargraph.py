from audioop import avg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import TVWS_process
import TVWS_tools1
import TVWS_tools2

def barGraph(directory, filters):
    bar_data=[] #bar graph data
    moreFilters = ""
    morethan1dir = "n"
    reply = ""
    avgTotalCount=[]
    inpt = "" #holds avg total or count current value to test while loop.
    i = 0 #holds array spot
    multipleDir=[]
    multipleDir.append(directory)

    filters.clear()
    print("Clearing Filters list...")

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
                bar_data.append(TVWS_tools1.calc(aTC, filt, filters, dir, "1", "", ""))
            else:
                bar_data.append(TVWS_tools1.calc(aTC, filt, filters, directory, "1", "", ""))
            print(bar_data)
            i = i + 1

    xaxis = [','.join(pair) for pair in zip(filters,avgTotalCount)]
    if morethan1dir == "y":
        xaxis = xaxis + xaxis
    plt.bar(xaxis,bar_data)
    plt.title("Generic Bar Graph")
    plt.xlabel("Inputted fields")
    plt.show()
    plt.savefig("GenericBarGraph.png")
    bar_data.clear()
    avgTotalCount.clear()
    multipleDir.clear()