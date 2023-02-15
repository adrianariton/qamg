from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, QuantumRegister, assemble, Aer, AncillaRegister
from math import pi, sqrt
from qiskit.circuit.library.standard_gates import PhaseGate
from qiskit.circuit.library.basis_change import QFT

carry_circ = QuantumCircuit(4, name='CARRY')
carry_circ.ccx(1, 2, 3)
carry_circ.cnot(1, 2)
carry_circ.ccx(0, 2, 3)
carry = carry_circ.to_instruction()

sum_circ = QuantumCircuit(3, name='SUM')
sum_circ.cnot(1, 2)
sum_circ.cnot(0, 2)
sum = sum_circ.to_instruction()

dcarry_circ = QuantumCircuit(4, name='CARRY_dg')
dcarry_circ.ccx(0, 2, 3)
dcarry_circ.cnot(1, 2)
dcarry_circ.ccx(1, 2, 3)
dcarry = dcarry_circ.to_instruction()

dsum_circ = QuantumCircuit(3, name='SUM_dg')
dsum_circ.cnot(0, 2)
dsum_circ.cnot(1, 2)
dsum = dsum_circ.to_instruction()

def adder(bits):
    qa = QuantumRegister(bits)
    qb = QuantumRegister(bits+1)
    qc = QuantumRegister(bits)
    add_circ = QuantumCircuit(qa, qb, qc, name='ADD')
    n = bits - 1
    for i in range(n + 1):
        if i is not n:
            add_circ.append(carry, [qc[i], qa[i], qb[i], qc[i+1]])
        else:
            add_circ.append(carry, [qc[i], qa[i], qb[i], qb[i+1]])
    add_circ.cnot(qa[n], qb[n])
    
    for j in range(n + 1):
        i = n - j
        if i < n:
            add_circ.append(dcarry, [qc[i], qa[i], qb[i], qc[i+1]])
        add_circ.append(sum, [qc[i], qa[i], qb[i]])
    return add_circ.to_instruction()

def dadder(bits):
    return adder(bits=bits).inverse()

def init_reg(circ, register, states):
    lg = len([*register])
    print(f'lr {lg}')
    for i in range(lg):
        circ.initialize(states[i], register[i])
        
def high():
    return [0, 1]

def low():
    return [1, 0]

def addermodn(bits, n):
    qa = QuantumRegister(bits)
    qb = QuantumRegister(bits + 1)
    qc = QuantumRegister(bits)
    qn = QuantumRegister(bits)
    qt = QuantumRegister(1)
    
    addmod_circ = QuantumCircuit(qa, qb, qc, qn, qt, name='MODADDn')
    addmod_circ.append(adder(bits), [*qa] + [*qb] + [*qc])
    for i in range(bits):
        addmod_circ.swap(qa[i], qn[i])
    addmod_circ.append(dadder(bits), [*qa] + [*qb] + [*qc])
    
    addmod_circ.x(qb[bits])
    addmod_circ.cnot(qb[bits], qt[0])
    addmod_circ.x(qb[bits])
    m = n
    nbits = []
    for i in range(bits):
        bit = (m) & 1
        nbits = nbits + [bit]
        m = (m >> 1)
    for i in reversed(range(bits)):
        bit = nbits[i]
        if bit == 1:
            addmod_circ.cnot(qt[0], qa[i])
    addmod_circ.append(adder(bits), [*qa] + [*qb] + [*qc])
    
    for i in range(bits):
        bit = nbits[i]
        if bit == 1:
            addmod_circ.cnot(qt[0], qa[i])
            
    addmod_circ.barrier()
    for j in range(bits):
        addmod_circ.swap(qa[j], qn[j])
    
    addmod_circ.append(dadder(bits), [*qa] + [*qb] + [*qc])
      
    addmod_circ.cnot(qb[bits], qt[0])

    addmod_circ.append(adder(bits), [*qa] + [*qb] + [*qc])
    
    addmod_circ.draw('mpl', filename='addmod.qg.png')
    
    return addmod_circ.to_instruction()

def addermod(bits):
    qa = QuantumRegister(bits)
    qb = QuantumRegister(bits + 1)
    qc = QuantumRegister(bits)
    qn = QuantumRegister(bits)
    qn2 = QuantumRegister(bits)
    qt = QuantumRegister(1)
    '''
    qa(bits) qb(bits+1) qc(bits) qn(bits) qn2(bits) qt(1)
    qn2, qc and gt should be prepared in state zero
    '''
    
    addmod_circ = QuantumCircuit(qa, qb, qc, qn, qn2, qt, name='MODADD')
    
    for i in reversed(range(bits)):
        addmod_circ.cx(qn[i], qn2[i])
        
    addmod_circ.barrier()

    
    addmod_circ.append(adder(bits), [*qa] + [*qb] + [*qc])
    for i in range(bits):
        addmod_circ.swap(qa[i], qn[i])
    addmod_circ.append(dadder(bits), [*qa] + [*qb] + [*qc])
    
    addmod_circ.x(qb[bits])
    addmod_circ.cnot(qb[bits], qt[0])
    addmod_circ.x(qb[bits])
    
    for i in reversed(range(bits)):
        addmod_circ.ccx(qt[0], qn2[i], qa[i])

    addmod_circ.append(adder(bits), [*qa] + [*qb] + [*qc])
    
    for i in range(bits):
        addmod_circ.ccx(qt[0], qn2[i], qa[i])

            
    addmod_circ.barrier()
    for j in range(bits):
        addmod_circ.swap(qa[j], qn[j])
    
    addmod_circ.append(dadder(bits), [*qa] + [*qb] + [*qc])
      
    addmod_circ.cnot(qb[bits], qt[0])

    addmod_circ.append(adder(bits), [*qa] + [*qb] + [*qc])
    
    for i in range(bits):
        addmod_circ.cnot(qn[i], qn2[i])
    
    addmod_circ.draw('mpl', filename='addmod_good.qg.png')
    
    return addmod_circ.to_instruction()

'''
    Duplicator - slow as hell
    Would've worked better with just sliding
'''
def badncd(bits):
    qz = QuantumRegister(bits+1)
    qa = QuantumRegister(bits+1)
    qb = QuantumRegister(bits + 1)
    qc = QuantumRegister(bits)
    qn = QuantumRegister(bits)
    qn2 = QuantumRegister(bits)
    qt = QuantumRegister(1)
    
    dupl_circ =  QuantumCircuit(qz,qa,qb,qc,qn,qn2,qt, name = 'DONT_NCD')
    
    for i in range(bits):
        dupl_circ.cnot(qz[i], qa[i])
    
    dupl_circ.append(addermod(bits), RegisterUtils.join(qa[0:bits], qb, qc, qn, qn2, qt))
    
    for i  in range(bits+1):
        dupl_circ.swap(qz[i], qb[i])
    
    dupl_circ.append(addermod(bits), RegisterUtils.join(qa[0:bits], qb, qc, qn, qn2, qt))
    
    for i  in range(bits+1):
        dupl_circ.swap(qz[i], qb[i])
        
    dupl_circ.append(addermod(bits), RegisterUtils.join(qa[0:bits], qb, qc, qn, qn2, qt))

    for i in range(bits):
        dupl_circ.cnot(qz[i], qb[i])
    
    for i  in range(bits+1):
        dupl_circ.swap(qz[i], qa[i])
    
    return dupl_circ.to_instruction()

def ncd(bits):
    qa = QuantumRegister(bits)
    qb = QuantumRegister(bits + 1)
    qc = QuantumRegister(bits)
    qn = QuantumRegister(bits)
    qn2 = QuantumRegister(bits)
    qt = QuantumRegister(1)
    
    dupl_circ =  QuantumCircuit(qa,qb,qc,qn,qn2,qt, name = 'NCD')
    
    for i in range(bits):
        dupl_circ.cnot(qa[i], qb[i])
    
    dupl_circ.append(addermod(bits), RegisterUtils.join(qa, qb, qc, qn, qn2, qt))
   
    return dupl_circ.to_instruction()

def rslide(bits, k):
    data = QuantumRegister(bits)
    ancilla = AncillaRegister(k)
    c = QuantumRegister(1)
    
    circ = QuantumCircuit(data, ancilla, c, name='RSLIDE')
    
    for i in range(k-1):
        circ.swap(ancilla[i], ancilla[i+1])
    if k > 0:
        circ.swap(ancilla[k-1], data[bits-1])
    
    for i in reversed(range(bits)):
        if i > 0:
            circ.swap(data[i], data[i-1])
    if k >= 1:
        circ.cswap(c[0], ancilla[k-1], data[0])
    
    return circ.to_instruction()



def crslide(bits, k):
    data = QuantumRegister(bits)
    ancilla = AncillaRegister(k)
    ctrl = QuantumRegister(1)
    
    circ = QuantumCircuit(data, ancilla, ctrl, name='RSLIDE')
    
    circ.x(ctrl)
    for i in range(k-1):
        circ.cswap(ctrl[0],ancilla[i], ancilla[i+1])
    if k > 0:
        circ.cswap(ctrl[0],ancilla[k-1], data[bits-1])
    
    for i in reversed(range(bits)):
        if i > 0:
            circ.cswap(ctrl[0],data[i], data[i-1])
    if k >= 1:
        circ.cswap(ctrl[0], ancilla[k-1], data[0])
    circ.x(ctrl)
    return circ.to_instruction()

'''
    Useful
'''
class RegisterUtils:
    def join(*regs):
        ar = []
        for r in regs:
            ar = ar + [*r]
        return ar
'''
    Useful
'''
class DefiniteStates:
    def binary(n, bits):
        ar = []
        binary = bin(n)[2:]
        for i in binary:
            if str(i) == '0':
                ar = [low()] + ar
            else:
                ar = [high()] + ar 
        k = len(ar)
        while k < bits:
            ar = ar + [low()]
            k = k + 1
        return ar

    def h(bits):
        ar = []
        for i in range(bits):
            ar = ar + [[1/sqrt(2), 1/sqrt(2)]]
        return ar
            
'''
    Rough implementations of QFT
'''      
class QuantumPeriodGates:
    def qft_rotations(circuit, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return circuit
        n -= 1
        circuit.h(n)
        for qubit in range(n):
            circuit.cp(pi/2**(n-qubit), qubit, n)
        # At the end of our function, we call the same function again on
        # the next qubits (we reduced n by one earlier in the function)
        QuantumPeriodGates.qft_rotations(circuit, n)
    
    def swap_registers(circuit, n):
        for qubit in range(n//2):
            circuit.swap(qubit, n-qubit-1)
        return circuit

    def qft(bits):
        a = QuantumRegister(bits)
        qft_circ = QuantumCircuit(a, name='QFT')
        QuantumPeriodGates.qft_rotations(qft_circ, bits)
        QuantumPeriodGates.swap_registers(qft_circ, bits)
        
        qft_circ.draw('mpl', filename='qft.qg.png')

        return qft_circ.to_instruction()

class QFTArithmetic:
    def QFTInPlaceAdder(in_bits):
        a = QuantumRegister(in_bits)
        b = QuantumRegister(in_bits + 1)
        circ = QuantumCircuit(a, b, name='QFTPadder')
        circ.append(QFT(in_bits+1, do_swaps=False).to_gate(), RegisterUtils.join(b))
        for k in range(in_bits + 1):
            for e in range(in_bits):
                ang = (2 * pi) / (2 ** (k + 1 - e))
                circ.append(PhaseGate(ang).control(1), [a[e], b[k]])
        circ.append(QFT(in_bits+1, do_swaps=False).inverse().to_gate(), RegisterUtils.join(b))
        return circ.to_gate()
    
    def QFTInPlaceDAdder(in_bits):
        a = QuantumRegister(in_bits)
        b = QuantumRegister(in_bits + 1)
        circ = QuantumCircuit(a, b, name='QFTPadder_dg')
        circ.append(QFT(in_bits+1, do_swaps=False).to_gate(), RegisterUtils.join(b))
        for k in range(in_bits + 1):
            for e in range(in_bits):
                ang = -(2 * pi) / (2 ** (k + 1 - e))
                circ.append(PhaseGate(ang).control(1), [a[e], b[k]])
        circ.append(QFT(in_bits+1, do_swaps=False).inverse().to_gate(), RegisterUtils.join(b))
        return circ.to_gate()
    
    '''
        N = D * Q + R
         
        Input registers: n(bits), d(bits), r(bits):0, q(bits):0, anc(3):0
        Output (in place): n, d, r: n%d, q: n/d, anc':garbage
        
            |n\ |d\ |0\ |0\ |000\ => |n\ |d\ |n%d\ |n/d\ |***\ 
        
        Pseudo code thanks to wikipedia:
        | --------------------------------------------------------------------------------------------------
        |  
        |  Q := 0                  -- Initialize quotient and remainder to zero
        |  R := 0                     
        |  for i := n - 1 .. 0 do  -- Where n is number of bits in N
        |      R := R << 1           -- Left-shift R by 1 bit
        |      R(0) := N(i)          -- Set the least-significant bit of R equal to bit i of the numerator
        |      if R ≥ D then
        |          R := R - D
        |          Q(i) := 1
        |      end
        |  end
    '''
    def QFTRemainderTheorem(in_bits, h = -1):
        n = QuantumRegister(in_bits)
        d = QuantumRegister(in_bits)
        r = QuantumRegister(in_bits)
        anc = QuantumRegister(3)
        q = QuantumRegister(in_bits)
        
        
        circ = QuantumCircuit(n, d ,r, q, anc, name='QFTRTH')
        ipadd = QFTArithmetic.QFTInPlaceAdder(in_bits)
    
        u = 0

        leftshift = rslide(in_bits, 1)
        for i in reversed(range(in_bits)):
            u = u + 1
            circ.append(leftshift, RegisterUtils.join(r, anc[0:2]))

            circ.cnot(n[i], r[0])
            
            circ.append(ipadd.inverse(), RegisterUtils.join(d, r, anc[0:1]))
            
            circ.cnot(anc[0], q[i])
            
            circ.append(ipadd, RegisterUtils.join(d, r, anc[0:1]))
            
            circ.x(q[i])

            circ.append(ipadd.inverse().control(1), [q[i]] + RegisterUtils.join(d, r, anc[0:1]))

            if h != -1 and u >= h:
                print(f'@debug RTH_Gate: Stopped_At( \n \tu: {u}\n\tLast step: i = {i}\n)')
                break

        return circ.to_instruction()
            
            
            
    '''
        QFT ModularMultiply gate is still in progress and will be implemented 
        with 3 QFTRemainderTheorem gates and one Phase Multiplication
    '''
    def QFTModularMultiply(in_bits, out_bits):
        a = QuantumRegister(in_bits)
        b = QuantumRegister(in_bits)
        n = QuantumRegister(in_bits)
        out = QuantumRegister(out_bits)
        t = QuantumRegister(in_bits)
        x = QuantumRegister(1)
        
        circ = QuantumCircuit(a, b, n, out, t, x, name='QFTMM')
        
        circ.append(QFT(out_bits, do_swaps=False).to_gate(), RegisterUtils.join(out))
        
        # 2 x QFTRTH

        # QFTMultiply
        for i in range(in_bits):
            for j in range(in_bits):
                for k in range(out_bits):
                    ang = (2 * pi) / (2 ** (k + 1 - i - j))
                    circ.append(PhaseGate(ang).control(2), [a[j], b[i], out[k]])

        circ.append(QFT(out_bits, do_swaps=False).inverse().to_gate(), RegisterUtils.join(out))

        # 2 x QFTRTH

        return circ.to_gate()

def all():
    return ['ADD', 'CARRY', 'SUM', 'CARRY_dg', 'SUM_dg', 'ADD_dg', 'MODADDn', 'MODADDn_dg', 'MODADD', 'MODADD_dg', 'QFT', 'QFT_dg', 'NCD', 'NCD_dg', 'LSLIDE', 'LSLIDE_dg', 'RSLIDE', 'RSLIDE_dg']
