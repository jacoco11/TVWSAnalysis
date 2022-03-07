import os
import csv
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np


# Function for data visualization on processed data
def graph(directory, graph, filters):
    # Graph data points
    if graph != None:
        check2 = True
        while check2:
            value1 = input("Enter field 1: ")
            value2 = input("Enter field 2: ")
            if value1 in filters and value2 in filters:
                check2 = False
            elif value1 == "exit" or value2 == "exit":
                check2 = False
            else:
                print("Invalid field(s), re-enter. ")
        indx1 = int(filters.index(value1))
        indx2 = int(filters.index(value2))

        if graph == "plot":
            print()

        elif graph == "scatter":
            print()

        elif graph == "bar":
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.bar(value1,value2)
            plt.show()
            print()

    else:
        print("No graph type selected. ")
