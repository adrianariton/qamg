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
    Useful paper https://arxiv.org/pdf/1208.0928.pdf
    [Can also be found in README.md]
    
    For distance=3 4x4 Single Zcut Cubit QEC,
    the following configuration works:
    
        b2 = 13
        b1 = 12
        [...]
        QEC_circ = ErrorCorrection.LaticealSurfaceCodes.SingleZcut(width=4, height=4, distance=1)

    The one below is for a 4x2 distance=1 Single Zcut Cubit
'''
b2 = 8
b1 = 7
w = QuantumRegister(b2)
anc = AncillaRegister(b1)
cl = ClassicalRegister(b1)
circuit = QuantumCircuit(w,anc,cl)

QEC_circ = ErrorCorrection.LaticealSurfaceCodes.SingleZcut(width=4, height=2, distance=1)
#QEC_circ = ErrorCorrection.LaticealSurfaceCodes.FullSurface(begin_with='X', width=bits, height=bits)

stabz = ErrorCorrection.LaticealSurfaceCodes.StabilizerZ()

def measure_circ():
    circuit.append(stabz, [w[3],w[1],w[4], w[6], anc[3]])
    circuit.measure(anc[3], cl[3])

def logical_xgate():
    circuit.x(w[1])

def logical_zgate():
    circuit.z(w[1])
    circuit.z(w[3])
    circuit.z(w[4])
    circuit.z(w[6])
    
def noise():
    circuit.x(w[2])

'''
     Append QEC [Error correction]
     then logical X gate
     and then the correction again
'''
circuit.append(QEC_circ.to_instruction(), regs.join(w, anc) , cl)
circuit.barrier()
logical_xgate()
circuit.append(QEC_circ.to_instruction(), regs.join(w, anc) , cl)

'''
+- noise function which is small because we only have
distance=1 (Aer needs a lot more time for distance=3 and 4)


'''
noise()

circuit.append(QEC_circ.to_instruction(), regs.join(w, anc) , cl)
circuit.barrier()
logical_zgate()
circuit.append(QEC_circ.to_instruction(), regs.join(w, anc) , cl)


circuit.barrier()
measure_circ()


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
print(result.get_statevector())

dt = result.get_statevector()
print(dt.draw(output='latex_source'))

#circle1 = plt.Circle((0, 0), 1, color='b', fill=False)
#plt.gca().add_patch(circle1)

#plt.plot([0,result.get_counts()['0000000']/1024.0], [0,result.get_counts()['0001000']/1024.0], '.-')

#plt.show()
'''
data = result.get_counts()

courses = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (10, 5))

# creating the bar plot
plt.bar(courses, values, color ='maroon',
        width = 0.4)

plt.title('Ancilla')
plt.show()
'''

