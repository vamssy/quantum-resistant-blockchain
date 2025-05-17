import json
import os
import matplotlib.pyplot as plt
import numpy as np

def analyze_quantum_security():
    """Analyze and visualize the quantum security of ECDSA vs Dilithium"""
    print("\n=== Quantum Security Analysis ===")
    
    # Create results directory
    os.makedirs('results/quantum_analysis', exist_ok=True)
    
    # Security levels against classical and quantum computers (in bits)
    security_data = {
        'ECDSA (P-256)': {
            'classical_security': 128,
            'quantum_security': 0,  # Effectively broken by Shor's algorithm
            'vulnerable_to_quantum': True
        },
        'Dilithium (Level 2)': {
            'classical_security': 128,
            'quantum_security': 128,  # Maintains security level
            'vulnerable_to_quantum': False
        }
    }
    
    # Save security data
    with open('results/quantum_analysis/security_levels.json', 'w') as f:
        json.dump(security_data, f, indent=4)
    
    # Generate security comparison chart
    plt.figure(figsize=(12, 6))
    
    algorithms = list(security_data.keys())
    classical_security = [security_data[algo]['classical_security'] for algo in algorithms]
    quantum_security = [security_data[algo]['quantum_security'] for algo in algorithms]
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    plt.bar(x - width/2, classical_security, width, label='Classical Security (bits)')
    plt.bar(x + width/2, quantum_security, width, label='Quantum Security (bits)')
    
    plt.ylabel('Security Level (bits)')
    plt.title('Security Against Classical vs Quantum Attacks')
    plt.xticks(x, algorithms)
    plt.legend()
    
    # Add text annotations
    for i, algo in enumerate(algorithms):
        if security_data[algo]['vulnerable_to_quantum']:
            plt.text(i, 10, "VULNERABLE TO\nQUANTUM ATTACKS", 
                    ha='center', va='center', color='red', fontweight='bold')
    
    plt.savefig('results/quantum_analysis/security_comparison.png')
    
    # Estimated resources to break each algorithm
    resources_data = {
        'ECDSA (P-256)': {
            'qubits_required': 2330,  # Based on research for breaking P-256
            'estimated_break_time': "Hours to days with sufficient quantum computer"
        },
        'Dilithium (Level 2)': {
            'qubits_required': "Unknown - No known quantum attack",
            'estimated_break_time': "Beyond foreseeable quantum capabilities"
        }
    }
    
    with open('results/quantum_analysis/breaking_resources.json', 'w') as f:
        json.dump(resources_data, f, indent=4)
    
    print("Quantum security analysis completed. Results saved to results/quantum_analysis/")
    
    return security_data, resources_data

if __name__ == "__main__":
    analyze_quantum_security()
