import rdkit.Chem as Chem
from collections import Counter
import re
import copy
import numpy as np
from .stkcage import *
from .molecule import molecule
from .bash import BashCall
from .boss import GetParmsFromBOSS
import subprocess


def add_s(i):
    if len(i)==1:
        return i+" "
    else:
        return i

def OPLSAA_parm(strs,parm,improper=False):
    if improper==False:
        strs1=[add_s(i) for i in strs]
        s=['-'.join(strs1).strip(),'-'.join(strs1[::-1]).strip()]
        strs2 =copy.deepcopy(strs1)
        strs2[0]=strs2[0][0]+".?"
        strs2[-1] = strs2[-1][0] + ".?"
        ss = ['-'.join(strs2).strip(), '-'.join(strs2[::-1]).strip()]
        len_type={2:parm[1],3:parm[2],4:parm[3]}
        for i in s:
            if i in len_type[len(strs)]:
                return len_type[len(strs)][i]
            else:
                for i in ss:
                    for j in len_type[len(strs)]:
                        if len(re.findall(i,j)) ==1:
                            return len_type[len(strs)][j]
    elif improper==True:
        if strs[0]=="CA":
            return "1.100  0.0"
        elif strs[0][0]=="N":
            return "1.000  0.0"
        elif strs[0]=="CM" and "O" not in [strs[1][0],strs[2][0],strs[3][0]]:
            return "15.00  0.0"
        elif strs[0][0]=="C":
            return "10.50  0.0"

def useless_atom_set(b):
    gs=list(b.get_functional_groups())
    uas=set()
    for i in gs:
        uas=uas|(set(i.get_atom_ids())-set(i.get_core_atom_ids()))
    return uas
def bonder_atom_set(b):
    gs=list(b.get_functional_groups())
    uas=set()
    for i in gs:
        uas=uas|set(i.get_placer_ids())
    return uas

def useful_ids(b):
    return [i for i in range(len(b.to_rdkit_mol().GetAtoms())) if i not in useless_atom_set(b)]




symb2mass = {
        'H': 1.008,
        'F': 18.998403163,
        'Cl': 35.45,
        'Br': 79.904,
        'I': 126.90447,
        'O': 15.999,
        'S': 32.06,
        'N': 14.007,
        'P': 30.973761998,
        'C': 12.011,
        'Si': 28.085,
        'Na': 22.98976928,
        'SOD': 22.98976928,
        'K': 39.0983,
        'Mg': 24.305,
        'Ca': 40.078,
        'Mn': 54.938044,
        'Fe': 55.845,
        'Co': 58.933194,
        'Ni': 58.6934,
        'Cu': 63.546,
        'Zn': 65.38, }

name="test"
Pairflag=True
MMFFflag=True
MDArgs=""
LMPexe="/home/zhangkexin/software/lammps/src/lmp_gnu"
BOSSdir="/home/zhangkexin/software/boss"
block1=["NCCCCN","-NH2"]
block2=["O=Cc1cc(C=O)cc(C=O)c1","-CHO"]
topology="2+3"

def write_oplsaa_opt(name,block1,block2,topology,Pairflag,MMFFflag,MDArgs,LMPexe,BOSSdir,EOflag):
    if block1[0].split(".")[-1]=="mol":
        b1=block_file(block1[0],[group[block1[1]]()])
    else:
        b1=block(block1[0],[group[block1[1]]()])
    if block2[0].split(".")[-1]=="mol":
        b2=block_file(block2[0],[group[block2[1]]()])
        b3 = block_file(block2[0], [group[block2[1]]()])
    else:
        b2=block(block2[0],[group[block2[1]]()])
        b3 = block(block2[0], [group[block2[1]]()])

    cageobj=cage(topology,(b1,b2),MMFFopt=MMFFflag)
    with open(name+"_init.mol","w") as f:
        print(Chem.MolToMolBlock(Chem.MolFromMolBlock(mol_block(cageobj.frame),removeHs=False)),file=f)
    b3._placer_ids=b3._placer_ids[:2]
    b3._functional_groups=b3._functional_groups[:2]   # 这里改变内定的值, 已经无法再用于build了, 所以build cage需要靠前.
    fra=stk.BuildingBlock.init_from_molecule(build_framework(stk.polymer.Linear((b1,b3),"AB",1),MMFFopt=True),
                                             functional_groups=[group[block1[1]](),group[block2[1]]()])
    parameters=GetParmsFromBOSS(BOSSdir,fra)
    print("1. Get oplsaa parameters from BOSS successfully!")
    ub1=useful_ids(b1)
    ub2=useful_ids(b2)
    uf=useful_ids(fra)
    bb1=bonder_atom_set(b1)
    bb2=bonder_atom_set(b2)
    bf=bonder_atom_set(fra)

    b1type_dict=dict()
    b2type_dict=dict()
    for id,i in enumerate(ub1):
        if i in bb1 and uf[id] not in bf:
            b1bondtype=parameters[0][uf[id]]
            break
    else:
        print("No bond atom find!")
        raise IOError

    for id, i in enumerate(ub1):
        if i in bb1:
            b1type_dict[id]=b1bondtype
        else:
            b1type_dict[id]=parameters[0][uf[id]]

    for id,i in enumerate(ub2):
        if i in bb2 and uf[id+len(ub1)] not in bf:
            b2bondtype=parameters[0][uf[id+len(ub1)]]
            break
    else:
        print("No bond atom find!")
        raise IOError

    for id, i in enumerate(ub2):
        if i in bb2:
            b2type_dict[id]=b2bondtype
        else:
            b2type_dict[id]=parameters[0][uf[id+len(ub1)]]

    # for i in b2type_dict:
    #     print(i)
    b1chargedict=dict()
    for i in b1type_dict:
        try:
            b1chargedict[b1type_dict[i][0]]+=[float(b1type_dict[i][1])]
        except:
            b1chargedict[b1type_dict[i][0]]= [float(b1type_dict[i][1])]
    for i in b1chargedict:
        b1chargedict[i]=sum(b1chargedict[i])/len(b1chargedict[i])
    for i in b1type_dict:
        b1type_dict[i][1]=str(b1chargedict[b1type_dict[i][0]])

    b2chargedict=dict()
    for i in b2type_dict:
        try:
            b2chargedict[b2type_dict[i][0]]+=[float(b2type_dict[i][1])]
        except:
            b2chargedict[b2type_dict[i][0]]= [float(b2type_dict[i][1])]
    for i in b2chargedict:
        b2chargedict[i]=sum(b2chargedict[i])/len(b2chargedict[i])
    for i in b2type_dict:
        b2type_dict[i][1]=str(b2chargedict[b2type_dict[i][0]])


    b1num=int(eval(topology)/5*3)
    b2num=int(eval(topology)/5*2)
    atoms_all=[]
    for i in range(b2num):
        for j in range(len(b2type_dict)):
            atoms_all.append(b2type_dict[j])
    for i in range(b1num):
        for j in range(len(b1type_dict)):
            atoms_all.append(b1type_dict[j])


    mean_q=sum(float(i[1]) for i in atoms_all)/len(atoms_all)
    for i in atoms_all:
        i[1]=str(float(i[1])-mean_q)
    type_dict={i:atoms_all[i][0] for i in range(len(atoms_all))}

    cage_mol=cageobj.frame.to_rdkit_mol()
    cage_mol_m=molecule(cage_mol)
    atoms=len(cage_mol_m.atoms_idx)
    bonds=len(cage_mol_m.bonds_idx)
    angles=len(cage_mol_m.angles_idx)
    dihedrals=len(cage_mol_m.dihedrals_idx)
    impropers=len(cage_mol_m.impropers_idx)

    # write lammps input files

    f=open(name+".data","w")
    print("LAMMPS "+name+" CAGE",file=f)
    print(atoms,"atoms\n",bonds,"bonds\n",angles,"angles",file=f)
    print(dihedrals,"dihedrals\n",impropers,"impropers\n",file=f)
    print(atoms, "atom types\n", bonds, "bond types\n", angles, "angle types",file=f)
    print(dihedrals, "dihedral types\n",impropers, "improper types\n",file=f)
    print("-100 100  xlo xhi\n-100 100 ylo yhi\n-100 100 zlo zhi",file=f)
    print("\nMasses\n",file=f)
    for i,atom in enumerate(cage_mol.GetAtoms()):
        print(i+1,symb2mass[atom.GetSymbol()],file=f)
    print("\nAtoms\n",file=f)
    position=cage_mol.GetConformer().GetAtomPosition
    for i in range(atoms):
        print(i+1,1,i+1,atoms_all[i][1],position(i)[0],position(i)[1],position(i)[2],file=f)

    if Pairflag:
        print("\nPair Coeffs\n",file=f)
        for i in range(atoms):
            print(i + 1, atoms_all[i][3],atoms_all[i][2],file=f)
    print("\nBond Coeffs\n",file=f)
    for id,i in enumerate(cage_mol_m.bonds_idx):
        print(id+1, *OPLSAA_parm([type_dict[i[0]], type_dict[i[1]]], parameters)[::-1],"#", type_dict[i[0]]+"-"+type_dict[i[1]],file=f)
    print("\nAngle Coeffs\n",file=f)
    for id,i in enumerate(cage_mol_m.angles_idx):
        print(id+1, *OPLSAA_parm([type_dict[i[0]], type_dict[i[1]], type_dict[i[2]]], parameters)[::-1],
              "#", type_dict[i[0]]+"-"+type_dict[i[1]]+"-"+type_dict[i[2]],file=f)
    print("\nDihedral Coeffs\n",file=f)
    for id,i in enumerate(cage_mol_m.dihedrals_idx):
        print(id+1, OPLSAA_parm([type_dict[i[0]], type_dict[i[1]], type_dict[i[2]],type_dict[i[3]]], parameters),
              "#", type_dict[i[0]]+"-"+type_dict[i[1]]+"-"+type_dict[i[2]]+"-"+type_dict[i[3]],file=f)
    print("\nImproper Coeffs\n",file=f)
    for id,i in enumerate(cage_mol_m.impropers_idx):
        print(id+1, OPLSAA_parm([type_dict[i[0]], type_dict[i[1]], type_dict[i[2]],type_dict[i[3]]], parameters,improper=True),
              "#", type_dict[i[0]]+"-"+type_dict[i[1]]+"-"+type_dict[i[2]]+"-"+type_dict[i[3]],file=f)
    print("\nBonds\n",file=f)
    for id,i in enumerate(cage_mol_m.bonds_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,file=f)
    print("\nAngles\n",file=f)
    for id,i in enumerate(cage_mol_m.angles_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,i[2]+1,file=f)
    print("\nDihedrals\n",file=f)
    for id,i in enumerate(cage_mol_m.dihedrals_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,i[2]+1,i[3]+1,file=f)
    print("\nImpropers\n",file=f)
    for id,i in enumerate(cage_mol_m.impropers_idx):
        print(id+1,id+1,i[0]+1,i[1]+1,i[2]+1,i[3]+1,file=f)
    f.close()
    f = open(name+".in", 'w')
    print("units real\nboundary f f f\natom_style full\nbond_style harmonic\nangle_style harmonic\ndihedral_style opls\n"
          "improper_style harmonic",file=f)
    if Pairflag:
        print("pair_style lj/cut/coul/cut 14.0 14.0\nspecial_bonds lj/coul 0.0 0.0 0.5\npair_modify mix geometric",file=f)
    print('read_data "'+name+'.data"', file=f)
    print('neighbor 6 bin\nneigh_modify every 1 delay 0 check yes\nthermo 100', file=f)
    print(MDArgs,file=f)
    print("#dump 1 all movie 1 movie.mp4 type type size 640 480 zoom 10\ndump 2 all custom 1 dump.lammpstrj id mass x y z", file=f)
    print('minimize 1.0e-5 1.0e-7 10000 100000\ntimestep 1', file=f)
    f.close()

    print("2. Write lammps input files successfully")
    if EOflag:
        EO=None
    else:
        EO=subprocess.PIPE
    BashCall(LMPexe+" < "+name+".in",EO=None)
    with open("dump.lammpstrj",'r') as f:
        coors=f.readlines()[-atoms:]
    coor_mat=[[0. for j in range(atoms)]for i in range(3)]
    for i in coors:
        coor_mat[0][int(i.split()[0])-1]=float(i.split()[2])
        coor_mat[1][int(i.split()[0]) - 1] = float(i.split()[3])
        coor_mat[2][int(i.split()[0]) - 1] = float(i.split()[4])
    cageobj.frame._position_matrix=np.array(coor_mat)

    with open(name+"_opt.mol","w") as f:
        print(Chem.MolToMolBlock(Chem.MolFromMolBlock(mol_block(cageobj.frame),removeHs=False)),file=f)
    BashCall("rm -f log.lammps {0}.data {0}.in dump.lammpstrj log".format(name))
    print("3. Write optimized cage mdp file from lammps output successfully!!!!\nEND!!!")
