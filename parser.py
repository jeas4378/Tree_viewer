
valid_symbols = [')', '(', ',']


def parser(host_file):
    """
    A parser for the PrimeTV-format. Returns one or two arrays with either Host- and Gene-tree combined or seperate.

    :param host_file: A file containing a host-tree on PrimeTV-format.
    :return: Returns two arrays containing the host-tree and reconciled gene-tree.
    """
    if host_file is None:
        return False

    with open(host_file, 'r') as f:
        str_host = f.read()

    arr_host = m_splitter(str_host)

    print(arr_host)
    return arr_host


def m_splitter(str_content):
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
        elif str_content[i] == ":":
            if (end - current) >= 1:
                str_split.append(str_content[current:end])
            current = i
            end = current
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


def is_numerical(val):

    if val[0] == ":":
        return True
    else:
        return False


def primetag_extractor(tag):

    tag_split = tag.split()
    tag_split.pop(0)

    id = None
    host_leaf = None
    AC = None
    name = None

    buffer = ""

    for element in tag_split:
        if element[0] == 'I':
            buffer = element[3:]
            id = buffer
        elif element[0] == 'A':
            buffer = element[4:len(element)]
            buffer = buffer.split()
            AC = buffer
        elif element[0] == 'S':
            buffer = element[2:]
            host_leaf = buffer
        elif element[0] == 'N':
            buffer = element[6:]
            name = buffer

    return id, host_leaf, AC, name



if __name__ == '__main__':
    parser('ex_host.txt')
