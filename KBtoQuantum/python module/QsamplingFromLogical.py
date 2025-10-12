import numpy as np
import qiskit as qis

from qiskit.quantum_info.operators.random import * 
from qiskit_aer import AerSimulator
from qiskit.quantum_info import *

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, plot_bloch_multivector

from matplotlib.pyplot import figure
import itertools


"""Code elements for the mapping procedure"""

def extractvariables(expr):
    """Recursively extract unique variables from a logical expression."""
    variables = set()
    if isinstance(expr, list):
        for subexpr in expr[1:]:  # Skip the connective at index 0
            variables.update(extractvariables(subexpr))
    elif isinstance(expr, str):
        variables.add(expr)
    return variables

def countconnectives(expr):
    """Recursively count logical connectives in a logical expression."""
    count = 0
    if isinstance(expr, list):
        count += 1  # Count this connective
        for subexpr in expr[1:]:  # Skip the connective at index 0
            count += countconnectives(subexpr)
    return count

def resolveexpression(expr, circuit, qubitsmap, ancillastart, ancillacounter):
    """
    Recursively resolve logical expressions into quantum gates.
    Returns the qubit index storing this subexpression's result.
    """
    if isinstance(expr, str):  # It's a variable
        return qubitsmap[expr]

    gate = expr[0]  # Logical connective
    args = expr[1:]

    # Recursively resolve arguments
    resolved_args = [resolveexpression(arg, circuit, qubitsmap, ancillastart, ancillacounter) for arg in args]
    target = ancillastart + ancillacounter[0]
    ancillacounter[0] += 1  # Increment counter

    # Apply quantum gates for each logical connective
    if gate == "not" and len(resolved_args) == 1:
        circuit.x(resolved_args[0])
        circuit.cx(resolved_args[0], target)
    elif gate == "and" and len(resolved_args) == 2:
        q1, q2 = resolved_args
        circuit.ccx(q1, q2, target)
    elif gate == "or" and len(resolved_args) == 2:
        q1, q2 = resolved_args
        circuit.cx(q1, target)
        circuit.cx(q2, target)
        circuit.ccx(q1, q2, target)
    elif gate == "xor" and len(resolved_args) == 2:
        q1, q2 = resolved_args
        circuit.cx(q1, target)
        circuit.cx(q2, target)
    elif gate == "implication" and len(resolved_args) == 2:
        q1, q2 = resolved_args
        circuit.x(q1)
        circuit.cx(q1, target)
        circuit.x(q1)
        circuit.cx(q2, target)
    elif gate == "bijection" and len(resolved_args) == 2:
        q1, q2 = resolved_args
        circuit.cx(q1, target)
        circuit.cx(q2, target)
        circuit.x(target)
    else:
        raise ValueError(f"Unknown or improperly formatted gate: {gate}")

    return target

"""The mapping procedure"""

def logicaltoquantum(expression):
    """
    Maps a logical expression to a quantum circuit with dynamic qubit allocation.
    Returns the circuit and the variable-to-qubit mapping.
    """
    """Automatically maps logical expressions to quantum circuits with dynamic qubit allocation."""
    # Extract variables and count connectives
    variables = extractvariables(expression)
    num_ancilla = countconnectives(expression)

    # Dynamic Qubit Mapping
    var_list = sorted(list(variables))  #sort the variables
    qubitsmap = {var: idx for idx, var in enumerate(var_list)} #get the qubits from the no. of variables
    ancilla_start = len(qubitsmap) #have the ancillas properly sorted
    ancilla_map = {f"anc{i+1}": ancilla_start + i for i in range(num_ancilla)}    #get the qubits from the no. of ancillas
    qubitsmap.update(ancilla_map)  #update the no. of qubits

    # Create Quantum Register with Named Qubits

    circuit = QuantumCircuit()
    for name in sorted(variables):
        qreg = QuantumRegister(1, name=name)
        circuit.add_register(qreg)
        
    anc_reg = QuantumRegister(num_ancilla, name = "anc")
    """out_reg = ClassicalRegister(1, name = "OUT")
    circuit.add_register(anc_reg, out_reg)"""
    circuit.add_register(anc_reg)

    #Add Hadamard Gates to Basis Qubits to create superposition
    basis_qubits = set(range(len(variables)))  # Indices of the logical variables
    for q in basis_qubits:
        circuit.h(q)  # Apply Hadamard to each basis qubit

    # Resolve the expression
    ancilla_counter = [0]  # Use a list to keep the counter mutable
    final_result = resolveexpression(expression, circuit, qubitsmap, ancilla_start, ancilla_counter)
    #print(f"Final result stored in qubit: {final_result}")  #show where do we store the final qubit
    
    return circuit, qubitsmap

"""Formula evaluation for truth probabilities of 0 and 1 states"""

def eval_formula(formula, assignment):
    if isinstance(formula, str):  # variable
        return assignment[formula]
    op = formula[0]
    if op == 'not':
        return 1 - eval_formula(formula[1], assignment)
    elif op == 'and':
        return eval_formula(formula[1], assignment) * eval_formula(formula[2], assignment)
    elif op == 'or':
        return max(eval_formula(formula[1], assignment), eval_formula(formula[2], assignment))
    elif op == 'implication':
        left = eval_formula(formula[1], assignment)
        right = eval_formula(formula[2], assignment)
        return max(1 - left, right)   # (¬left) ∨ right
    elif op == 'xor':
        left = eval_formula(formula[1], assignment)
        right = eval_formula(formula[2], assignment)
        return (left + right) % 2
    elif op == 'bijection':  # logical equivalence
        left = eval_formula(formula[1], assignment)
        right = eval_formula(formula[2], assignment)
        return 1 if left == right else 0
    else:
        raise ValueError(f"Unknown operator {op}")

def formula_probability(formula, variables):
    probs = {var: 0.5 for var in sorted(variables)}
    vars_ = list(probs.keys())
    total = 0.0
    for values in itertools.product([0,1], repeat=len(vars_)):
        assignment = dict(zip(vars_, values))
        # joint probability under independence
        p = 1.0
        for v in vars_:
            p *= probs[v] if assignment[v] == 1 else (1 - probs[v])
        if eval_formula(formula, assignment):
            total += p
    return total

"""Oracle and diffusion operators for amplitude amplification"""
"""Oracle is generated for states 0 and 1 as well, but chosen by the program, for the one with the lower probabilty"""

def amplification_rounds(formula, variables):
    c1 = formula_probability(formula, variables)
    if (1-c1) < c1:
        rounds = int(np.floor(np.pi/4 * np.sqrt(1/(1-c1))))
        prob = 1-c1
    else:
        rounds = int(np.floor(np.pi/4 * np.sqrt(1/(c1))))
        prob = c1

    return rounds, prob


def oracle_generate(input_circ, prob):
    len = input_circ.num_qubits
    orac = QuantumCircuit(len)
    if 1-prob < prob:
        orac.x(len - 1)
        orac.z(len - 1)
        orac.x(len - 1)
    else:
        orac.z(len - 1)

    return orac

def diffusion_generate(input_circ):
    len = input_circ.num_qubits
    b1 = QuantumCircuit(len)
    b2 = b1.compose(input_circ.inverse())

    for qubit in range(len ):
        b2.x(qubit)

    b2.h(len - 1)
    b2.mcx(list(range(0, len - 1)), len - 1)
    b2.h(len - 1)

    for qubit in range(len ):
        b2.x(qubit)

    diffusion = b2.compose(input_circ)

    return diffusion

"""Applying Oracle and diffusion operators iteratively"""

def apply_operators(circuit, oracle, amplifier, rounds):
    for _ in range(rounds):
        circuit = circuit.compose(oracle).compose(amplifier)

    return circuit


def generate_amplified_circuits(base_circuit, oracle, diffuser, max_rounds):
    amplified_circuits = {0: base_circuit}
    for i in range(1, max_rounds + 1):
        amplified_circuits[i] = apply_operators(amplified_circuits[i-1], oracle, diffuser, 1)
    return amplified_circuits
