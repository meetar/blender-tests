import sys
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

print(argv)  # --> ['example', 'args', '123']