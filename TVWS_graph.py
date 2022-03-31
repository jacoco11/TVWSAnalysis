import os
import csv
import subprocess
#import pyqtgraph as pg
import matplotlib.pyplot as plt
import glob
import pandas as pd
import numpy as np
import TVWS_process
import TVWS_tools1
#

# Function for data visualization on processed data
def graph(directory, graph, filters):
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
            looptyloop = True
            while looptyloop:
                value1 = input("Info for help\nEnter what you want graphed: ")
                if value1 == "exit": looptyloop = False
                if(value1 == "info"):
                    print("Bar Graph Info: " +
                    "\n- 'PercentFlow' : graphs completed/failed flows" +
                    "\n- 'AggregateBytes' : graphs Aggregate byte size" +
                    "\n- 'AverageFlow' : graphs Average Flow size" +
                    "\n- 'AvgTCPStat' : generates table of average TCP statistics" +
                    "\n- 'exit' : exit back to main menu")
                elif(value1.lower() == "percentflow"):
                    looptyloop = False
                elif(value1.lower() == "aggregatebytes"):   
                    looptyloop = False
                elif(value1.lower() == "averageflow"):
                    looptyloop = False
                elif(value1.lower() == "avgtcpstat"):
                    fig, ax = plt.subplots()
                    table_data=[]
                    filters.append("tcp.len")
                    filters.append("tcp.analysis.ack_rtt")
                    filters.append("tcp.analysis.fast_retransmission")
                    filters.append("tcp.analysis.retransmission")
                    filters.append("tcp.flags")
                    ans = input("Process files? No if already processed. (y/n): ")
                    if ans.lower() == "y":
                        TVWS_process.process(directory, filters, "", "", "")
                    sizeOfFiles = TVWS_tools1.calc("total", "tcp.len", filters, directory, "1", "", "")/8589934592 # Bytes -> GB
                    print(sizeOfFiles)
                    totalPackets = TVWS_tools1.calc("count", "tcp.len", filters, directory, "1", "", "")
                    print(totalPackets)
                    totalControlPackets = TVWS_tools1.calc("count", "cpkt", filters, directory, "1", "", "")
                    print(totalControlPackets)
                    avgRTT = TVWS_tools1.calc("avg", "tcp.analysis.ack_rtt", filters, directory, "1", "", "")
                    print(avgRTT)
                    totalRetransmissions = (TVWS_tools1.calc("total", "tcp.analysis.fast_retransmission", filters, directory, "1", "", "") +
                    TVWS_tools1.calc("total", "tcp.analysis.retransmission", filters, directory, "1", "", ""))
                    print(totalRetransmissions)
                    table_data.append(sizeOfFiles)
                    table_data.append(totalPackets)
                    table_data.append(totalControlPackets)
                    table_data.append(avgRTT)
                    table_data.append(totalRetransmissions)
                    data=[]
                    data.append(table_data) # Tables require an array inside an array???
                    print(table_data)
                    column_labels=["Total GB", "Total Packets", "Total control packets (%)", "Average RTT(s)", "Total retransmissions(%)"]
                    the_table = ax.table(fontsize=40,cellText=data,colLabels=column_labels, loc="center")
                    ax.axis('off')
                    the_table.set_fontsize(20)
                    plt.show()
                    looptyloop == False