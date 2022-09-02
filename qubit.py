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
    def cnot(self, control, target):
        for i, amp in enumerate(self.states):
            if str(bin(i)[2:].zfill(self.length))[control-1] == '1':
                pos = i + (2**(self.length-target))
                print(pos)
                if pos > self.length:
                    break
                self.states[i] = self.states[pos]
                self.states[pos] = amp
                print(amp)

q1 = Qubit(0,1)
q2 = Qubit(0.5, 0.5)

circuit = Quantum_Circuit(q1, q2)

circuit.measure()
circuit.state()
circuit.probs()
print(circuit.result[0])
print(circuit.result[1])
