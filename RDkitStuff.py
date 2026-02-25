from rdkit import Chem
from rdkit.Chem import Draw
import tkinter
from PIL import Image, ImageTk


class SMILESdraw:   
    def __init__(self, SMILES : str):
        self.SMILESstring = SMILES

    def drawFromSMILES(self):
        mol = Chem.MolFromSmiles(self.SMILESstring)
        size = (300,300)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {self.SMILESstring}")

        img = Draw.MolToImage(mol,size=size)

        photo = ImageTk.PhotoImage(img)
        return photo
