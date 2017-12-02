import sys

# Get script parameters:
# all list items after the last occurence of "--"
print()
print(sys.argv)
print()

try:
    args = list(reversed(sys.argv))
    idx = args.index("--")

except ValueError:
    params = []

else:
    params = args[:idx][::-1]

print("Script params:", params)
