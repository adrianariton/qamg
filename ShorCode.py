'''
    Shor correction code [different from Shor algorithm]
    
    Repetition code that corrects for any random
    single-cubit transformation such as parralel
    X, Z, Y and I on one qubit
        
    See more here: https://en.wikipedia.org/wiki/Quantum_error_correction
    Block codes: https://en.wikipedia.org/wiki/Block_code
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


psi = QuantumRegister(1)
anc = QuantumRegister(8)
cl = ClassicalRegister(1)


circuit = QuantumCircuit(psi, anc, cl)

gates.init_reg(circuit, psi, [[3.0/5, 4.0/5]])


circuit.cnot(psi[0], anc[2])
circuit.cnot(psi[0], anc[5])

circuit.h(psi[0])
circuit.h([anc[2], anc[5]])

circuit.cnot(psi[0], anc[0])
circuit.cnot(anc[2], anc[3])
circuit.cnot(anc[5], anc[6])

circuit.cnot(psi[0], anc[1])
circuit.cnot(anc[2], anc[4])
circuit.cnot(anc[5], anc[7])

# <E> [Environment operator]
circuit.barrier()

circuit.z(anc[6])
circuit.y(anc[6])
circuit.z(anc[6])



circuit.barrier()
# </E> [Environment operator]

circuit.cnot(psi[0], anc[0])
circuit.cnot(anc[2], anc[3])
circuit.cnot(anc[5], anc[6])

circuit.cnot(psi[0], anc[1])
circuit.cnot(anc[2], anc[4])
circuit.cnot(anc[5], anc[7])

circuit.ccx(anc[1], anc[0], psi[0])
circuit.ccx(anc[4], anc[3], anc[2])
circuit.ccx(anc[7], anc[6], anc[5])

circuit.h(psi[0])
circuit.h([anc[2], anc[5]])

circuit.cnot(psi[0], anc[2])
circuit.cnot(psi[0], anc[5])

circuit.ccx(anc[5], anc[2], psi[0])

circuit.barrier()


circuit.measure(psi[0], cl[0])




'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='shorcode.png')
print(f">>> Quasi-distribution: {result.quasi_dists[0]}")
