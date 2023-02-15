import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister, assemble, transpile, Aer
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import AerError
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from math import pi
from sympy import symbols, preview, Symbol
import gates
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
bits = 4

'''
    Declare Quantum Registers
    and classical register used for measurement
'''
a = QuantumRegister(bits)
b = QuantumRegister(bits+1)
c = QuantumRegister(bits)
n = QuantumRegister(2*bits+1)
cl = ClassicalRegister(bits+1)


add = gates.addermod(bits)

circuit = QuantumCircuit(a,b,c,n,cl)

'''
    Initialize a and b to 3 and 5
    and n to 6
    
    It will calculate (3+5)%6 = 2
'''
gates.init_reg(circuit, a, ds.binary(3, bits))
gates.init_reg(circuit, b, ds.binary(5, bits+1))


gates.init_reg(circuit, n, ds.binary(6, bits) + [[1, 0]] * (bits+1) )


'''
    Multiply registers a and b and output to register n
'''
circuit.append(add, regs.join(a,b,c,n))



'''
    Measure the n-register
'''
circuit.barrier()
for i in range(bits+1):
    circuit.measure(b[i], cl[i])



'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='pics/modadd.qg.png')
print(f">>> Quasi-distribution: {result.quasi_dists[0]}")