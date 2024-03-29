
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
    bool_brackets = False

    for i in range(len(str_content)):
        if (str_content[i] in valid_symbols) and not bool_brackets:
            if (i - current) > 1:
                str_split.append(str_content[current: i])
            str_split.append(str_content[i])
            current = i + 1
            continue
        elif str_content[i] == ":":
            if (i - current) >= 1:
                str_split.append(str_content[current:i])
            current = i
        elif str_content[i] == '[':
            if (i - current) > 1:
                str_split.append(str_content[current:i])
            current = i + 1
            bool_brackets = True
            continue
        elif str_content[i] == ']':
            str_split.append(str_content[current:i])
            current = i + 1
            bool_brackets = False
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
    """
    A function that checks if the upcoming value is numerical.

    :param val: A String to be checked.
    :return: A boolean.
    """

    if val[0] == ":":
        return True
    else:
        return False


def primetag_extractor(node, tag):
    """
    Exctracts the information from a Prime-tag and assigns it to a Node-object.

    :param node: A node-object to which the information in the Prime-tag will be assigned.
    :param tag: The Primetag containing the information.
    :return: None.
    """

    tag_split = my_prime_splitter(tag)
    tag_split.pop(0)

    id = None
    host_leaf = None
    AC = None
    name = None

    buffer = ""

    for element in tag_split:
        if element[0] == 'I':
            buffer = element[3:]
            node.set_id(buffer)
        elif element[0] == 'A':
            buffer = element[4:-1]
            buffer = buffer.split()
            node.set_ac(buffer)
        elif element[0] == 'S':
            buffer = element[2:]
            node.set_host_leaf(buffer)
        elif element[0] == 'N':
            buffer = element[6:]
            node.set_name(buffer)

def my_prime_splitter(val):
    """
    Takes a Primetag as a String and splits out all the information as elements into an array.

    :param val: The Primetag as a String.
    :return: An Array with all the information in the Primetag as elements.
    """

    result = []
    bracket = 0
    current = 0

    for i in range(1, len(val)):
        if val[i] == ' ' and bracket == 0:
            result.append(val[current:i])
            current = i + 1

        elif val[i] == '(':
            bracket += 1

        elif val[i] == ')':
            bracket -= 1

    result.append(val[current:])

    return result


def is_valid_symbols(val):
    """
    Checks if a value is in the list 'valid symbols' up top.

    :param val: A character to be checked.
    :return: A boolean.
    """

    if val in valid_symbols:
        return True
    else:
        return False

if __name__ == '__main__':
    parser('ex_host.txt')
