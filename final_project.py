
fileName = "datapoints/in1.txt"
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


print("base x: " + x)
print(arr1)
print("base y: " + y)
print(arr2)
# Generate string x
for index in arr1:
    x = x[:index + 1] + x + x[index + 1:]

x = x.replace(' ', '').replace('\n', '')

for index in arr2:
    y = y[:index + 1] + y + y[index + 1:]

y = y.replace(' ', '').replace('\n', '')

print(x)
print(y)





# Read data into two strings
# input is two base strings and number of times they are repeates respectively