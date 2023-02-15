'''
    --- WORK IN PROGRESS ---
    [Does not work yet]
    
    See more complex gates here:
    https://qiskit.org/documentation/apidoc/circuit_library.html
'''

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
import matplotlib.pyplot as plt
from math import pi
import gates

from qiskit_ibm_runtime import Estimator, Session
from qiskit_ibm_runtime import QiskitRuntimeService

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
b = QuantumRegister(bits)
n = QuantumRegister(bits)
out = QuantumRegister(2*bits)
t = QuantumRegister(bits+1)

cl = ClassicalRegister(1)


'''
    Takes in 3 registers of length bits initialized to whatever
    and a register of length 2*bits+1 initialized to |000....0\ aka 0. (out + t)
    
    Returns the first 3 register unchanged and the null one goes from 0 to
    a * b mod n.
    
    |a\ |b\ |n\ |00...00\ |0\  => |a\ |b\ |n\ |a*b mod n\ |t\ 
'''
mul = gates.QFTArithmetic.QFTModularMultiply(in_bits=bits, out_bits=2*bits)
'''
    QFT ModularMultiply gate is still in progress and will be implemented 
    with 3 QFTRemainderTheorem gates and one Phase Multiplication
'''

circuit = QuantumCircuit(a,b,n, out, t,cl)

gates.init_reg(circuit, a, ds.binary(2, bits=bits))
gates.init_reg(circuit, b, ds.binary(3, bits=bits))
gates.init_reg(circuit, n, ds.binary(5, bits=bits))

'''
    Multiply registers a and b modulo n and output to register out
'''
circuit.append(mul, regs.join(a, b, n, out, t))
    

'''
    Measure the out-register
'''
circuit.barrier()
for i in range(1):
    circuit.measure(t[bits + i], cl[i])



'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='pics/modmul.qg.png')
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