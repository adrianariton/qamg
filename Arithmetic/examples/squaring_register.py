'''
    This is a simple circuit that performes a squaring operation,
    using the ibm-runtime
    
    For an aer example, see 'aer_simulator_example.py'
    
    The circuit contains 3 registers:
        - a and b: a is the input and b should be initialized to 0
                   each has 'bits' bits
        - n: where the result is stored, n has '2*bits' bits
    
    See more complex gates here:
    https://qiskit.org/documentation/apidoc/circuit_library.html
'''

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister, assemble, transpile, Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import AerError
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from math import pi
from sympy import symbols, preview, Symbol
import Arithmetic.gates as gates
from qiskit.circuit.library import RGQFTMultiplier

from qiskit import QuantumCircuit, execute
from qiskit.circuit.library import RGQFTMultiplier

from qiskit_ibm_runtime import Estimator, Session
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.circuit.random import random_circuit

from qiskit.primitives import Sampler

sampler = Sampler()

regs = gates.RegisterUtils
ds = gates.DefiniteStates
'''
    If you want your own api key, register at:
    https://quantum-computing.ibm.com and run
    QiskitRuntimeService.save_account(channel="ibm_quantum", token="API_TOKEN")
    or use the commented line (once), with my token
'''
# QiskitRuntimeService.save_account(channel="ibm_quantum", token="1df855214acba333a1a1b8475d93d571dce92f0104fee8e25d3616afe112e342ed32f0f4a4517f2e893ce574eb265f007e9dd5b86cbb49a8217912a0eb582de2")


service = QiskitRuntimeService()

'''
    Change it to whatever suits your needs
'''
bits = 5

'''
    Declare Quantum Registers
    and classical register used for measurement
'''
a = QuantumRegister(bits)
b = QuantumRegister(bits)
n = QuantumRegister(2*bits)
cl = ClassicalRegister(2*bits)


'''
    Prebuilt qiskit multiplyer (tred to implement my own but felt 
    like i was reinveting the wheel so no thank you)
    
    [In gates.py you can find working but slow implementations of adder and addermod]
    
    Takes in 2 registers of length bits initialized to whatever
    and a register of length 2*bits initialized to |000....0\ aka 0.
    
    Returns the first 2 register unchanged and the null one goes from 0 to
    a * b.
    
    |a\ |b\ |0\ => |a\ |b\ |a*b\ 
'''
mul = RGQFTMultiplier(num_state_qubits=bits, num_result_qubits=2*bits).to_instruction()
# mul = gates.QFTArithmetic.QFTModularMultiply(in_bits=bits, out_bits=2*bits)


circuit = QuantumCircuit(a,b,n,cl)

'''
    Hadamard gate
    Initializes a to a state qwith equal probability of being any definite state
    ~ Equivalent to 
    ```
        circuit.h(a)
    ```
'''
gates.init_reg(circuit, a, ds.h(bits))

'''
    Entangle a and b: equivalent of duplication for definite states |0\ and |1\ 
    to perform a squaring operation
'''
for i in range(bits):
    circuit.cnot(a[i], b[i])

'''
    Multiply registers a and b and output to register n
'''
circuit.append(mul, regs.join(a,b,n))

'''
    Undo 'duplicating'
'''
for i in range(bits):
    circuit.cnot(a[i], b[i])
    

'''
    Measure the n-register
'''
circuit.barrier()
for i in range(2*bits):
    circuit.measure(n[i], cl[i])



'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='pics/rand.qibm.png')
print(f">>> Quasi-distribution: {result.quasi_dists[0]}")