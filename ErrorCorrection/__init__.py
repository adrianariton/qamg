from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, QuantumRegister, assemble, Aer, AncillaRegister
from math import pi, sqrt
from qiskit.circuit.library.standard_gates import PhaseGate
from qiskit.circuit.library.basis_change import QFT
import matplotlib.pyplot as plt
class LaticealSurfaceCodes:
    def StabilizerZ(dirs=4):
        bits = QuantumRegister(dirs)
        anc = QuantumRegister(1)
        circ = QuantumCircuit(bits, anc, name='StabZ')
        circ.id(anc)
        for i in range(dirs):
            circ.cnot(bits[i], anc[0])
        circ.id(anc)
        
        return circ
    
    def StabilizerX(dirs=4):
        bits = QuantumRegister(dirs)
        anc = QuantumRegister(1)
        circ = QuantumCircuit(bits, anc, name='StabX')
        circ.h(anc)
        for i in range(dirs):
            circ.cnot(anc[0], bits[i])
        circ.h(anc)
        
        return circ
    
    def FullSurface(width=4, height=4, cut=False, cut_line=3, begin_with='Z'):
        total = (width+1)*(height+1)
        anc_nr = total//2 
        bits_nr = total//2
        if anc_nr*2 < total:
            bits_nr = bits_nr + 1
        bits = QuantumRegister(bits_nr, name='*')
        anc = QuantumRegister(anc_nr, name='o')
        cl = ClassicalRegister(anc_nr, name='cl')
        print(bits_nr, anc_nr)
        circuit = QuantumCircuit(bits, anc, cl, name='LSCF')
        arx = []
        ary = []
        arc = []
        for i in range(0, height+1):
            for j in range(0, width+1):
                # if ancilla bit is center
                if (i+j)%2 == 1:
                    anc_position = i * width + i + j
                    pos1 = anc_position - 1
                    pos3 = anc_position + 1
                    pos2 = anc_position - width - 1
                    pos4 = anc_position + width + 1
                    if i == 0:
                        pos2 = -1
                    if i == height:
                        pos4 = -1
                    if j == 0:
                        pos1 = -1
                    if j == width:
                        pos3 = -1
                    pos = [pos1, pos2, pos3, pos4]
                    pos = list(filter(lambda val: val != -1, pos))
                    
                    pos = [(e+1)//2 for e in pos]
                    
                    anc_position = (anc_position)//2
                    
                    arr = []
                    
                    for el in pos:
                        arr = arr + [bits[el]]
                    sw = 1
                    if cut and i == cut_line and j == width//2:
                        sw = 0
                    k = 0
                    if begin_with == 'X':
                        k = 1 - k
                    if sw == 1:
                        if i % 2 == k:
                            circuit.append(LaticealSurfaceCodes.StabilizerZ(dirs=len(pos)), arr + [anc[anc_position]])
                            if sw == 1:
                                arc = arc + ['g']
                        if i % 2 == 1 - k:
                            circuit.append(LaticealSurfaceCodes.StabilizerX(dirs=len(pos)), arr + [anc[anc_position]])
                            if sw == 1:
                                arc = arc + ['y']
                    if sw == 1:
                        arx = arx + [j]
                        ary = ary + [i]
                    if sw == 0:
                        print(f'De-activated anc: {anc_position} \n\tbits:{pos}')
                    if sw == 1:
                        circuit.measure(anc[anc_position], cl[anc_position])
        plt.scatter(arx, ary, c=arc, s=[300] * len(arx))
        plt.show()
        return circuit
    
    def SingleZcut(width=4, height=4, distance=2):
        return LaticealSurfaceCodes.FullSurface(width, height, cut=True, cut_line=2*distance-1, begin_with='X')
    
    def SingleXcut(width=4, height=4, distance=2):
        return LaticealSurfaceCodes.FullSurface(width, height, cut=True, cut_line=2*distance-1, begin_with='Z')