i = 0
while True:
    try:
        s = raw_input()
    except EOFError:
        break
    for j,x in enumerate(s):
        if str.isdigit(x):
            print i,j,x,
    i = i+1
