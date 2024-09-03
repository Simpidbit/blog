from simblogpy.log import print_func_to_log

"""
    Args:
        argv: list. The list composed of strings to be processed.
    Returns:
        dict: Dictionary obtained through analysis.
"""
@print_func_to_log
def argv_parse_to_dict__dict(argv):
    """Parse the parameter list."""
    arglist = []
    option = ""
    for each in argv:
        if each[0] == '-':
            option = each
            continue

        if option != "":
            arglist.append([option, each])
            option = ""
        else:
            arglist.append(each)

    argdict = { "__ANONYMOUS": list() }
    for element in arglist:
        if isinstance(element, str):
            argdict["__ANONYMOUS"].append(element)
        elif isinstance(element, list):
            if len(element) == 2:
                if isinstance(element[0], str) and isinstance(element[1], str):
                    argdict[element[0]] = element[1]
                else:
                    raise TypeError(f"argv_analysis: Element of unexpected " + 
                                    f"type: {element}")
            else:
                raise IndexError(f"argv_analysis: Unexpected element: {element}")
    return argdict

