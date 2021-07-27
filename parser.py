# Parses the curl--help file (output from curl --help) and makes a skeleton for the completion spec
import re
import json

with open('curl--help', 'r') as infile:
    global s
    s = infile.read()

# Helper function to print and debug, delete after


def printArray(arr):
    for x in arr:
        print(x)


def parseInput(s):
    # Parse curl--help by splitting on - and --
    fullArray = re.split(r"(\s\s--|\s\s-)", s)

    # Delete all occurances of \n in array
    noNewlineArr = [x.replace("\n", "") for x in fullArray]

    # Delete lasdt val & first value (not option)
    noNewlineArr.pop()
    noNewlineArr = noNewlineArr[1:]

    # Combine delimiters with appropriate options + descriptions
    combinedArr = []
    i = 0
    while i < len(noNewlineArr) - 1:
        combinedArr.append(noNewlineArr[i].strip() + noNewlineArr[i+1])
        i += 2

    # Split based on commas to separate short and long options
    separatedArr = []
    for val in combinedArr:
        if "," in val[:4]:
            twothings = val.split(",")

            # manipulate to add first thing
            firsthing = twothings[1].split()
            firsthing[0] = twothings[0]
            separatedArr.append(" ".join(firsthing))

            # add the second thing
            separatedArr.append(twothings[1])

    # Construct new array of combinedArr (minus the ones with commas + seperatedArr)
    for val in combinedArr:
        if "," not in val[:4]:
            separatedArr.append(val)

    # printArray(separatedArr)

    # Split on new word sunless it start with <
    finalArr = []
    for item in separatedArr:
        # Put them in format of [option, description, arg (if it exists)]
        vals = item.split()
        lilArray = []
        lilArray.append(vals[0])  # adding options

        if vals[1][0] == "<":
            lilArray.append(" ".join(vals[2:]))
            lilArray.append(vals[1])  # adding optional argument
        else:
            lilArray.append(" ".join(vals[1:]))

        if len(lilArray) > 2:
            lilArray[2] = lilArray[2][1:-1]

        print(lilArray)
        finalArr.append(lilArray)

    # Combines short and long options
    superFinalArr = []
    i = 0

    # TODO: Missing a few options for some reason here, troubleshoot
    while i < len(finalArr) - 1:
        # if descriptions are the same, append to just one item to finalArr with name being an array
        # else just append
        if finalArr[i][1] == finalArr[i+1][1]:
            temp = [[finalArr[i][0], finalArr[i+1][0]], finalArr[i][1]]
            if len(finalArr[i]) > 2:
                temp.append(finalArr[i][2])
            superFinalArr.append(temp)
            i += 2
        else:
            superFinalArr.append(finalArr[i])
            i += 1
    superFinalArr.append(finalArr[-1])
    printArray(superFinalArr)

    return finalArr


def completionSpecsJSON(l):

    # Getting a list of [opt, description, arg] & turning it into JSON
    options = []
    for item in l:
        dict = {
            "name": item[0],
            "description": item[1] if len(item) > 1 else ""
        }
        if len(item) > 3:
            dict["args"] = [{
                "name": item[2],
                "description": item[2]
            },
                {
                "name": item[3],
                "description": item[3]
            }, ]
        elif len(item) > 2:
            dict["args"] = {
                "name": item[2],
                "description": item[2]
            }
        options.append(dict)

    # write to json
    with open('data.json', 'w') as outfile:
        json.dump(options, outfile)


# TODO: Manually use insertValue for anything that has an = and also look for all / and | to make them multiple args or something in the final spec
parseInput(s)
# completionSpecsJSON(formatArray(parseInput(s)))

'''
Should look like:
    options: [
    {
        name: "--name",
        description: "Mandatory flag.",
        args: {
            name: "env-name",
            description: "Env name",
        },
    },
],
'''
