from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import  QuantumRegister, assemble, Aer, AncillaRegister, transpile, IBMQ
from math import pi, sqrt
from qiskit.circuit.library.standard_gates import PhaseGate
from qiskit.circuit.library.basis_change import QFT
# from qiskit.circuit.library import CSwapGate as Fredkin
from qiskit.circuit.gate import Gate

from qiskit_ibm_runtime import Estimator, Session
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.providers.fake_provider import FakeVigo

import numpy as np
import Arithmetic.gates as gates

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

def number_to_qubit_string(n, bits_no, signed):
    ans = []

    if signed == True:
        if n < 0:
            ans.append([0, 1])
            n = 2**(bits_no - 1) + n
        
        else :
            ans.append([1, 0])
    print(n)
    print(ans)
    while n > 0:
        if n % 2 == 0:
            ans.insert(0 if signed == False else 1, [1, 0])
        else:
            ans.insert(0 if signed == False else 1, [0, 1])
        n //= 2
        print(ans)

    return ans

# print(number_to_qubit_string(-7))

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

        while x < 1:
            exp -= 1
            x *= 2
        
        # print(x)
        # print(exp)
        
        self.E_bits = number_to_qubit_string(exp, const_E_bits_no, True)

        while len(self.E_bits) < const_E_bits_no:
            self.E_bits.insert(1, [1, 0])

        x -= 1

        x = int(x * (2 ** const_M_bits_no))
        # print(x)
        self.M_bits = number_to_qubit_string(x, const_M_bits_no, False)

        while len(self.M_bits) < const_M_bits_no:
            self.M_bits.insert(1, [1, 0])

    def printall(self):
        print("sign ", end = "")
        print (self.sign)

        print("exponent ", end = "")
        print (self.E_bits)

        print("mantissa ", end = "")
        print (self.M_bits)



# get upper bound of log in base 2

def log_2(n):
    a = 0
    while (2 ** a < n):
        a+=1
    return a


# this gate will perform the transformation |1> |x> -> |n> |2^(2^order) * x> 
# n is going to be represented on shift_bits, where shift_bits = log(x_bits)

def fp_order_shift(x_bits, order):
    a = QuantumRegister(1)
    b = QuantumRegister(2 * x_bits)
    circ = QuantumCircuit(a, b, name=f"{order}_order_shift")

    for j in range (2 * x_bits - 2 ** order):
        circ.cswap(a[0], b[j], b[j + 2 **order])
    
    # circ.draw("mpl", filename = f"pics/{order}_order_shift")

    return circ.to_instruction()

# this gate will perform the transformation |n> |x> -> |n>|2^n * x> 
# n is going to be represented on shift_bits, where shift_bits = log(x_bits)

def fp_qubit_shifting(x_bits, shift_bits):
    a = QuantumRegister(shift_bits) # shift_bits
    b = QuantumRegister(2 * x_bits)
    circ = QuantumCircuit(a,b, name="FP_SHIFT")

    for i in range(shift_bits):
        circ.append(fp_order_shift(x_bits, i), [a[i]] + [*b])
            


    # circ.draw("mpl", filename = "pics/qubit_shifting.png")

    return circ.to_instruction()


# the following functions returns the output 1 if two numbers are equal
# the numbers a and b are represented on x_bits number of bits

# the rule this function will follow is |a > |b > |0...0> |0> -> | new_exec > | a > | b > |anc> |out>

# we will consider the following
# by comparing bit to bit of the two numbers, we make the following observations:
"""
    if a[i] and b[i] are equal, then cnot(|a[i]> ,|b[i]>) ->  |a[i]> ,|0>, else
    cnot(|a[i]>, |b[i]>) -> |a[i]> |1>
"""

# |a> |b> |0> -> |a> |a xor b> |(a == b)>
def circuit_equal(x_bits):
    a = QuantumRegister(x_bits)
    b = QuantumRegister(x_bits)
    out = QuantumRegister(1)

    circ = QuantumCircuit(a, b, out, name= "IS_EQUAL_HALF")

    for i in range(x_bits):
        circ.cx(a[i], b[i])
        circ.x(b[i])
    circ.mcx([*b], out)

    circ.draw("mpl", filename="pics/equal_first_gate.png")

    return circ.to_instruction()

# by reversing it and adding a new qubit to save the state
# we will obtain the following transformation:
# |a> |b> |0> |0 -> |a> |b> |0> |out>

# Observation: we used for this operation just two  aditional qubits

def equal_numbers(x_bits):
    a = QuantumRegister(x_bits)
    b = QuantumRegister(x_bits)
    out1 = QuantumRegister(1)
    out2 = QuantumRegister(1)

    circ = QuantumCircuit(a, b, out1, out2, name = "IS_EQUAL")
    aux_gate = circuit_equal(x_bits)

    circ.append(aux_gate, [*a] + [*b] + [*out1])

    circ.cx(out1, out2)

    circ.append(aux_gate.reverse_ops(), [*a] + [*b] + [*out1])

    circ.draw("mpl", filename = "pics/equal_final.png")
    return circ.to_instruction()


# function to get the negative of a x_bits number
# |x> -> |-x>
def get_negative(x_bits):
    a = QuantumRegister(x_bits)
    b = QuantumRegister(1)
    circ = QuantumCircuit(a, b, name = "NEGATIVE")
    for i in range(x_bits):
        circ.x(a[i])

    
    

class FPArithmetic:
    def __init__(self) -> None:
        pass
### Initialize circuit registers


# fp_qubit_shifting(8, 3)

# fp_order_shift(8, 1)

def initialize_states(circ, register, states):
    for i in range(len(states)):
        circ.initialize(states[i], register[i])

def initialize_fp(circ, exponent_register, mantissa_register, fp):
    initialize_states(circ, exponent_register, fp.E_bits)
    initialize_states(circ, mantissa_register, fp.M_bits)


# the following function represents an experiment to verify if two numbers are equal
def verify_two_numbers_equality_experiment(a, b):
    fp1 = FloatingPoint(a)
    fp2 = FloatingPoint(b)

    exp1 = QuantumRegister(len(fp1.E_bits))
    exp2 = QuantumRegister(len(fp1.E_bits))

    man1 = QuantumRegister(len(fp1.M_bits))
    man2 = QuantumRegister(len(fp2.M_bits))

    aux = QuantumRegister(1)
    out = QuantumRegister(1)

    cl = ClassicalRegister(1)

    fp1.printall()

    circ = QuantumCircuit(exp1, exp2, man1, man2, aux, out, cl)

    initialize_fp(circ, exp1, man1, fp1)
    initialize_fp(circ, exp2, man2, fp2)

    circ.append(equal_numbers(const_E_bits_no), [*exp1] + [*exp2] + [*aux] + [*out])

    # circ.measure_all()

    circ.measure(out[0], cl[0])
    circ.draw("mpl", filename = "pics/fp_circuit.png")


    ### Initialize conditions

    device_backend = FakeVigo()
    sim_ideal = AerSimulator()
    sim_vigo = AerSimulator.from_backend(device_backend)

    result = sim_ideal.run(transpile(circ, sim_ideal)).result()
    counts = result.get_counts(0)
    plot_histogram(counts, title='Output value', filename='pics/histogram_equal.png')


