
'''
    Coes: https://en.wikipedia.org/wiki/Quantum_error_correction
    Code is from here:
        https://qiskit.org/textbook/ch-quantum-hardware/error-correction-repetition-code.html
    Soon, I will clean and improve it
'''
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
aer_sim = Aer.get_backend('aer_simulator')

def get_noise(p_meas,p_gate):
    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_gate1 = depolarizing_error(p_gate, 1)
    error_gate2 = error_gate1.tensor(error_gate1)

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_meas, "measure") # measurement error is applied to measurements
    noise_model.add_all_qubit_quantum_error(error_gate1, ["x"]) # single qubit gate error is applied to x gates
    noise_model.add_all_qubit_quantum_error(error_gate2, ["cx", "swap"]) # two qubit gate error is applied to cx gates
        
    return noise_model

noise_model = get_noise(0.01,0.01)

qc0 = QuantumCircuit(3) # initialize circuit with three qubits in the 0 state
qc0.swap(0,1)
qc0.swap(0,1)
qc0.swap(0,1)
qc0.swap(0,1)
qc0.swap(0,1)
qc0.swap(0,1)
qc0.swap(0,1)


qc0.measure_all() # measure the qubits

# run the circuit with the noise model and extract the counts
qobj = assemble(qc0)
counts = aer_sim.run(qobj, noise_model=noise_model).result().get_counts()

plot_histogram(counts, filename='histograms_QEC/noisyQEC2_hist.png')