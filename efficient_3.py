import sys
from resource import *
import time
import psutil

GAP_PENALTY = 30

MISMATCH_PENALTY = {
    ('A', 'A'): 0,
    ('T', 'T'): 0,
    ('C', 'C'): 0,
    ('G', 'G'): 0,
    ('A', 'T'): 94,
    ('T', 'A'): 94,
    ('A', 'C'): 110,
    ('C', 'A'): 110,
    ('A', 'G'): 48,
    ('G', 'A'): 48,
    ('T', 'C'): 48,
    ('C', 'T'): 48,
    ('T', 'G'): 48,
    ('G', 'T'): 48,
    ('G', 'C'): 118,
    ('C', 'G'): 118,
}


def main():
    INPUT = "SampleTestCases/" + sys.argv[1]
    [x, y] = generateStrings(INPUT)
    start_time = time.time()
    output = nw(x, y)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    # score
    print(output[0])
    # x answer
    print(output[1])
    # y answer
    print(output[2])
    # time
    print(time_taken)
    # memory
    print(process_memory())

def hirschberg(x, y):
    z = ""
    w = ""
    if len(x) == 0:
        for i in y:
            z = z + '-'
            w = w + i
    elif len(y) == 0:
        for i in x:
            z = z + i
            w = w + '-'
    elif len(x) == 1 or len(y) == 1:
        output = nw(x, y)
        z = output[1]
        w = output[2]
    else:
        xlen = len(x)
        xmid = len(x) / 2
        ylen = len(y)

        # scoreL = nwScore(x[:xmid], y)
        # scoreR = nwScore(x[xmid:][::-1], y[::-1])
        ymid = argMax(scoreL + scoreR[::-1])

        z, w = hirschberg(x[:xmid], y[:ymid]) + hirschberg(x[xmid:], y[ymid:])
    
    return z, w

def argMax(scoreL, scoreR):
  max_index = 0
  max_sum = float('-Inf')
  for i, (l, r) in enumerate(zip(scoreL, scoreR)):
    # calculate the diagonal maximum index
    if sum([l, r]) > max_sum:
      max_sum = sum([l, r])
      max_index = i
  return max_index 

def nw(x, y):
    # len(x): number of rows
    # len(y): number of columns
    memo = [[0 for i in range(len(y) + 1)] for j in range(len(x) + 1)]

    # Initialize 0th row
    memo[0] = [i*GAP_PENALTY for i in range(len(y) + 1)]

    # Initialize 0th column
    for j, row in enumerate(memo):
        row[0] = j*GAP_PENALTY

    # Fill memo table
    for i in range(1, len(memo)):
        for j in range(1, len(memo[0])):
            memo[i][j] = min(
                MISMATCH_PENALTY[(x[i - 1], y[j - 1])] + memo[i-1][j-1],  # mismatch
                GAP_PENALTY + memo[i-1][j], # gap on y
                GAP_PENALTY + memo[i][j-1] # gap on x
            )
    
    # reconstruct solution
    i = len(x)
    j = len(y)
    xans = ""
    yans = ""
    while((i != 0) and (j != 0)):
        if(memo[i][j] == MISMATCH_PENALTY[(x[i - 1], y[j - 1])] + memo[i-1][j-1]):
            xans = x[i - 1] + xans
            yans = y[j - 1] + yans
            i -= 1
            j -= 1
        elif (memo[i][j] == GAP_PENALTY + memo[i-1][j]):
            xans = x[i - 1] + xans
            yans = "_" + yans
            i -= 1
        elif (memo[i][j] == GAP_PENALTY + memo[i][j - 1]):
            xans = "_" + xans
            yans = y[j - 1] + yans
            j -= 1

    while(i > 0):
        xans = x[i - 1] + xans
        yans = "_" + yans
        i -= 1
    while(j > 0):
        xans = "_" + xans
        yans = y[j - 1] + yans
        j -= 1

    return([memo[len(x)][len(y)], xans, yans])


def generateStrings(fileName):
    x = ""
    y = ""
    arrNum = 1
    arr1 = []
    arr2 = []

    # Read file input
    with open(fileName) as file:
        for i, line in enumerate(file):
            if(i == 0): # first line in file
                x = line
            else: 
                if(arrNum == 1): # first line in file
                    try:
                        arr1.append(int(line))
                    except ValueError:
                        y = line
                        arrNum = 2
                else: 
                    arr2.append(int(line))

    # Generate string x
    for index in arr1:
        x = x[:index + 1] + x + x[index + 1:]

    x = x.replace(' ', '').replace('\n', '')

    # Generate string y
    for index in arr2:
        y = y[:index + 1] + y + y[index + 1:]

    y = y.replace(' ', '').replace('\n', '')

    return[x, y]

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def check(x, y):
    print(x)
    print(y)
    cost = 0
    for i in range(len(x)):
        if(x[i] == '_'):
            cost += GAP_PENALTY
        elif(y[i] == '_'):
            cost += GAP_PENALTY
        else:
            cost += MISMATCH_PENALTY[(x[i], y[i])]

    print(cost)


if __name__ == "__main__":
    main()
