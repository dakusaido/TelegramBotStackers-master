from os import listdir
from os.path import isfile, join

mypath = "data/testFiles"


def gen_makups():
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(onlyfiles)


gen_makups()
