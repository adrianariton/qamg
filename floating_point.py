from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import  QuantumRegister, assemble, Aer, AncillaRegister, transpile, IBMQ
from math import pi, sqrt
from qiskit.circuit.library.standard_gates import PhaseGate
from qiskit.circuit.library.basis_change import QFT

from qiskit_ibm_runtime import Estimator, Session
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import Arithmetic.gates as gates
from qiskit.providers.fake_provider import FakeVigo

### Initialize conditions

device_backend = FakeVigo()
aersimulator = AerSimulator()
sim_vigo = AerSimulator.from_backend(device_backend)

service = QiskitRuntimeService()

### floating points numbers representations
"""
    sign_bit
    E - exponent
    M - mantissa

    then x = (-1) ^ sign_bit * 2 ^ exponent * mantissa

    observation: mantissa is ussualy a number in the interval [1,2)

    The following representation will follow the big endiannes principles.

    First bit of the exponent is a sign-bit

"""

const_E_bits_no = 4 # exponent
const_M_bits_no = 7

def zero():
    return [1, 0]

def one():
    return [0, 1]

def number_to_qubit_string(n):
    ans = []
    if n < 0:
        ans.append([0, 1])
        n = -n
        n += 1
    
    else :
        ans.append([1, 0])
    
    while n > 0:
        if n % 2 == 0:
            ans.insert(1, [1, 0])
        else:
            ans.insert(1, [0, 1])
        n //= 2
        #print(n)

    return ans

print(number_to_qubit_string(-7))

class FloatingPoint:
    def __init__(self, E_bits = [], M_bits = []):
        if len(E_bits) == 0:
            E_bits = [[1,0] for i in range(const_E_bits_no)]
        if len(M_bits) == 0:
            M_bits = [[1,0] for i in range(const_M_bits_no)]

        self.E_bits = E_bits
        self.M_bits = M_bits
        self.sign = 0
    def __init__(self, x):
        exp = 0
        sign = -1 if x < 0 else 1

        self.sign = [1, 0] if sign == 1 else [0, 1]

        x = x * sign
        while x >= 2 :
            exp += 1
            x /= 2

        print(x)
        while x < 1:
            exp -= 1
            x *= 2
        
        self.E_bits = number_to_qubit_string(exp)

        while len(self.E_bits) < const_E_bits_no:
            self.E_bits.insert(1, [1, 0])

        x -= 1

        x = int(x * (2 ** const_M_bits_no))

        self.M_bits = number_to_qubit_string(x * sign)

        while len(self.M_bits) < const_M_bits_no:
            self.M_bits.insert(1, [1, 0])

    def print(self):
        print (self.sign)
        print (self.E_bits)
        print (self.M_bits)


x = FloatingPoint(4.875)
print("\nNext lines are for x exp and mantissa:")
x.print()


        
        



### Initialize circuit registers





