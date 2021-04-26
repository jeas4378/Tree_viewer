import sys
import re

valid_symbols = [')', '(', ',']


def parser(file):
    if file is None:
        return

    str_input = ""
    with open(file[1], 'r') as f:
        str_input = f.read()

    str_input = split_operation(str_input)
    print(str_input)


def split_operation(str_content):
    str_split = []
    current = 0
    end = 1
    bool_brackets = False

    for i in range(len(str_content)):
        if (str_content[i] in valid_symbols) and not bool_brackets:
            if (end - current) > 1:
                str_split.append(str_content[current: end])
            str_split.append(str_content[i])
            current = i + 1
            end = current
            continue
        elif str_content[i] == '[':
            if (end - current) > 1:
                str_split.append(str_content[current:end])
            current = i + 1
            end = current
            bool_brackets = True
            continue
        elif str_content[i] == ']':
            str_split.append(str_content[current:end])
            current = i + 1
            end = current
            bool_brackets = False
            continue
        else:
            end += 1
            continue

    return str_split


if __name__ == '__main__':
    parser(sys.argv)
