import numpy as np
import random

class Qubit:
    def __init__(self, alpha, beta):
        self.states = []
        squareSum = alpha*np.conj(alpha) + beta*np.conj(beta)
        modulus = np.sqrt(squareSum)
        self.states.append(alpha / modulus)
        self.states.append(beta / modulus)
        self.matrix = np.array([[self.states[0]],[self.states[1]]])
    def state(self):
        print(round(float(self.states[0]), 15), round(float(self.states[1]), 15))
    def probs(self):
        print(round(float(self.states[0]*np.conj(self.states[0])), 15), round(float(self.states[1]*np.conj(self.states[1])), 15))
    def measure(self):
        rnd = random.random()
        if rnd <= self.states[0] * np.conj(self.states[0]):
            self.result = 0
        else:
            self.result = 1
    def gate(self, operator):
        if operator == 'X':
            gateMat = np.array([[0, 1],[1, 0]])
        elif operator == 'Z':
            gateMat = np.array([[1, 0],[0, -1]])
        elif operator == 'Y':
            gateMat = np.array([[0, -1j],[1j, 0]])
        elif operator == 'H':
            gateMat = np.array([[1/np.sqrt(2), 1/np.sqrt(2)],[1/np.sqrt(2), -1/np.sqrt(2)]])
        else:
            print('Invalid operator')
        result = np.matmul(gateMat, self.matrix)
        self.states[0] = result[0]
        self.states[1] = result[1]

class Quantum_Circuit:
    def __init__(self, *argv):
        self.qubits = argv
        self.length = len(argv)
        self.states = []
        self.createStates()
    def createStates(self):
        for i in range(2**len(self.qubits)):
            tempBin = bin(i)[2:].zfill(self.length)
            result = 1
            for j in range(self.length):
                result = result * self.qubits[j].states[int(tempBin[j-1])]
            self.states.append(result)
    def state(self):
        for i, amp in enumerate(self.states):
            print(round(float(amp), 15), end = " ")
        print()
    def probs(self):
        for i, amp in enumerate(self.states):
            print(round(float(amp*np.conj(amp)), 15), end = " ")
        print()
    def measure(self):
        rnd = random.random()
        total = 0
        for i, amp in enumerate(self.states):
            total += (amp * np.conj(amp))
            if rnd <= total:
                self.result = bin(i)[2:].zfill(self.length)
                break
    def update(self, *argv):
        self.qubits = argv
        self.states = []
        self.createStates()

'initialise qubits      
q1 = Qubit(1, 0)
q2 = Qubit(1, 0)

'initialise the circuit using these qubits
circuit = Quantum_Circuit(q1,q2)
circuit.state()

'apply hadamard gate to qubit 1
q1.gate('H')
'apply not gate to qubit 2
q2.gate('X')

'update the circuit with new qubit
circuit.update(q1, q2)
'print state of the two qubits combined
circuit.state()
'print probabilities of each state being outputted when measured
circuit.probs()
'measure both qubits at once
circuit.measure()
print(circuit.result)
