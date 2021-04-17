class cs:
    quit='\033[00m'
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    
    black='\033[30m'
    red='\033[31m' 
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    magenta='\033[35m'
    cyan='\033[36m'
    lgrey='\033[37m'
    dgrey='\033[90m'
    lred='\033[91m'
    lgreen='\033[92m'
    yellow='\033[93m'
    lblue='\033[94m'
    pink='\033[95m'
    lcyan='\033[96m'

#More used colors in functions
def red(str):
    return cs.red + str + cs.quit

def green(str):
    return cs.green + str + cs.quit

def blue(str):
    return cs.blue + str + cs.quit

def magenta(str):
    return cs.magenta + str + cs.quit

def yellow(str):
    return cs.orange + str + cs.quit

def lgrey(str):
    return cs.lgrey + str + cs.quit

def lcyan(str):
    return cs.lcyan + str + cs.quit

def lblue(str):
    return cs.lblue + str + cs.quit