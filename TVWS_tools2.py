import os
import csv
import subprocess

# GLOBALS
count = 0
total = 0
average = []


# Function to perform calculations on processed data
def calc(directory, filters):
    global count
    global total
    global average

    count = 0
    total = 0
    average.clear()

    check = True
    while check:
        calc = input("Enter function: ")
        if calc == "total" or calc == "avg" or calc == "count": check = False
        elif calc == "info":
            print("Tools/Calc Info: " +
                  "\nInput: " +
                  "\n- 'count' : Calculates the amount of occurrences of a value" +
                  "\n- 'total' : Calculates the total of a value" +
                  "\n- 'avg' : Calculates the average of a value")
        else: print("Invalid function, re-enter. ")
    check2 = True
    while check2:
        value = input("Enter field: ")
        if value in filters: check2 = False
        else: print("invalid field, re-enter. ")
    indx = int(filters.index(value))
    indx = indx + 1
    indx = str(indx)

    for file in os.listdir(directory):
        if file.endswith(".csv"):
            if calc == "count":
                try:
                    #command = "awk -F \",\" \"BEGIN{count=0}($"+indx+"!=\\\"\\\"){count=count+1}END{print count}\" " + os.path.join(directory, file)
                    #subprocess.run(command)
                    proc = subprocess.Popen("awk -F \",\" \"BEGIN{count=0}($"+indx+"!=\\\"\\\"){count=count+1}END{print count}\" "
                                            + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    count += int(proc.communicate()[0].decode('ascii'))
                except:
                    print("ERROR: Could not perform calculation. ")
                    continue
            elif calc == "total":
                try:
                    #command = ["awk", "-F", ",", "\"BEGIN{sum=0}{sum=sum+$"+indx+"}END{print", "sum}\"", file]
                    #subprocess.run(command)
                    proc = subprocess.Popen("awk -F \",\" \"BEGIN{total=0}($"+indx+"!=\\\"\\\"){total=total+$"+indx+"}END{print total}\" "
                                            + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    total += float(proc.communicate()[0].decode('ascii'))
                except:
                    print("ERROR: Could not perform calculation. ")
                    continue
            elif calc == "avg":
                try:
                    #command = ["awk", "-F", ",", "BEGIN{sum=0;count=0}{sum=sum+$"+indx+";", "count=count+1}END{print", "sum,count}", file]
                    #subprocess.run(command)
                    proc = subprocess.Popen("awk -F \",\" \"BEGIN{total=0;count=0}($"+indx+"!=\\\"\\\"){total=total+$"+indx+";count=count+1}END{print total,count}\" "
                                            + os.path.join(directory, file), shell=True, stdout=subprocess.PIPE)
                    result = str(proc.communicate()[0].decode('ascii'))
                    results = result.split()
                    total = float(results[0])
                    count = float(results[1])
                    average.append([total, count])
                    count = 0
                    total = 0
                except:
                    print("ERROR: Could not perform calculation. ")
                    continue

    if calc == "count":
        return None, None,None, None, count
    elif calc == "total":
        return value, total, None, None, None
    elif calc == "avg":
        try:
            totalSum = 0
            totalCount = 0
            for item in average:
                totalSum += item[0]
                totalCount += item[1]
            avg = totalSum / totalCount
            return None, None, value, avg, None
        except:
            print("Error: Unable to perform calculation")
    else: return None, None, None, None, None