'''
    Quantum Encoder with a function
    
    Works exactly as the classical one, only if permutes the
    inputs so thet the result of the selecton is placed on position 0
    
'''

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
import matplotlib.pyplot as plt
from math import pi, sqrt
import gates

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
    bits: inrease for precision
'''
bits = 6
'''
    psi_bits: number of bits for wave representation
'''
psi_bits = 4

'''
    Declare Quantum Registers
    and classical register used for measurement
'''
a = QuantumRegister(bits)
psi = QuantumRegister(psi_bits)

cl = ClassicalRegister(bits)

circuit = QuantumCircuit(a,psi,cl)

'''
    Initialize psi[2] to 1:
        psi : |0010...0\ 
'''
gates.init_reg(circuit, psi, ds.binary(2 ** 2, psi_bits))

'''
    If more bits are initialized to 1, the output is:
        out = 1 / (sum(fct(i)) foreach i with psi[i] == |1\ )
'''

'''
    The function should be positive, and greater then 0,
    and also continous
'''
def fct(i):
    return 2 ** (i + 2)

encod = gates.Selectors.ENCODER(psi_bits=psi_bits, precision_bits=bits, func=fct)
circuit.append(encod, regs.join(a, psi))

circuit.barrier()
for i in range(bits):
    circuit.measure(a[i], cl[i])


circuit = circuit.decompose(reps=1)
'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='pics/rth.qg.png')
print(f">>> Quasi-distribution: {result.quasi_dists[0]}")

exval = 0
for key, val in result.quasi_dists[0].items():
    exval += key * val
print()
print(f'>>> Expectation value: {exval}')
print(f'    Fct value: fct(i) = {2 ** bits / exval}')
print(f'    [i as in the i"th bit is 1 and the rest are 0]')

'''
For plotting:
    D = result.quasi_dists[0]

    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), list(D.keys()))
    # # for python 2.x:
    # plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
    # plt.xticks(range(len(D)), D.keys())  # in python 2.x

    plt.show()
'''