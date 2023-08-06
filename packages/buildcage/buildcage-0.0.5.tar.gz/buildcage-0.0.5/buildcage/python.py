import stk

import stk

bb1 = stk.BuildingBlock('NCCCN', [stk.PrimaryAminoFactory()])
bb2 = stk.BuildingBlock(
    smiles='O=CC(C=O)CC=O',
    functional_groups=[stk.AldehydeFactory()],
)
tetrahedron = stk.cage.EightPlusTwelve((bb1, bb2))
cage1 = stk.ConstructedMolecule(tetrahedron)
cage1.write("test.mol")