import subprocess

subprocess.run(["clear"], shell=True, check=True)
print("Called!!!")

def clear():
    subprocess.run(["clear"], shell=True, check=True)
