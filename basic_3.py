import sys

GAP_PENALTY = 2

# strings are made up of only A, T, C, G
# we need to make a datastructure for mismatch penalties between these
MISMATCH_PENALTY = {
    ('A', 'A'): 0,
    ('T', 'T'): 0,
    ('C', 'C'): 0,
    ('G', 'G'): 0,
    ('A', 'T'): 1,
    ('T', 'A'): 1,
    ('A', 'C'): 2,
    ('C', 'A'): 2,
    ('A', 'G'): 3,
    ('G', 'A'): 3,
    ('T', 'C'): 4,
    ('C', 'T'): 4,
    ('T', 'G'): 5,
    ('G', 'T'): 5,
    ('G', 'C'): 6,
    ('C', 'G'): 6,
}


def main():
    INPUT = "datapoints/" + sys.argv[1]
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
                MISMATCH_PENALTY[(x[i - 1], y[j - 1])] + memo[i-1][j-1], 
                GAP_PENALTY + memo[i-1][j],
                GAP_PENALTY + memo[i][j-1]
            )
    
    print(memo[len(x)][len(y)])


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
