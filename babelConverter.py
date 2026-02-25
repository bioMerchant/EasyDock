import subprocess

class ObabelConverter:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path   
        self.output_path = output_path  
    
    def convert(self):
        cmd = ["obabel", self.input_path, "-O", self.output_path, "-xh"]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Converted {self.input_path} → {self.output_path}")
            return True, self.output_path
        except subprocess.CalledProcessError as e:
            print(f"✗ Error: {e.stderr}")
            return False, None
    
    def fastConvert(self):
        cmd = ["obabel", self.input_path, "-O", self.output_path]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Converted {self.input_path} → {self.output_path}")
            return True, self.output_path
        except subprocess.CalledProcessError as e:
            print(f"✗ Error: {e.stderr}")
            return False, None        



