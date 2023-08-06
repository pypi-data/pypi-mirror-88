import argparse
from buildcage.src.readjson import ArgsFromJson
from buildcage.src.boss import GetParmsFromBOSS
from buildcage.src.stkcage import *
from buildcage.src.lmp import write_oplsaa_opt

parser=argparse.ArgumentParser(prog='buildcage')
parser.add_argument("json",help="Cage definition json file")
parser.add_argument("--MMFF",action='store_true',help="Wheter to start a MMFF optimization initially")
parser.add_argument("--simp",action='store_true',help="Wheter to hide lammps process!")
parser.add_argument("--pair",action='store_true',help="Wheter to include pair interactions during minimization")
args=parser.parse_args()

def main():
    config=ArgsFromJson(args.json)
    config_block=config["cage"]["blocks"]
    MMFFflag=True if args.MMFF else False
    Pairflag=True if args.pair else False
    EOflag=True if args.simp else False
    write_oplsaa_opt(config["name"],config_block[0],config_block[1],config["cage"]["topology"],
                     Pairflag,MMFFflag,"\n".join(config["MDArgs"]),config["LMPexe"],config["BOSSdir"],EOflag)
if __name__=="__main__":
    main()
    pass

