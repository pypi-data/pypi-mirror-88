
import numpy as np

class Message:

    def __init__(self, *args):

        if len(args) == 0:
            self._data = np.array([])

        elif len(args) == 1:
            if type(args[0]) == list:
                self._data = args[0]
            else:
                print("Invalid type of input..")
                raise TypeError

        else:
            print("Invaid number of inputs..")
            raise TypeError
    
    def __repr__(self):
        if type(self._data) == type(np.array([])):
            return self._data.tolist().__repr__()
        else:
            return self._data.__repr__()

    def __str__(self):
        if type(self._data) == type(np.array([])):
            return self._data.tolist().__str__()
        else:
            return self._data.__str__()

    def __len__(self):
        return len(self._data)
