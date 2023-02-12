'''
    Aer runs pretty slow for me so i'll use IBMProvider for now
'''

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, QuantumRegister, assemble, Aer, AncillaRegister
from math import pi, sqrt
import gates
from qiskit import transpile
from qiskit.circuit.library import RGQFTMultiplier, PhaseGate, PolynomialPauliRotations, WeightedAdder, PiecewiseChebyshev
from gates import RegisterUtils as regs
from gates import DefiniteStates as ds
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import numpy as np
from qiskit.circuit.library import QFT

aer_sim = Aer.get_backend('aer_simulator', method='matrix_product_state')

'''
--------------------------Cebishev approx: didnt really understand it--------------------------
    
    It is supposed to give a remez polynomial aproximattion. Can't really see it
    See more complex gates here:
    https://qiskit.org/documentation/apidoc/circuit_library.html
    
    Commented code for cebishev approx here:

        f_x, degree, breakpoints, num_state_qubits = lambda x: 1/np.sqrt(x), 2, [1, 5], 2
        pw_approximation = PiecewiseChebyshev(f_x, degree, breakpoints, num_state_qubits)
        pw_approximation._build()
        print(pw_approximation.polynomials)
        circ = QuantumCircuit(pw_approximation.num_qubits)
        circ.h(list(range(num_state_qubits)))

        circ.append(pw_approximation.to_instruction(), circ.qubits)
'''

a = QuantumRegister(2)
z = QuantumRegister(1)

circ = QuantumCircuit(a,z)

'''
    Initialize register a to 3
'''
gates.init_reg(circ, a, ds.binary(3, bits=2))

'''
--------------------------Pauli Polynomial Rotation--------------------------

    Calculates sin(p(a)) and cos(p(a)), which are encoded in the probabilities
    and therefore not measurable in one shot :(.
        
    |a\ |0\ => cos(p(a)) |a\ |0\ + sin(p(a)) |a\ |0\ 

'''
circ.append(PolynomialPauliRotations(2, [0.1, 0.1], basis='Y'), regs.join(a,z))

'''
    Optional decomposition
'''
circ = circ.decompose(reps=4, gates_to_decompose=gates.all())
print("DECOMPOSED")

'''
    Save state vector without measuring.
    For measuring see squaring_register.py
'''
circ.save_statevector()

circ.draw('mpl', filename='pics/circ.aer_sim_exp.png')
print("DREW")

'''
    Run simulation and print results
'''
qasm = transpile(circ, aer_sim)
res = aer_sim.run(qasm).result()
counts = res.get_counts()
state = res.get_statevector()


print("State:")
print(state)

print("Counts")
print(counts)
plot_histogram(counts, filename='pics/hist.aer_sim_exp.png')