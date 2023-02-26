# qamg + mohican

# Important!
## AMG-ul:
## Open issues for any quaestion you have so we can solve it

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
- [Basics](https://arxiv.org/pdf/quant-ph/0406176.pdf)
- [Shor algorithm and QFT intuition (medium.com)](https://medium.com/mit-6-s089-intro-to-quantum-computing/a-general-implementation-of-shors-algorithm-da1595694430)
- [Register shift](https://arxiv.org/pdf/quant-ph/0112107.pdf)
- [Performant modular multiplicators: QFT and binary](https://apps.dtic.mil/sti/pdfs/AD1083851.pdf)
- [Arithmetic gates with modular parameter, optimized for shor's algorithm](https://arxiv.org/pdf/1202.6614.pdf)
- [Some nice video courses on qutube](https://www.qutube.nl/quantum-computer-12/surface-codes)

# In-depth Arithmetics
- [Fast Modular Exponential Architecture](https://www.researchgate.net/publication/228102587_Fast_Quantum_Modular_Exponentiation_Architecture_for_Shor%27s_Factorization_Algorithm)

# Resources
- [https://quantum-computing.ibm.com](https://quantum-computing.ibm.com)
- [Qiskit](https://qiskit.org/textbook/ch-prerequisites/setting-the-environment.html)


# Basic QEC [For more indepth, view next section]
- [QEC Codes](https://bvermersch.github.io/Teaching/QO_Lecture3.pdf)
- [QEC Correction](https://wdscultan.github.io/files/QEC.pdf)
- [https://en.wikipedia.org/wiki/Quantum_error_correction](https://en.wikipedia.org/wiki/Quantum_error_correction)
- [https://arxiv.org/pdf/1808.06709.pdf](https://arxiv.org/pdf/1808.06709.pdf)
- [Noise models in qiskit](https://qiskit.org/textbook/ch-quantum-hardware/error-correction-repetition-code.html)

# Surface codes: in-depth dive
- [Toric surface code explained on stackexchange. Also helps for a basic understanding of surface codes](https://quantumcomputing.stackexchange.com/questions/2106/what-is-the-surface-code-in-the-context-of-quantum-error-correction)
- [Logical cubits and gates, single and double X/Z-cut logical bits, and useful implementations of measurement and initialization operations on QEC surface codes](https://arxiv.org/pdf/1208.0928.pdf)
- [Nature cool article](https://www.nature.com/articles/s41586-022-05434-1)
- [Noise models in qiskit](https://qiskit.org/textbook/ch-quantum-hardware/error-correction-repetition-code.html)

# History
- 15.Feb.23 : Added QFTRemainderTheorem (RTH)
- 16.Feb.23 : Added qMUX
- 17.Feb.23 : Added qENCODER with custom function (QPE generalization)
- 17.Feb.23 : Beginining to study Black codes and Quantum Surface Codes
- 24.Feb.23 : Added MPGs (parametrized gates): SCMM and SMA

# TODOs
- Read about block codes [Done]
- Surface codes in depth

## Note:
Run the following command in the root folder if problems with imports and modules arrise:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
```
'yourpath' is the output of the **pwd** command in the root directory
