import subprocess


def BashCall(cmdline,sourcefile=None,EO=subprocess.PIPE):
    '''
    :param cmdline: cmd strings
    :param sourcefile: additional source file name
    :return: state code of that process
    '''
    if sourcefile==None:
        cmdline = ["bash", "-c", cmdline]
    else:
        cmdline = ["bash", "-c", "source "+sourcefile+";"+cmdline]
    return subprocess.call(cmdline,stderr=EO,stdout=EO)


