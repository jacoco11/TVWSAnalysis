import os
import subprocess


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
                    commandBegin = ["tshark.exe", "-r", os.path.join(directory, file)]
                    for item in commandBegin:
                        command.append(item)
                    # fields = " ".join(str(e) for e in __filters2) #list to string
                    for fltr in filters:
                        command.append("-e")
                        command.append(fltr)
                    commandEnd = ["-T", "fields", "-E", "separator=,", "-E", "occurrence=f"]
                    for item in commandEnd:
                        command.append(item)

                    try:
                        subprocess.run(command, stdout=outfile, check=True)
                    except Exception as err:
                        print("ERROR: Unable to run tshark command: ", err)
                        continue
        print("Files processed. ")
    else:
        print("ERROR: No filters specified. ")