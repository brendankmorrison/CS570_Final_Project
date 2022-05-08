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
    INPUT = "SampleTestCases/" + sys.argv[1]
    [x, y] = generateStrings(INPUT)
    start_time = time.time()
    z, w = hirschberg(x, y)
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

    """
    filepath = "SampleTestCases/" + sys.argv[1]
    [x, y] = generateStrings(filepath)
    # print(str(nw_score(x, y)))
    start_time = time.time()
    z, w = hirschberg(x, y)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    # validate
    # print(validateStrings(x, z))
    # print(validateStrings(y, w))
    # score
    check(z, w)
    # x answer
    print(z)
    # y answer
    print(w)
    # time
    # print(time_taken)
    # memory
    # print(process_memory())
    """


def hirschberg(x, y):
    z = ""
    w = ""
    if len(x) < 2 or len(y) < 2:
        output = nw(x, y)
        z = output[1]
        w = output[2]
    else:
        m = len(x)
        n = len(y)

        score_l = nw_score(x, y[:n//2])
        score_r = nw_score(x[::-1], y[n//2:][::-1])
        q = argmin(score_l, score_r[::-1])

        zl, wl = hirschberg(x[:q], y[:n//2])
        zr, wr = hirschberg(x[q:], y[n//2:])

        z = zl + zr
        w = wl + wr

    return z, w


def nw_score(x, y):
    prev = [i * GAP_PENALTY for i in range(len(x) + 1)]
    current = [0 for i in range(len(x) + 1)]

    for j in range(1, len(y) + 1):
        current[0] = j * GAP_PENALTY
        for i in range(1, len(x) + 1):
            score_sub = prev[i - 1] + MISMATCH_PENALTY[(x[i - 1], y[j - 1])]
            score_del = prev[i] + GAP_PENALTY
            score_ins = current[i - 1] + GAP_PENALTY
            current[i] = min(score_sub, score_del, score_ins)
        # prev = copy.copy(current)
        prev = copy.deepcopy(current)
        # prev = current



    return current


def argmin(score_l, score_r):
    min_index = 0
    min_sum = float('Inf')
    for i in range(len(score_l)):
        if score_l[i] + score_r[i] < min_sum:
            min_sum = score_l[i] + score_r[i]
            min_index = i

    return min_index


"""
def hirschberg(x, y):
    z = ""
    w = ""
    if len(x) == 0:
        for i in y:
            z = z + '_'
            w = w + i
    elif len(y) == 0:
        for i in x:
            z = z + i
            w = w + '_'
    elif len(x) == 1 or len(y) == 1:
        output = nw(x, y)
        z = output[1]
        w = output[2]
    else:
        x_len = len(x)
        x_mid = len(x) // 2
        y_len = len(y)

        score_l = nw_score(x[:x_mid], y)
        score_r = nw_score(x[x_mid:][::-1], y[::-1])
        y_mid = argmax(score_l, score_r[::-1])

        zl, wl = hirschberg(x[:x_mid], y[:y_mid])
        zr, wr = hirschberg(x[x_mid:], y[y_mid:])

        z = zl + zr
        w = wl + wr

    return z, w


# returns last line of the nw score matrix
def nw_score(x, y):
    insert = -2
    delete = -2

    prev = [0 for i in range(len(y) + 1)]
    current = [0 for i in range(len(y) + 1)]

    for j in range(1, len(y) + 1):
        prev[j] = prev[j - 1] + insert

    for i in range(1, len(x) + 1):
        current[0] = current[0] + delete
        for j in range(1, len(y) + 1):
            score_sub = prev[j - 1] + sub(x[i - 1], y[j - 1])
            score_del = prev[j] + delete
            score_ins = current[j - 1] + insert
            current[j] = max(score_sub, score_del, score_ins)
        # prev = copy.copy(current)
        prev = copy.deepcopy(current)
        # prev = current


    print("test: " + str(current))

    return current
"""

def sub(x, y):
    if x == y:
        return 2
    else:
        return -1


def argmax(score_l, score_r):
    max_index = 0
    max_sum = float('-Inf')
    for i in range(len(score_l)):
        if score_l[i] + score_r[i] > max_sum:
            max_sum = score_l[i] + score_r[i]
            max_index = i

    return max_index


def nw(x, y):
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
