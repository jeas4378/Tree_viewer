import sys


def parser(file):
    if file is None:
        return

    str_input = ""
    with open(file[1], 'r') as f:
        str_input = f.read()

    




if __name__ == '__main__':
    parser(sys.argv)
