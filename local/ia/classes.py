import itertools

if __name__ == '__main__':
    fingers_possibilities = list(itertools.product([0, 1], repeat=5))
    print(fingers_possibilities)
    file = open('classes.txt', 'w')
    for item in fingers_possibilities:
        file.write(str(item))
        file.write("\n")
    file.close()
