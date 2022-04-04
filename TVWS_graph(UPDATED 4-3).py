import os
import csv
import subprocess
from  matplotlib import pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import math


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
            #Creates the figure.
            plt.figure()

            #Initializes the axis.
            xaxis = []
            yaxis = []

            #Goes through the directory.
            for file in os.listdir(directory):
                #Finds files that end in .csv
                if file.endswith(".csv"):
                    #Opens the csv files.
                    with open(os.path.join(directory, file)) as f:

                        csv_reader = csv.reader(f, delimiter=',')

                        #Gets each x axis element for the corresponding y axis.
                        proc = subprocess.Popen("awk -F \",\" \"{a[$1]+=$2;b[$1]++}END{for(i \"in\" \"a){print\" i,a[i]/b[i]}}\" "+ os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                        temp1 = str(proc.communicate()[0].decode('ascii'))
                        temp2 = temp1.split('\r\n')
                        for i in temp2:
                            temp = i.split(' ')
                            if len(temp) < 2:
                                continue
                            elif temp[1] == '0' or temp[1] == '':
                                continue
                            else:
                                xaxis.append(float(temp[0]))
                                yaxis.append(float(temp[1]))

            #Plots the elements found within the csv files.
            plt.plot(xaxis, yaxis, "o")
            #Sets the labels.
            plt.ylabel(value2)
            plt.xlabel(value1)
            #Shows the plotted graph.
            plt.show()
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
