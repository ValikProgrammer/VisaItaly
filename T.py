def getD(file="html/visa2022:06:05-10:27:42(+0300).html"):
    with open(file, "r") as file:
        text = file.read()
    return text

arr = getD().splitlines()
forbiddenS   = '<!-- Matomo Code -->'
forbiddenLen = 429

if (len(arr) == 429 and arr[5].strip() == s.strip()):
    print("fake html page! \nVisa : NO")
# for i in range(0,10):
#     print(f"{i} {arr[i]}")