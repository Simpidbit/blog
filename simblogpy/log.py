LOGFILE_PATH = ".\\client.log"

with open(LOGFILE_PATH, "a") as f:
    f.write("\n\n################### NEW BEGINNING ##################\n\n")

def printlog(s):
    with open(LOGFILE_PATH, "a") as f:
        f.write(s + '\n')

# This is a decorator function
def print_func_to_log(func):
    def wrapper(*args, **kwargs):
        if func.__doc__ is None:
            raise Exception(f"print_to_log: Function without documentation:" +
                            f" {func.__name__}")
        else :
            printlog(f"================= {func.__name__} begin =================")
            printlog(f"About to enter the function: {func.__name__}")
            printlog(f"The documentation of the function: {func.__doc__}")
            printlog(f"Real parameters: {args}, {kwargs}")
            result = func(*args, **kwargs)
            printlog(f"Return value: {result}")
            printlog(f"The function finishes.")
            printlog(f"================= {func.__name__} end =================")
            return result
    return wrapper

