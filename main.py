import StringGenerator as SG
import basic_3
import efficient_3

INPUT = "datapoints/in1.txt"
OUTPUT = ""
GAP_PENALTY = 0
MISMATCH_PENALTY = 0

def main():
    [x, y] = SG.generateStrings(INPUT)
    print(x)
    print(y)

if __name__ == "__main__":
    main()