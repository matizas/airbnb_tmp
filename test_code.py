import re
str1 = 'User.update("id", "name", "Paschal")'
str2 = "User.update(id, {'age':30})"
pattern = "^(?P<cls_name>[a-zA-Z]+)\.(?P<method_name>[a-zA-Z]+)\((?P<args>.*)\)"

test = re.match(pattern, str2)
st = [test.group("cls_name"), test.group("method_name"), test.group("args")]
[cn, mn, args] = st


def args_update_parser(args_list):
    _list = [None] * 3
    [id, *rest] = args_list
    attr_name = ""
    attr_value = ""
    id = id.strip("'\"")
    _list[0] = id

    if len(rest) == 2:
        [attr_name, attr_value] = rest
        attr_name = attr_name.strip("'\" ")
        attr_value = attr_value.strip(" ")

    elif len(rest) == 1:
        arg2 = rest[0]
        [attr_name, attr_value] = arg2.split(":")
        attr_name = attr_name.strip("{'\" ")
        attr_value = attr_value.strip("} ")

    _list[1] = attr_name
    _list[2] = attr_value
    return _list


print(args_update_parser(args.split(","))[2])
