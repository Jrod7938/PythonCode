import os

# Generate Negative Description File
def gndf():
    with open('neg.txt', "w") as f:
        for filename in os.listdir("negative"):
            f.write("negative/" + filename + "\n")