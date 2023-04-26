with open('normdocx.txt') as old, open('newdocx.txt', 'w') as new:
    lines = old.readlines()
    new.writelines(lines[2:-1])