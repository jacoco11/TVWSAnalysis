import os
import csv
import subprocess
#import pyqtgraph as pg
from  matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import glob
import pandas as pd
import numpy as np
import TVWS_graphPacketTypes


# Function for data visualization on processed data
def graph(directory, graph, filters):
    # Graph data points
    check = True
    while check:
        graphPacketTypes = input("Graph all Packet types of all pcap files in directory? (y/n)\n" + "Type 'n' to continue to graph processed data.")
        if graphPacketTypes == "y":
            check = False
            TVWS_graphPacketTypes.capgraph(directory)
        elif graphPacketTypes == "n":
            check = False
        else:
            print("Please enter a valid entry\n")

    #START OF GRAPHING PROCESSED DATA-------------------------------------------------------

    if graph != None:
        check2 = True
        if graph == "bar":
            check2 = False
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
            pdf = False
            print("'n' for feild 1(x) vs feild 2(y)")
            print("If 'y' for PDF it uses the feild one only")
            value = input("Would you like to Graph the PDF (y or n): ")
            if value == "y":
                pdf = True
            else:
                pdf = False

            plt.figure()
            plt.rcParams["figure.autolayout"] = True

            if "rtt" in value1:
                start = 0.01
                end = 1
                step = 0.01
            elif "bytes_in_flight" in value1:
                start = 0
                end = 100000
                step = start*100
            else:
                start = 0
                end = 2000
                step = 500
                
            for file in os.listdir(directory):
                if file.endswith(".csv"):
                    with open(os.path.join(directory, file)) as f:
                        csv_reader = csv.reader(f, delimiter=',')
                        xaxis = []
                        yaxis = []
                        count = 0
                        if pdf == False:
                            proc = subprocess.Popen("awk -F \",\" \"{a[$1]+=$2;b[$1]++}END{for(i \"in\" \"a){print\" i,a[i]/b[i]}}\" "+ os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc.communicate()[0].decode('ascii'))
                            temp2 = temp1.split('\r\n')
                            for i in temp2:
                                temp = i.split(' ')
                                if len(temp) < 2:
                                    continue
                                elif temp[1] == '0':
                                    continue
                                else:
                                    xaxis.append(temp[0])
                                    yaxis.append(temp[1])
                            plt.plot(xaxis, yaxis, '*')
                        else:
                            #Gets the count
                            proc = subprocess.Popen("awk -F \",\" \"BEGIN{count=0}($1!=\\\"\\\"){count=count+1}END{print count}\" "+ os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                            count += int(proc.communicate()[0].decode('ascii'))
                            #Gets the values of each value for first field that is not empty.
                            proc2 = subprocess.Popen("awk -F \",\" \"BEGIN{$1}($1!=\\\"\\\"){print $1}\" "+ os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                            temp1 = str(proc2.communicate()[0].decode('ascii'))
                            temp2 = temp1.splitlines()
                            for i in temp2:
                                if len(i) < 2:
                                    continue
                                elif i == '0' or i == ' ':
                                    continue
                                else:
                                    xaxis.append(i)
                            x = np.sort(xaxis)
                            y = np.arange(count) / float(count)
                            plt.plot(x, y, '*')
                            plt.yticks(np.arange(0, 1, 0.2))

            plt.xlabel(value1)
            plt.ylabel(value2)
            #plt.xticks(np.arange(start, end, step))
            plt.show()
        elif graph == "scatter":
            print()

        elif graph == "bar":
            check3 = True
            while check3:
                value1 = input("Enter a Field to graph from previously selected Filters: ")
                if value1 in filters:
                    check3 = False
                else:
                    print("Invalid field(s), re-enter. ")
            indx1 = int(filters.index(value1))

            csv_files = glob.glob(directory + "\*.csv")
            for file in csv_files:
                print("Reading from csv file: ", csv_files)
                xaxis = pd.read_csv(file)
                xaxis.plot()
                plt.ylabel("Frequency")
                plt.show()
            print("All files Graphed.")
    else:
        print("No graph type selected. ")
