from __future__ import print_function
import sys

def existence_error(varname):
    error_message="The variable " + varname +" does not exist" +"""
    Ensure you have named the variable properly,
    bearing in mind that capital letters matter.
    """
    return(error_message)

def size_error(varname):
    error_message="The variable " + varname +" is the wrong size" +"""
    Try using len(...) to determine the size of the array, or print(...)
    to check the values look as you expect them to.
    """
    return(error_message)

def value_error(varname):
    error_message="The variable " + varname +" has the wrong value(s)" +"""
    Try using print(...) to check the values look as you expect them to, and 
    ensure the expression used to calculate the variable is correct.
    """
    return(error_message)

def import_error():
    error_message="your code failes to execute" +"""
    Please refer to the error messages printed in the terminal to resolve
    any errors in your code.
    """
    return(error_message)

def print_error_message(error,varname):
    from AssCheck.bcolors import bcolors

    if (str(error)=="success"):
        print(f"{bcolors.OKGREEN}Variable {varname} is correct!\n{bcolors.ENDC}")

    else:
        if (str(error)=="existence"):
            emsg=existence_error(varname)
        elif (str(error)=="size"):
            emsg=size_error(varname)
        elif (str(error)=="value"):
            emsg=value_error(varname) 
        elif (str(error)=="import"):
            emsg=import_error()
        else:
            emsg("something not right with "+varname)
        print(f"{bcolors.FAIL}{emsg}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}")


def output_check(expected):
    import subprocess
    import sys
    from AssCheck.bcolors import bcolors

    def run(cmd):
        proc = subprocess.Popen(cmd,
            stdout = subprocess.PIPE,
            )
        stdout = proc.communicate()

        return  stdout

    out= run([sys.executable, 'main.py'])
    screen_out=str(out).split("'")[1].strip("\\n")   

    check = screen_out==expected

    errmsg="The text printed to screen is not correct. Ensure you have printed the correct variables, in the correct order, and that nothing else is printed."

    if not (check):
        print(f"{bcolors.FAIL}test_output has failed. \n{errmsg}")
    else:
        print(f"{bcolors.OKGREEN}Printing is correct!\n")

    print(f"{bcolors.WARNING}{30*'='}\n{bcolors.ENDC}")

    return check
    
