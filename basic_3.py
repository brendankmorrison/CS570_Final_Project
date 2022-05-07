import sys

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
    run(x, y)

def run(x, y):
    print(x)
    print(y)
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
    
    print(memo)


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


if __name__ == "__main__":
    main()
