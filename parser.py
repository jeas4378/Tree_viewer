
valid_symbols = [')', '(', ',']


def parser(file, bool_separate=False):
    """
    A parser for the PrimeTV-format. Returns one or two arrays with either Host- and Gene-tree combined or seperate.

    :param file: A file on PrimeTV-format to be parsed.
    :param bool_separate: If True the Host-tree and Gene-tree will be returned separately.
    :return: If bool_seperate is True then Host- and Gene-tree will be returned separately. Otherwise one array will
    be returned with Host- and Gene-tree combined.
    """
    if file is None:
        return False

    with open(file, 'r') as f:
        str_input = f.read()

    str_input = split_operation(str_input)

    if bool_separate:
        arr_host, arr_gene = host_gene_retriever(str_input, True, True)
        print(arr_host)
        print(arr_gene)
        return arr_host, arr_gene

    return str_input


def split_operation(str_content):
    """
    A function that does the actual splitting by going through 'str_content' and splitting it accordingly into an
    array.
    :param str_content: A String with content in PrimeTV-format.
    :return: An Array with the splitted result.
    """
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


def host_gene_retriever(arr_input, bool_host, bool_gene):
    """
    A function that splits the Host- and Gene-tree and returns them both seperately or just one or the other.
    :param arr_input: An Array containing the material from the PrimeTV-format.
    :param bool_host: A Boolean which if True results in returning the Host-tree.
    :param bool_gene: A Boolean which if True results in returning the Gene-tree.
    :return: One or Two arrays depending on the truth-values of 'bool_host' and 'bool_gene'.
    """

    arr_host = []
    arr_gene = []

    for element in arr_input:
        if element[0] == "&":
            arr_gene.append(element)
        else:
            arr_host.append(element)

    if bool_host:
        if bool_gene:
            return arr_host, arr_gene
        else:
            return arr_host
    else:
        return arr_gene


if __name__ == '__main__':
    parser('ex_data.txt', True)
