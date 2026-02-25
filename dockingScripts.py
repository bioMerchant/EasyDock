from vina import Vina
import numpy as np
from Bio.PDB import PDBParser


# need to come up with a way for deaing with output files and results handling
class docking:
    def __init__(self,receptorPath:str, ligandPath:str, exhutivenessNumber:int, posesNumber:int ):
        self.receptor = receptorPath
        self.ligand = ligandPath
        self.exhustiveness = exhutivenessNumber
        self.poses = posesNumber
        self.vina = Vina(sf_name='vina')
        self.vina.set_receptor(receptorPath)
        self.vina.set_ligand_from_file(ligandPath)

    def getCoordinatesBlindDock(self):
        parser  = PDBParser(QUIET = True)
        structure = parser.get_structure('receptor',self.receptor)

        min_coords = np.inf
        max_coords = -np.inf

        for model in structure:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        coords = np.array(atom.coord)
                        min_coords = np.minimum(min_coords, coords)
                        max_coords = np.maximum(max_coords, coords)
        padding = 5.0
        centre = (min_coords + max_coords)/2
        size = (max_coords - min_coords) + 2 * padding

        return {
            'centre' : centre.tolist(),
            'box_size': np.ceil(size).tolist()
        }
    
    def dockBlind(self):
        outputFileName = ''

        center_size = self.getCoordinatesBlindDock() 
        center = center_size['centre']
        size = center_size['box_size']

        self.vina.compute_vina_maps(center = center, box_size=size)

        energy =  self.vina.score()
        
        blindDockOutput = 'Score before minimization: %.3f (kcal/mol)' % energy[0]

        energy_minimized = self.vina.optimize()
        blindDockOutput = blindDockOutput + '\n' + 'Score after minimization : %.3f (kcal/mol)' % energy_minimized[0]
        self.vina.write_pose(outputFileName, overwrite=True)

        self.vina.dock(exhaustiveness=self.exhustiveness,n_poses = self.poses)
        self.vina.write_poses(outputFileName,n_poses=self.poses, overwrite = True)
