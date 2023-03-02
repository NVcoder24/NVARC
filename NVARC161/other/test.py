import json

arr = []
string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(len(string)):
    arr.append(string[i])

print(json.dumps(arr))