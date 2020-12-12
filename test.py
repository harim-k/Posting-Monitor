import difflib


diff = difflib.Differ()
a = "aaa\n"
b = "bbb"
print(diff.compare(a, b))

