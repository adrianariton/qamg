import ErrorCorrection

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

from qiskit_ibm_provider import IBMProvider

# Save account credentials.
# IBMProvider.save_account(token=MY_API_TOKEN)

# Load previously saved account credentials.

aer_sim = Aer.get_backend('aer_simulator', method='matrix_product_state')


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
backend = service.backend("ibmq_qasm_simulator")

sampler = Sampler()

'''
    Change it to whatever suits your needs
'''

w = QuantumRegister(1)
cl = ClassicalRegister(1)
circuit = QuantumCircuit(w,cl)
# logical_bit = ErrorCorrection.LaticealSurfaceCodes.FullSurface(begin_with='X')
circuit.x(w)
circuit.z(w)
circuit.measure(w[0], cl[0])

'''
    Measure the n-register
'''
circuit.barrier()

circuit.save_statevector()


circuit = circuit.decompose(gates_to_decompose=gates.all(), reps=5)
#circuit.draw("mpl", filename='pics/qqqq.qg.png')
circuit = transpile(circuit, aer_sim)
print(f'Circuit: {circuit.depth()}')
'''
    Run sampler and output results
'''
job = aer_sim.run(circuit)
result = job.result()

print(f">>> Quasi-distribution: {result.get_counts()}")
dt = result.get_statevector()
dt.draw(output='hinton', filename='pics/hinton.png')
'''
xx = list([*result.quasi_dists[0]])
plt.title('Ancilla measurements')
plt.plot(xx,  dict(result.quasi_dists[0]).values(), 'r.')
plt.show()
'''

