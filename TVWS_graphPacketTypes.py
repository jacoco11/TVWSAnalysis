import os
import pyshark
import collections
import matplotlib.pyplot as plt
import numpy as np
import glob


def capgraph(directory):
    csv_files = glob.glob(directory + "\*.pcap")
    for file in csv_files:
        print("Processing" + file)
        cap = pyshark.FileCapture(file, only_summaries=True)
        protocolList = []
        for packet in cap: #Iterates packets in file(s)
            line = str(packet)
            #print(line)
            formattedLine = line.split(" ")
            protocolList.append(formattedLine[4])
        counter = collections.Counter(protocolList)

#GRAPH STYLING----------------------------------------------------------------------------------------------  
        plt.style.use('ggplot')
        y_pos = np.arange(len(list(counter.keys())))
        plt.bar(y_pos, list(counter.values()), align='center', width = 1, alpha=0.5, color=['b', 'r',])
        plt.xticks(y_pos, list(counter.keys()), rotation = 90)
        plt.xlabel("Protocol Name", labelpad = 7)
        plt.ylabel("Frequency of Packet Type")
        plt.savefig(file + ".png")
        plt.show()