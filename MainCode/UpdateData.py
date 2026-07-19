import pickle

from .MainClasses import PATH

class Update:

    def API(self, API):

        mainData_path = PATH("mainData.bin")

        with open(mainData_path ,"wb") as f:
            pickle.dump(API, f)

    def MainCity(self, city):

        mainData_path = PATH("Cities.txt")

        with open(mainData_path ,"r") as f:
            data = f.readlines()

        if data == []:
            data.append(city+'\n')
        else:        
            if f"{city}\n" in data:
                data.pop(data.index(f"{city}\n"))
            data.insert(0,f"{city}\n")

        with open(mainData_path ,"w") as f:
            f.writelines(data)
      