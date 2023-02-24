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
import Arithmetic.gates as gates
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
bits = 3

'''
    Declare Quantum Registers
    and classical register used for measurement
'''
ctrl = QuantumRegister(1)
z = QuantumRegister(bits)
a = QuantumRegister(bits)
b = QuantumRegister(bits+1)
anc = AncillaRegister(2 * bits + 1)
cl = ClassicalRegister(bits+1)
circuit = QuantumCircuit(ctrl,z,a,b,anc,cl)

gates.init_reg(circuit, z, ds.binary(4, bits))

circuit.x(ctrl)

scmm = gates.ModularParametrizedGates(modular=True, N=7).SimpleControlledModularMultiplicator(bits, 5)

circuit.append(scmm, regs.join(ctrl,z,a,b,anc))


'''
    Measure the n-register
'''
circuit.barrier()
for i in range(bits+1):
    circuit.measure(b[i], cl[i])


circuit = circuit.decompose(gates_to_decompose=gates.all(), reps=5)

print(f'Circuit: {circuit.depth()}')
'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='pics/gtest.qg.png')
print(f">>> Quasi-distribution: {result.quasi_dists[0]}")

