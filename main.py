import customtkinter as ctk
from tkinter import filedialog
import os

import dockingScripts
import babelConverter
import RDkitStuff


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme('blue')


import customtkinter as ctk
from tkinter import filedialog

class UserInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title('EasyDock')
        self.geometry('900x500')
        
        #//////////////////////////////////////////////////////////////////////////////// Create tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, fill="both", expand=True)

        #//////////////////////////////////////////////////////////////////////////////// Tab 1: File converter 
        
        FileConverterTab = self.tabview.add("Convert pdb to pdbqt")    
        self.converter_frame = ctk.CTkFrame(FileConverterTab)
        self.converter_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Input PDB selector
        ctk.CTkLabel(self.converter_frame, text="Input PDB file:").pack(pady=(10, 5))
        self.input_frame = ctk.CTkFrame(self.converter_frame)
        self.input_frame.pack(fill="x", padx=20, pady=5)

        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="No file selected")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        ctk.CTkButton(self.input_frame, text="Browse Input", 
              command=self.select_input_pdb).pack(side="right", padx=10, pady=10)

# Output folder selector
        ctk.CTkLabel(self.converter_frame, text="Output folder:").pack(pady=(20, 5))
        self.output_frame = ctk.CTkFrame(self.converter_frame)
        self.output_frame.pack(fill="x", padx=20, pady=5)

        self.output_entry = ctk.CTkEntry(self.output_frame, placeholder_text="Select output folder")
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        ctk.CTkButton(self.output_frame, text="Browse Folder", 
              command=self.select_output_folder).pack(side="right", padx=10, pady=10)

# Output filename
        ctk.CTkLabel(self.converter_frame, text="Output filename (without .pdbqt):").pack(pady=(10, 5))
        self.output_filename_entry = ctk.CTkEntry(self.converter_frame, placeholder_text="converted")
        self.output_filename_entry.pack(fill="x", padx=20, pady=5)

# Convert slow button
        ctk.CTkButton(self.converter_frame, text="Convert to PDBQT",command=self.convert_file).pack(pady=(20,5))

#Convert fast button
        ctk.CTkButton(self.converter_frame, text="Convert to PDBQT (faster no hydrogens)",command=self.convert_fileFast).pack(pady=(20,5))

        #//////////////////////////////////////////////////////////////////////////////// Tab 2: Smiles to visualize 
        SMILEVisualizeTab = self.tabview.add("SMILES visualizer")
        self.SMILESVFrame = ctk.CTkFrame(SMILEVisualizeTab)
        self.SMILESVFrame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.SMILESVFrame, text = 'Input SMILES for conversion or visulaization').pack(pady=(10, 5))
        self.InputSMILES = ctk.CTkEntry(self.SMILESVFrame, placeholder_text= 'SMILES')
        self.InputSMILES.pack(fill="x", padx=20, pady=5)

        self.SMILESButtonVisualize = ctk.CTkButton(
        self.SMILESVFrame, 
        text='Show structure',
        command=self.show_SMILES
        )
        self.SMILESButtonVisualize.pack(pady=10)

        #//////////////////////////////////////////////////////////////////////////////// Tab 3: Smiles to PDBQT 
        SMILESconverterTab = self.tabview.add('Convert SMILES to PDBQT')
        self.smilesConverterFrame = ctk.CTkFrame(SMILESconverterTab)
        self.smilesConverterFrame.pack(fill='x', padx = 20 , pady = 5)

        #label and input for SMILES 
        ctk.CTkLabel(self.smilesConverterFrame, text = "Input SMILES:").pack(pady = (10,5))
        self.SMILESInputforconv = ctk.CTkEntry(self.smilesConverterFrame)
        self.SMILESInputforconv.pack(fill="x", expand=True, padx=(10, 10), pady=10)

        #label and input for SMILES pdbqt with button
        ctk.CTkLabel(self.smilesConverterFrame, text = "Select File destination for output:").pack(pady = (20,5))

        self.input_entry_SMILES_dest = ctk.CTkEntry(self.smilesConverterFrame, placeholder_text="No file selected")
        self.input_entry_SMILES_dest.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        ctk.CTkButton(self.smilesConverterFrame, text="Browse output destination", 
              command=self.select_output_folder).pack(padx=10, pady=10)
        
        # Convert smiles button
        ctk.CTkButton(self.smilesConverterFrame, text="Convert to PDBQT",command=self.convert_file).pack(pady=(20,5))



        #//////////////////////////////////////////////////////////////////////////////// Tab 4: Quick Blind Dock - File selectors
        QuickBlindDockTab = self.tabview.add("Quick Blind Dock")
        
        # File selection frame INSIDE the tab
        self.files_frame = ctk.CTkFrame(QuickBlindDockTab)
        self.files_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Receptor file selector
        ctk.CTkLabel(self.files_frame, text="Receptor (.pdbqt):").pack(pady=10)
        self.receptor_frame = ctk.CTkFrame(self.files_frame)
        self.receptor_frame.pack(fill="x", padx=20, pady=5)
        
        self.receptor_entry = ctk.CTkEntry(self.receptor_frame, placeholder_text="No file selected")
        self.receptor_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        
        ctk.CTkButton(self.receptor_frame, text="Browse", 
                     command=self.select_receptor).pack(side="right", padx=10, pady=10)
        
        # Ligand file selector  
        ctk.CTkLabel(self.files_frame, text="Ligand (.pdbqt):").pack(pady=10)
        self.ligand_frame = ctk.CTkFrame(self.files_frame)
        self.ligand_frame.pack(fill="x", padx=20, pady=5)
        
        self.ligand_entry = ctk.CTkEntry(self.ligand_frame, placeholder_text="No file selected")
        self.ligand_entry.pack(side="left", fill="x", expand=True, padx=(10, 10), pady=10)
        
        ctk.CTkButton(self.ligand_frame, text="Browse", 
                     command=self.select_ligand).pack(side="right", padx=10, pady=10)
        
        #///////////////////////////////////////////////////////////////////////////////// Tab 5: Multidock
        MultiDock = self.tabview.add("Dock ligand to multipe targets")
        ctk.CTkLabel(MultiDock, text="Advanced options will go here").pack(pady=50)
        ctk.CTkButton(MultiDock, text="Test Button", 
                     command=lambda: print("Advanced tab clicked")).pack(pady=10)
    

#//////////////////////////////////////////////////////////////////////////////////////// Functions
    def select_receptor(self):
        filename = filedialog.askopenfilename(
            title="Select Receptor (.pdbqt)",
            filetypes=[("PDBQT files", "*.pdbqt"), ("All files", "*.*")]
        )
        if filename:
            self.receptor_entry.delete(0, "end")
            self.receptor_entry.insert(0, filename)
    
    def select_ligand(self):
        filename = filedialog.askopenfilename(
            title="Select Ligand (.pdbqt)", 
            filetypes=[("PDBQT files", "*.pdbqt"), ("All files", "*.*")]
        )
        if filename:
            self.ligand_entry.delete(0, "end")
            self.ligand_entry.insert(0, filename)
    
    def select_input_pdb(self):
        filename = filedialog.askopenfilename(
        title="Select PDB file",
        filetypes=[("PDB files", "*.pdb"), ("All files", "*.*")]
        )
        if filename:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, filename)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)
    
    def select_output_folder_SMILESPDBQT(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.input_entry_SMILES_dest.delete(0, "end")
            self.input_entry_SMILES_dest.insert(0, folder)


    def convert_file(self):
        input_path = self.input_entry.get()
        output_folder = self.output_entry.get()
        filename = self.output_filename_entry.get() or "converted"
    
        if not input_path or not output_folder:
            print("Please select input file and output folder")
            return
    
        output_path = os.path.join(output_folder, f"{filename}.pdbqt")
    
        converter = babelConverter.ObabelConverter(input_path, output_path)
        success, result = converter.convert()
    
        if success:
            print(f"✓ Saved to: {result}")
        else:
            print("✗ Conversion failed")

    def convert_fileFast(self):
        input_path = self.input_entry.get()
        output_folder = self.output_entry.get()
        filename = self.output_filename_entry.get() or "converted"
    
        if not input_path or not output_folder:
            print("Please select input file and output folder")
            return
    
        output_path = os.path.join(output_folder, f"{filename}.pdbqt")
    
        converter = babelConverter.ObabelConverter(input_path, output_path)
        success, result = converter.fastConvert()
    
        if success:
            print(f"✓ Saved to: {result}")
        else:
            print("✗ Conversion failed")

    def show_SMILES(self):
        SMILES = self.InputSMILES.get().strip()
        if not SMILES:
            print("Please enter a SMILES string")
            return
        
        try:
            rd = RDkitStuff.SMILESdraw(SMILES)
            photo = rd.drawFromSMILES()
        
        
            if hasattr(self, 'structure_label'):
                self.structure_label.destroy()
            
        
            self.structure_label = ctk.CTkLabel(self.SMILESVFrame, image=photo, text="")  # Fixed: CTkLabel
            self.structure_label.image = photo  # Keep reference!
            self.structure_label.pack(pady=20)
        
        except Exception as e:
            print(f"Error visualizing SMILES: {e}")
        # Show error label
            error_label = ctk.CTkLabel(self.SMILESFrame, text=f"Error: {e}", text_color="red")
            error_label.pack(pady=20)
        

        

if __name__ == "__main__":
    app = UserInterface()
    app.mainloop()
