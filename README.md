# qamg + mohican

See Mohican basic code in the Mohican folder.
Qiskit links are in code.

Basic example for:
- Aer (slow ish simulator)
- Modular addition and duplication (with selfmade gates.py)
- Squaring register (with qiskit builtin function)

# Long term goals
- Achieving a working implementation of Shor's algorithm
with changeble inputs (no custom made circuit)

# Useful for understanding
- [https://medium.com/mit-6-s089-intro-to-quantum-computing/a-general-implementation-of-shors-algorithm-da1595694430](https://medium.com/mit-6-s089-intro-to-quantum-computing/a-general-implementation-of-shors-algorithm-da1595694430)
- [https://arxiv.org/pdf/quant-ph/0112107.pdf](https://arxiv.org/pdf/quant-ph/0112107.pdf)
- [https://apps.dtic.mil/sti/pdfs/AD1083851.pdf](https://apps.dtic.mil/sti/pdfs/AD1083851.pdf)
- [https://arxiv.org/pdf/1202.6614.pdf](https://arxiv.org/pdf/1202.6614.pdf)
- [https://arxiv.org/pdf/quant-ph/0406176.pdf](https://arxiv.org/pdf/quant-ph/0406176.pdf)
- [Some nice video courses on qutube](https://www.qutube.nl/quantum-computer-12/surface-codes)

# Resources
- [https://quantum-computing.ibm.com](https://quantum-computing.ibm.com)
- [Qiskit](https://qiskit.org/textbook/ch-prerequisites/setting-the-environment.html)


# Noise QEC
- [QEC Codes](https://bvermersch.github.io/Teaching/QO_Lecture3.pdf)
- [QEC Correction](https://wdscultan.github.io/files/QEC.pdf)
- [https://en.wikipedia.org/wiki/Quantum_error_correction](https://en.wikipedia.org/wiki/Quantum_error_correction)
- [https://arxiv.org/pdf/1808.06709.pdf](https://arxiv.org/pdf/1808.06709.pdf)
- [Noise models in qiskit](https://qiskit.org/textbook/ch-quantum-hardware/error-correction-repetition-code.html)

# History
- 15.Feb.23 : Added QFTRemainderTheorem (RTH)
- 16.Feb.23 : Added qMUX
- 17.Feb.23 : Added qENCODER with custom function (QPE generalization)

## Note:
Run the following command if problems with imports and modules arrise:
```bash
export PYTHONPATH=$PYTHONPATH:<yourpath> 
```
'yourpath' is the output os the **pwd** command in the root directory
