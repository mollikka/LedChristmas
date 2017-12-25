import re

x_list = []
y_list = []
z_list1 = []
z_list2 = []

with open("scaled_cam1.txt") as file1:
    for line in file1.readlines():
        x,z = re.findall(r"\d+.\d+",line)
        x_list.append(float(x))
        z_list1.append(float(z))

with open("scaled_cam2.txt") as file2:
    for line in file2.readlines():
        y,z = re.findall(r"\d+.\d+",line)
        y_list.append(float(y))
        z_list2.append(float(z))

z_list = [(z_list1[i] + z_list2[i]) /2 for i in range(len(z_list1))]

print("XCOORD[",len(x_list),"] = {")
for i in x_list:
    print(i,",")
print("};")

print("YCOORD[",len(y_list),"] = {")
for i in y_list:
    print(i,",")
print("};")

print("ZCOORD[",len(z_list),"] = {")
for i in z_list:
    print(i,",")
print("};")
