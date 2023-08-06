import importlib
def exists(varname):
    mod = importlib.import_module('main')

    varstring="mod."+varname # get variable from main code
    try:
        var=eval(varstring)
        return(True)
    except:
        return(False)
        
def get_var(varname):
    mod = importlib.import_module('main')
    varstring="mod."+varname # get variable from main code
    return(eval(varstring))

def check_size(a,b):
    if hasattr(b,"__len__") and  hasattr(a,"__len__"): # both arrays
        if len(a)==len(b): # size of arrays matches
            return True
        else: # mismatch in size
            return False
    elif not (hasattr(b,"__len__") or hasattr(a,"__len__")):# both scalars
        return True
    else:# mismatch in type
        return False

def check_value(a,b):
    from math import isclose
    if hasattr(b,"__len__") and  hasattr(a,"__len__"): # both arrays
        for x,y in zip (a,b):
            if isinstance(x,str) and isinstance(y,str):
                if not(x==y) : return False
            else:
                if not isclose(x,y,abs_tol=10**-5): return False
        return True
    else:
        if isinstance(a,str) and isinstance(b,str):
            return (a==b)
        else:
            return isclose(a,b,abs_tol=10**-7)

def check_vars(varname,expected):
    from AssCheck.variable_error_messages import print_error_message
    try:
        assert(exists(varname)), "existence"
        var=get_var(varname)
        assert(check_size(var,expected)), "size"
        assert(check_value(var,expected)), "value"
        print_error_message("success",varname)
    except AssertionError as error:
        print_error_message(error,varname)
        return(False)
    return(True)

def check_output(expected):
    from AssCheck.variable_error_messages import output_check
    return output_check(expected)
