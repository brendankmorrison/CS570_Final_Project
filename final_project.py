
fileName = "datapoints/in2.txt"
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

# Generate strings



print(x)
print(y)
print(arr1)
print(arr2)




# Read data into two strings
# input is two base strings and number of times they are repeates respectively