'''
    Aer simulator, with ideal and noisy conditions
    this will soon become a means to study syrface codes
    
'''
from qiskit import IBMQ, transpile
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.tools.visualization import plot_histogram
from qiskit.providers.fake_provider import FakeVigo
device_backend = FakeVigo()

# Construct quantum circuit
circ = QuantumCircuit(3, 3)
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure([0, 1, 2], [0, 1, 2])

sim_ideal = AerSimulator()
sim_vigo = AerSimulator.from_backend(device_backend)


# Execute and get counts, in an ideal environment
result = sim_ideal.run(transpile(circ, sim_ideal)).result()
counts = result.get_counts(0)
plot_histogram(counts, title='Ideal counts for 3-qubit GHZ state', filename='histograms_QEC/QEC_hist.png')


# Transpile the circuit for the noisy basis gates [real environment]
tcirc = transpile(circ, sim_vigo)

# Execute noisy simulation and get counts
result_noise = sim_vigo.run(tcirc).result()
counts_noise = result_noise.get_counts(0)
plot_histogram(counts_noise,
               title="Counts for 3-qubit GHZ state with device noise model", filename='histograms_QEC/noisyQEC_hist.png')