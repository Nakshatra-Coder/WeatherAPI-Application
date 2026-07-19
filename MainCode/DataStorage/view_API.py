import pickle

with open("mainData.bin","rb+") as f:
        print(pickle.load(f))

input()
