from vina import Vina
import numpy as np
from Bio.PDB import PDBParser
from fpdf import FPDF
import os


# need to come up with a way for deaing with output files and results handling
class docking:
    def __init__(self,receptorPath:str, ligandPath:str, exhutivenessNumber:int, posesNumber:int ):
        self.receptor = receptorPath
        self.ligand = ligandPath
        self.exhustiveness = exhutivenessNumber
        self.poses = posesNumber
        self.vina = None


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
        self.vina = Vina(sf_name='vina')
        self.vina.set_receptor(self.receptor)
        self.vina.set_ligand_from_file(self.ligand)
    
    
        output_filename = 'docked_poses.pdbqt'
        output_path = os.path.join(self.output_folder, output_filename)
        pdf_path = os.path.join(self.output_folder, "docking_report.pdf")
    
        center_size = self.getCoordinatesBlindDock() 
        center = center_size['centre']
        size = [min(30, s) for s in center_size['box_size']]  # Safety cap
    
        self.vina.compute_vina_maps(center=center, box_size=size)
        energy = self.vina.score()
        blindDockOutput = f'Score before minimization: {energy[0]:.3f} (kcal/mol)'
    
        energy_minimized = self.vina.optimize()
        blindDockOutput += f'\nScore after minimization: {energy_minimized[0]:.3f} (kcal/mol)'
    
    
        self.vina.write_pose(output_path, overwrite=True)
        self.vina.dock(exhaustiveness=self.exhustiveness, n_poses=self.poses)
        self.vina.write_poses(output_path, n_poses=self.poses, overwrite=True)
    
    # Create PDF report
        self.create_docking_pdf(pdf_path, blindDockOutput, center, size, self.exhustiveness, self.poses)
    
        print(f"✓ Docking complete!")
        print(f"  Output: {output_path}")
        print(f"  Report: {pdf_path}")

    def create_docking_pdf(self, pdf_path, results_text, center, size, exhaustiveness, poses):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=24, style="B")
        pdf.cell(200, 20, txt="Molecular Docking Report", ln=1)
    
        pdf.ln(10)
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="Blind Docking Results", ln=1)
    
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=results_text)
    
        pdf.ln(5)
        pdf.set_font("Arial", size=12, style="B")
        pdf.cell(200, 10, txt="Docking Parameters", ln=1)
    
        params = f"""
        Center: X={center[0]:.3f}, Y={center[1]:.3f}, Z={center[2]:.3f}
        Box Size: {size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f} Å
        Exhaustiveness: {exhaustiveness}
        Number of poses: {poses}
        Output file: docked_poses.pdbqt
        """
        pdf.multi_cell(0, 8, txt=params)
    
        pdf.output(pdf_path)