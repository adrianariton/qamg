'''
    Quantum Multiplexor: MUX
    
    Works exactly as the classical one, only if permutes the
    inputs so thet the result of the selecton is placed on position 0
    
'''

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
import matplotlib.pyplot as plt
from math import pi, sqrt
import Arithmetic.gates as gates
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
bits = 3

'''
    Declare Quantum Registers
    and classical register used for measurement
'''
a = QuantumRegister(bits)
n = QuantumRegister(2 ** bits)
anc = QuantumRegister(6)

cl = ClassicalRegister(1)


circuit = QuantumCircuit(a,n,cl)
'''
    a (selection) is 5 (101), so it selects the 5th input state:
        5/13 * |0\ + 12/13 * |1\ 
'''
gates.init_reg(circuit, a, ds.binary(5, bits=bits))

'''
    Initialize four different states for
    testing pusposes 
'''
gates.init_reg(circuit, n, [[3.0/5, 4.0/5], [1, 0], [0, 1], [1/sqrt(2), 1/sqrt(2)], [4.0/5, 3.0/5], [5.0/13, 12.0/13], [0, 1], [1/sqrt(2), 1/sqrt(2)]])

mux = gates.Selectors.MUX(bits)
circuit.append(mux, regs.join(a,n))

circuit.barrier()
circuit.measure(n[0], cl[0])



'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='pics/rth.qg.png')
print(f">>> Quasi-distribution: {result.quasi_dists[0]}")

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