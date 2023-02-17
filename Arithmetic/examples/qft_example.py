import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, assemble, Aer, transpile
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit_aer import AerError
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from math import pi
from sympy import symbols, preview, Symbol
import Arithmetic.gates as gates
ds = gates.DefiniteStates
regs = gates.RegisterUtils
sqrt = np.sqrt

sim = Aer.get_backend('aer_simulator', method='extended_stabilizer')

'''
    Number of bits in QFT: variable
'''
bits = 12

a = QuantumRegister(bits, 'a')

circ = QuantumCircuit(a)

'''
    Initialize a to superposition of all possible states
'''
gates.init_reg(circ, a, ds.h(bits))

'''
    See gates.py for rough implementation of Quantum Fourier Transform
    and aer_simulator_example.py and squaring_register.py for info on 
    how register and all such work
'''
circ.append(gates.QuantumPeriodGates.qft(bits), [*a])

'''
    Optional decomposition
'''
circ = circ.decompose(reps=3, gates_to_decompose=gates.all())
print("DECOMPOSED")


'''
    Save resulting state without measuring
'''
circ.save_statevector()
print("STATE")



circ.draw('mpl', filename='qfttest.q.png')
print("DREW")

'''
    If slow, lower the 'bits' variable
'''
qasm = assemble(circ)
res = sim.run(qasm).result()
counts = res.get_counts()
state = res.get_statevector()


print("State:")
print(state)
plot_bloch_multivector(state, filename='bloch_qft.q.png')

print("Counts")
print(counts)
plot_histogram(counts, filename='hist.q.png')
