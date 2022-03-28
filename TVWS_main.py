import os
import TVWS_process
import TVWS_tools
import TVWS_tools2
import TVWS_graph

# Globals
directory = None
graph = None
filters = []
totalCalcs = {}
avgCalcs = {}

# Function to set or update path of current working directory
def set_directory():
    global directory
    loop2 = True
    while loop2:
        inpt = input("Type info for help.\n" + "Enter directory: ")
        if inpt == "exit": loop2 = False
        elif inpt == "list": print(directory)
        elif inpt == "info":
            print("Set_Directory Info: " +
                  "\nInput: " +
                  "\n- 'list' : Outputs path to current working directory" +
                  "\n- 'exit' : Returns to main menu")
        elif os.path.isdir(inpt):
            directory = inpt
            print("Directory path set. ")
            loop2 = False
        else: print("Directory does not exist, re-renter. ")


# Function to set or update fields to be filtered when processing .pcap files
def set_filters():
    global filters
    loop2 = True
    while loop2:
        fltrs = list(input("Type info for help.\n" + "Enter filters: ").split())
        if fltrs[0] == "exit": loop2 = False
        elif fltrs[0] == "info":
            print("Set_Filter Info: " +
                  "\nPreface command using: " +
                  "\n- 'add' : Adds one or more fields to existing filter, separating arguments with a space" +
                  "\n- 'remove' : Removes one or more fields from existing filter, separating arguments with a space" +
                  "\n- 'clear' : Clears filter" +
                  "\n- 'list' : Outputs current fields in filter" +
                  "\n- 'exit' : Returns to main menu" +
                  "\nNone of the above arguments clears filter and adds in one or more fields, separating with a space")
        elif fltrs[0] == "add":
            for item in fltrs:
                if item != "add" and item not in filters:
                    filters.append(item)
            print("Filter(s) added. ")
        elif fltrs[0] == "remove":
            for item in fltrs:
                if item != "remove" and item in filters:
                    filters.remove(item)
            print("Filter(s) removed. ")
        elif fltrs[0] == "clear":
            filters.clear()
            print("Filters cleared. ")
        elif fltrs[0] == "list":
            print(filters)
        else:
            filters.clear()
            for item in fltrs:
                filters.append(item)
            print("Filter(s) added. ")


# Function to set graph type
def set_graph():
    global graph
    loop2 = True
    while loop2:
        choice = input("Type info for help.\n" + "Select graph type (plot/bar/scatter): ")
        if choice == "exit":
            loop2 = False
        elif choice == "info":
            print("Process Info: " +
                  "\nInput: " +
                  "\n- 'plot' : Set graph to plot" +
                  "\n- 'scatter' : Set graph to scatter" +
                  "\n- 'bar' : Set graph to bar")
        elif choice == "plot" or choice == "scatter" or choice == "bar":
            graph = choice
            print("Graph set.")
        else: print("Invalid entry, re-renter. ")


def main():
    global directory
    global graph
    global filters
    global tempTotal
    global tempAvg
    global totalCalcs
    global avgCalcs

    print("PCAP Trace Processing Tool" +
    "\nType info for help:")
    loop = True

    while loop:
        print("Main Menu: ")
        choice = input()

        if choice == "info":
            print("Main Menu Info: " +
                  "\nInput: " +
                  "\n- 'dir' : Enter specified directory from which .pcap files are processed" +
                  "\n- 'filter' : Enter fields to filter .pcap files from specified directory" +
                  "\n- 'graph' : Enter fields to be present in graph and type of graph" +
                  "\n- 'process' : Processes .pcap files in specified directory with chosen fields, and outputs them" +
                  " in desired graph" +
                  "\n- 'exit' : Exits PCAP Trace Processing Tool")
        elif choice == "dir":
            set_directory()
        elif choice == "filter":
            set_filters()
        elif choice == "graph":
            set_graph()
        elif choice == "process":
            TVWS_process.process(directory, filters)
        elif choice == "tools":
            loop2 = True
            while loop2:
                choice2 = input("Select tool: ")
                if choice2 == "info":
                    print("Tools Info: " +
                          "\nInput: " +
                          "\n- 'calc' : Calculates total and averages among values" +
                          "\n- 'graph' : Plots desired data points")
                elif choice2 == "calc":
                    totalValue, total, avgValue, avg, count = TVWS_tools2.calc(directory, filters)
                    totalCalcs[totalValue] = total
                    avgCalcs[avgValue] = avg
                    print("TOTAL: ", totalCalcs[totalValue])
                    print("AVERAGE: ", avgCalcs[avgValue])
                    print("COUNT: ", count)
                elif choice2 == "graph":
                    TVWS_graph.graph(directory, graph, filters)
                elif choice2 == "exit":
                    loop2 = False
                else: print("Invalid command, re-enter. ")
        elif choice == "exit":
            loop = False
        else: print("Invalid command, re-enter. ")


main()