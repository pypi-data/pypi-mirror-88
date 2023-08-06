from stkcage import *
import stk
from rdkit import Chem
from bash import BashCall
import re

b1=block("NC1CCCCC1N",[group["-NH2"]()]) #CHDNH2
b2=block("O=Cc1cc(C=O)cc(C=O)c1",[group["-CHO"]()])  # BTMCHO




print(GetParmsFromBOSS("/home/zhangkexin/software/boss",b1)[0])