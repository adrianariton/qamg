import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
import matplotlib.pyplot as plt
from math import pi, sqrt
import Arithmetic.gates as gates
from qiskit_ibm_runtime import Estimator, Session
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.circuit.random import random_circuit

from qiskit.primitives import Sampler

# Check if gate is gate :)
print(gates.QFTArithmetic.QFTRemainderTheorem(in_bits=3))
print('---------------------------')
print('Import succeded! Have fun!!')