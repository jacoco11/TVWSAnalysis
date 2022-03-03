import os
import csv

# GLOBALS
tempTotal = []
tempAvg = []
tempCount = 0


# Function to perform calculations on processed data
def calc(directory, filters):
    global tempTotal
    global tempAvg
    global tempCount

    tempTotal.clear()
    tempAvg.clear()
    tempCount = 0

    # Perform calculations on data: total and average
    check = True
    while check:
        calc = input("Enter function: ")
        if calc == "total" or calc == "avg" or calc == "count": check = False
        elif calc == "info":
            print("Tools/Calc Info: " +
                  "\nInput: " +
                  "\n- 'count' : Calculates the amount of occurrences of a value" +
                  "\n- 'totaL' : Calculates the total of a value" +
                  "\n- 'avg' : Calculates the average of a value")
        else: print("Invalid function, re-enter. ")
    check2 = True
    while check2:
        value = input("Enter field: ")
        if value in filters: check2 = False
        else: print("invalid field, re-enter. ")
    indx = int(filters.index(value))

    success = 0
    error = 0

    fileNum = 0
    for file in os.listdir(directory):
        rowNum = 0
        total = 0
        avg = 0
        count = 0
        if file.endswith(".csv"):
            with open(os.path.join(directory, file)) as f:
                csv_reader = csv.reader(f, delimiter=',')
                fileNum += 1
                for row in csv_reader:
                    rowNum += 1
                    line = row[indx].rstrip()
                    if line:
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
                        elif calc == "count":
                            try:
                                #print("SUCCESS: ", row[indx])
                                count += 1
                                success += 1
                            except:
                                #print("ERROR: ", row[indx])
                                error += 1
                                continue

                if calc == "total": tempTotal.append(total)
                elif calc == "avg": tempAvg.append([avg, count])
                elif calc == "count": tempCount += count

    print("SUCCESS: ", success, " ERROR: ", error)
    if calc == "total":
        try:
            totalTotal = 0
            for item in tempTotal:
                totalTotal += item
            return value, totalTotal, None, None, None
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
            print("TOTAL AVG: ", totalAvg, "TOTAL COUNT: ", totalCount, "AVG: ", avg)
            return None, None, value, avg, None
        except:
            print("Error: Unable to perform calculation")
    elif calc == "count":
        try:
            return None, None,None, None, tempCount
        except:
            print("Error: Unable to perform calculation")
    else: return None, None, None, None, None