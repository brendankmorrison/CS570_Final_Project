import StringGenerator

INPUT = "datapoints/in1.txt"

def main():
    [x, y] = StringGenerator.generateStrings(INPUT)
    print(x)
    print(y)

if __name__ == "__main__":
    main()