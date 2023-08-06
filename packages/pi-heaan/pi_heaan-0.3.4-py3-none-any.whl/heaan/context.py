
class Context:

    def __init__(self, *args):
        self._is_bootstrappable = False
        self._used_function = dict()
        self._time = 0

        if len(args) == 0:
            pass

        elif len(args) == 1:
            self._params = args[0]
            self._is_large = False

        elif len(args) == 2:
            self._params = args[0]
            self._is_large = args[1]
        
        else:
            print("Invaid number of inputs..")
            raise TypeError

    # estimated per mult at one core
    def __repr__(self):
        _function_time = {
            'add'       : 0.005,
            'sub'       : 0.010,
            'add_const' : 0.006,
            'sub_const' : 0.007,
            'negate'    : 0.006,
            'div_pow2'  : 0.008,
            'decrypt'   : 0.032,
            'encrypt'   : 0.191,
            'mult_msg'  : 0.211,
            'mult_const_int'    : 0.174,
            'mult_const_float'  : 0.186,
            'kill_imag' : 0.445,
            'rotate'    : 0.436,
            'mult'      : 1,
            'make_bootstrappable' : 8.904,
            'bootstrap' : 88.754,
        }

        output  = "\n"
        output += "=========== Operation Usage (in single thread) ===========\n"
        output += "==========================================================\n"
        output += "OP_TYPE\t\tTIME_UNIT\tNUM_USAGE\tTIME_USAGE\n"
        output += "----------------------------------------------------------\n"

        total_time = 0
        for op_type in self._used_function:
            op_time_unit = _function_time[op_type]
            op_num_usage = self._used_function[op_type]
            op_time_usage = op_time_unit * op_num_usage
            output += "{}\t\t{}\t\t{}\t\t{}\n".format(op_type, op_time_unit, op_num_usage, op_time_usage)
            total_time += op_time_usage

        output += "----------------------------------------------------------\n"
        output += "\t\t*** Total estimated time unit : {}\n".format(total_time)

        return output

    def _update_used_function(self, function):
        if function in self._used_function:
            self._used_function[function] += 1
        else:
            self._used_function[function] = 1
        pass

    def get_degree(self):
        return self._params.get_degree()
    
    def get_quantize_bits(self):
        return self._params._get_quantize_bits()
    
    def get_sp_num(self):
        return self._params.get_sp_num()
    
    def get_sp_modulus_bits(self):
        return self._params.get_sp_modulus_bits()
    
    def get_log_degree(self):
        return self._params.get_log_degree()

    def get_modulus_bits(self):
        return self._params.get_modulus_bits()
    
    def make_bootstrappable(self, log_slots):
        self._is_bootstrappable = True
        self._update_used_function("make_bootstrappable")
        pass

    def save_params(self, path):
        self._params.save(path)
    
    def load_params(self, path):
        self._params.load(path)