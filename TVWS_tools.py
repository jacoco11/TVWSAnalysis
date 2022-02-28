import os
import sys
import subprocess
import csv
import matplotlib.pyplot as plt
import numpy as np

# GLOBALS
tempTotal = []
tempAvg = []


# Function to address formatting issues in .csv files that occurs with ICMP packets (type 3)
def findPlace(filters, value):
    valIndex = filters.index(value)
    skipCount = 0

    if value == "ip.src" or value == "ip.dst" or value == "ip.proto" or value == "ip.ttl":
        if value == "ip.src":
            if valIndex > filters.index("ip.dst"): skipCount += 1
            if valIndex > filters.index("ip.proto"): skipCount += 1
            if valIndex > filters.index("ip.ttl"): skipCount += 1
        elif value == "ip.dst":
            if valIndex > filters.index("ip.src"): skipCount += 1
            if valIndex > filters.index("ip.proto"): skipCount += 1
            if valIndex > filters.index("ip.ttl"): skipCount += 1
        elif value == "ip.proto":
            if valIndex > filters.index("ip.src"): skipCount += 1
            if valIndex > filters.index("ip.dst"): skipCount += 1
            if valIndex > filters.index("ip.ttl"): skipCount += 1
        else:
            if valIndex > filters.index("ip.src"): skipCount += 1
            if valIndex > filters.index("ip.dst"): skipCount += 1
            if valIndex > filters.index("ip.proto"): skipCount += 1
    else:
        if valIndex > filters.index("ip.src"): skipCount += 1
        if valIndex > filters.index("ip.dst"): skipCount += 1
        if valIndex > filters.index("ip.proto"): skipCount += 1
        if valIndex > filters.index("ip.ttl"): skipCount += 1

    return skipCount


# Function to process and output data
def process(directory, filters):
    # If filters are specified, include those in command, otherwise use default filters
    if len(filters) != 0:
        print("Processing files... ")
        for file in os.listdir(directory):
            if file.endswith(".pcap"):
                filename2 = os.path.splitext(file)[0] + '.csv'
                with open(directory + "\\" + filename2, "w") as outfile:
                    command = []
                    commandBegin = ["C:\Program Files\Wireshark\\tshark.exe", "-r", os.path.join(directory, file), "-e", "icmp.type"]
                    for item in commandBegin:
                        command.append(item)
                    # fields = " ".join(str(e) for e in __filters2) #list to string
                    for fltr in filters:
                        command.append("-e")
                        command.append(fltr)
                    commandEnd = ["-T", "fields", "-E", "separator=,"]
                    for item in commandEnd:
                        command.append(item)

                    try:
                        subprocess.run(command, stdout=outfile, check=True)
                        print("Files processed. ")
                    except Exception as err:
                        print("ERROR: Unable to run tshark command: " + err)
                        continue
    else:
        print("ERROR: No filters specified. ")


# Function to perform calculations on processed data
def calc(directory, graph, filters):
    global tempTotal
    global tempAvg

    # Perform calculations on data: total and average
    check = True
    while check:
        calc = input("Enter function: ")
        if calc == "total" or calc == "avg": check = False
        elif calc == "info":
            print("Tools/Calc Info: " +
                  "\nInput: " +
                  "\n- 'totaL' : Calculates the total of a value" +
                  "\n- 'avg' : Calculates the average of a value")
        else: print("Invalid function, re-enter. ")
    check2 = True
    while check2:
        value = input("Enter field: ")
        if value in filters: check2 = False
        else: print("invalid field, re-enter. ")

    indx = int(filters.index(value) + 1)
    skipCount = findPlace(filters, value)

    success = 0
    error = 0
    icmp3 = 0

    for file in os.listdir(directory):
        total = 0
        count = 0
        avg = 0
        if file.endswith(".csv"):
            with open(os.path.join(directory, file)) as f:
                csv_reader = csv.reader(f, delimiter=',')
                for row in csv_reader:
                    icmpCheck = row[0].rstrip()
                    line = row[indx].rstrip()
                    
                    if icmpCheck != "3" and line:
                        if calc == "total":
                            try:
                                #print("SUCCESS: ", row[indx])
                                total += float(row[indx])
                                success += 1
                            except:
                                #print("ERROR: ", row[indx])
                                error += 1
                                continue
                        elif calc == "avg":
                            try:
                                #print("SUCCESS: ", row[indx])
                                avg += float(row[indx])
                                count += 1
                                success += 1
                            except:
                                #print("ERROR: ", row[indx])
                                error += 1
                                continue
                    elif icmpCheck == "3":
                        if calc == "total":
                            line = row[indx + skipCount].rstrip()
                            if line:
                                try:
                                    #print("ICMP3: ", row[indx + skipCount])
                                    total += float(row[indx + skipCount])
                                    icmp3 +=1
                                except:
                                    #print("ICMP3 ERROR: ", row[indx + skipCount])
                                    error += 1
                                    continue
                        elif calc == "avg":
                            line = row[indx + skipCount].rstrip()
                            if line:
                                try:
                                    #print("ICMP3: ", row[indx + skipCount])
                                    avg += float(row[indx + skipCount])
                                    count += 1
                                    icmp3 += 1
                                except:
                                    error += 1
                                    #print("ICMP3 ERROR: ", row[indx + skipCount])
                                    continue

                if calc == "total": tempTotal.append(total)
                elif calc == "avg": tempAvg.append([avg, count])

    print("SUCCESS: ", success, " ICMP3: ", icmp3, "ERROR: ", error)
    if calc == "total":
        try:
            totalTotal = 0
            for item in tempTotal:
                totalTotal += item
            return value, totalTotal, None, None
        except:
            print("Error: Unable to perform calculation")
    elif calc == "avg":
        try:
            totalAvg = 0
            totalCount = 0
            for item in tempAvg:
                totalAvg += item[0]
                totalCount += item[1]
            avg = totalAvg / totalCount
            return None, None, value, avg
        except:
            print("Error: Unable to perform calculation")
    else: return None, None, None


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
            else:
                print("Invalid field(s), re-enter. ")
        indx1 = int(filters.index(value1) + 1)
        indx2 = int(filters.index(value2) + 1)
        #print("INDEX1: ", indx1, " INDEX2: ", indx2)

        skipCount1 = findPlace(filters, value1)
        skipCount2 = findPlace(filters, value2)
        #print("SKIPC1: ", skipCount1, " SKIPC2: ", skipCount2)

        if graph == "plot":
            plt.grid()
            plt.rcParams["figure.figsize"] = [100.00, 5.00]
            plt.rcParams["figure.autolayout"] = True
            for file in os.listdir(directory):
                if file.endswith(".csv"):
                    with open(os.path.join(directory, file)) as f:
                        csv_reader = csv.reader(f, delimiter=',')
                        for row in csv_reader:
                            icmpCheck1 = row[0].rstrip()
                            line1 = row[indx1].rstrip()
                            line2 = row[indx2].rstrip()
                            if icmpCheck1 != "3" and line1 and line2:
                                plt.plot(float(row[indx1]), float(row[indx2]), marker="o", markersize=7.5,
                                         markerfacecolor="blue")
                            elif icmpCheck1 == "3":
                                line1 = row[indx1 + skipCount1].rstrip()
                                line2 = row[indx2 + skipCount2].rstrip()
                                if line1 and line2:
                                    plt.plot(float(row[indx1 + skipCount1]), float(row[indx2 + skipCount2]),
                                             marker="o", markersize=7.5, markerfacecolor="blue")
            plt.show()

        elif graph == "scatter":
            gsuccess = 0
            gerror = 0
            plt.style.use('seaborn')
            for file in os.listdir(directory):
                if file.endswith(".csv"):
                    with open(os.path.join(directory, file)) as f:
                        csv_reader = csv.reader(f, delimiter=',')
                        for row in csv_reader:
                            icmpCheck1 = row[0].rstrip()
                            line1 = row[indx1].rstrip()
                            line2 = row[indx2].rstrip()
                            if icmpCheck1 != "3" and line1 and line2:
                                try:
                                    if isinstance(float(row[indx1]), float) and isinstance(float(row[indx2]), float):
                                        #print(float(row[indx1]), float(row[indx2]))
                                        plt.scatter(float(row[indx1]), float(row[indx2]), edgecolor='black',
                                                    linewidth=1, alpha=0.75)
                                        gsuccess += 1
                                except:
                                    gerror += 1
                                    continue
                            elif icmpCheck1 == "3":
                                line1 = row[indx1 + skipCount1].rstrip()
                                line2 = row[indx2 + skipCount2].rstrip()
                                if line1 and line2:
                                    try:
                                        if isinstance(float(row[indx1 + skipCount1]), float) and isinstance(
                                                float(row[indx2 + skipCount2]), float):
                                            #print(float(row[indx1 + skipCount1]), float(row[indx2 + skipCount2]))
                                            plt.scatter(float(row[indx1 + skipCount1]), float(row[indx2 + skipCount2]),
                                                        edgecolor='black', linewidth=1, alpha=0.75)
                                            gsuccess += 1
                                    except:
                                        gerror += 1
                                        continue
            plt.title("Scatter: " + value1 + " x " + value2)
            plt.xlabel(value1)
            plt.ylabel(value2)
            plt.tight_layout()
            print("SUCCESS: ", gsuccess, " ERROR: ", gerror)
            plt.show()

    else:
        print("No graph type selected. ")

