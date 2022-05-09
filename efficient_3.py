import sys
import pdb
import copy
import math
import time
import psutil

GAP_PENALTY = 30

MISMATCH_PENALTY = {
    ('A', 'A'): 0,
    ('T', 'T'): 0,
    ('C', 'C'): 0,
    ('G', 'G'): 0,
    ('A', 'G'): 48,
    ('G', 'A'): 48,
    ('T', 'C'): 48,
    ('C', 'T'): 48,
    ('T', 'G'): 48,
    ('G', 'T'): 48,
    ('A', 'T'): 94,
    ('T', 'A'): 94,
    ('A', 'C'): 110,
    ('C', 'A'): 110,
    ('G', 'C'): 118,
    ('C', 'G'): 118,
}


def main():
    INPUT = sys.argv[1]
    [x, y] = generateStrings(INPUT)
    start_time = time.time()
    z, w = efficient(x, y)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000

    try:
        outputFile = open(sys.argv[2], "w") 
    except:
        outputFile = open(sys.argv[2], "x") 
    outputFile.write(str(check(z, w)) + '\n')
    outputFile.write(z + '\n')
    outputFile.write(w + '\n')
    outputFile.write(str(time_taken) + '\n')
    outputFile.write(str(process_memory()) + '\n')
    outputFile.close() 


def efficient(x, y):
    xans = ""
    yans = ""
    if len(x) < 2 or len(y) < 2:
        output = basic(x, y)
        xans = output[1]
        yans = output[2]
    else:
        m = len(x)
        n = len(y)

        score_l = score(x, y[:n//2])
        score_r = score(x[::-1], y[n//2:][::-1])
        q = min_index(score_l, score_r[::-1])

        xl, yl = efficient(x[:q], y[:n//2])
        xr, yr = efficient(x[q:], y[n//2:])

        xans = xl + xr
        yans = yl + yr

    return xans, yans


def score(x, y):
    prev = [i * GAP_PENALTY for i in range(len(x) + 1)]
    current = [0 for i in range(len(x) + 1)]

    for j in range(1, len(y) + 1):
        current[0] = j * GAP_PENALTY
        for i in range(1, len(x) + 1):
            current[i] = min(prev[i - 1] + MISMATCH_PENALTY[(x[i - 1], y[j - 1])], prev[i] + GAP_PENALTY, current[i - 1] + GAP_PENALTY)
        prev = copy.deepcopy(current)

    return current


def min_index(score_l, score_r):
    min_index = 0
    min_sum = float('Inf')
    for i in range(len(score_l)):
        if score_l[i] + score_r[i] < min_sum:
            min_sum = score_l[i] + score_r[i]
            min_index = i

    return min_index


def basic(x, y):
    # len(x): number of rows
    # len(y): number of columns
    memo = [[0 for i in range(len(y) + 1)] for j in range(len(x) + 1)]

    # Initialize 0th row
    memo[0] = [i * GAP_PENALTY for i in range(len(y) + 1)]

    # Initialize 0th column
    for j, row in enumerate(memo):
        row[0] = j * GAP_PENALTY

    # Fill memo table
    for i in range(1, len(memo)):
        for j in range(1, len(memo[0])):
            memo[i][j] = min(
                MISMATCH_PENALTY[(x[i - 1], y[j - 1])] + memo[i - 1][j - 1],  # mismatch
                GAP_PENALTY + memo[i - 1][j],  # gap on y
                GAP_PENALTY + memo[i][j - 1]  # gap on x
            )

    # reconstruct solution
    i = len(x)
    j = len(y)
    xans = ""
    yans = ""
    while ((i != 0) and (j != 0)):
        if (memo[i][j] == MISMATCH_PENALTY[(x[i - 1], y[j - 1])] + memo[i - 1][j - 1]):
            xans = x[i - 1] + xans
            yans = y[j - 1] + yans
            i -= 1
            j -= 1
        elif (memo[i][j] == GAP_PENALTY + memo[i - 1][j]):
            xans = x[i - 1] + xans
            yans = "_" + yans
            i -= 1
        elif (memo[i][j] == GAP_PENALTY + memo[i][j - 1]):
            xans = "_" + xans
            yans = y[j - 1] + yans
            j -= 1

    while (i > 0):
        xans = x[i - 1] + xans
        yans = "_" + yans
        i -= 1
    while (j > 0):
        xans = "_" + xans
        yans = y[j - 1] + yans
        j -= 1

    return ([memo[len(x)][len(y)], xans, yans])


def generateStrings(fileName):
    x = ""
    y = ""
    arrNum = 1
    arr1 = []
    arr2 = []

    # Read file input
    with open(fileName) as file:
        for i, line in enumerate(file):
            if (i == 0):  # first line in file
                x = line
            else:
                if (arrNum == 1):  # first line in file
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

    return [x, y]


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def check(x, y):
    cost = 0
    for i in range(len(x)):
        if (x[i] == '_'):
            cost += GAP_PENALTY
        elif (y[i] == '_'):
            cost += GAP_PENALTY
        else:
            cost += MISMATCH_PENALTY[(x[i], y[i])]

    return(cost)


def validateStrings(before, after):
    result = True
    iterator = 0
    for character in after:
        if(character != "_"):
            if(character != before[iterator]):
                return False
            else:
                iterator += 1
    
    return True


if __name__ == "__main__":
    main()
