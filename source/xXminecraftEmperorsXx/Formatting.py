import ast


def tuple_to_string(tupl):
    separator = ", "
    tuple_list = []

    for element in tupl:
        tuple_list.append(str(element))

    string = "(" + separator.join(tuple_list) + ")"
    return string


def string_to_tuple(string):
    # literal_eval takes a string and duck types it
    tupl = ast.literal_eval(string)
    return tupl

#takes two tuples of the same length and subtracts each element. zip returns an iterator
def tuple_dif(t1, t2):
    return tuple([x-y for x, y in zip(t1,t2)])

#converts q,r into q,r,s
def tuple2throuple(t):
    return (*t,-(t[0]+t[1]))

def throuple2tuple(t):
    return t[:2]