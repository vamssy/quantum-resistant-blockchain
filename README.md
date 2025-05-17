# Quantum-Resistant Blockchain

A blockchain implementation that compares traditional ECDSA signatures with post-quantum CRYSTALS-Dilithium signatures, demonstrating the security advantages and performance tradeoffs of quantum-resistant cryptography in distributed ledger systems.

## Project Overview

This project implements a blockchain system that supports both classical ECDSA signatures and quantum-resistant Dilithium signatures. It provides comprehensive performance metrics and visualizations to compare these two approaches, helping to understand the tradeoffs involved in adopting post-quantum cryptography for blockchain applications.

Key features:
- Simulated implementation of CRYSTALS-Dilithium signatures
- Traditional ECDSA signature implementation
- Comparative performance analysis
- Quantum security visualization
- Web interface for blockchain interaction

## Project Structure

```
quantum-resistant-blockchain/
│
├── blockchain.py              # Core blockchain implementation
├── crypto_utils.py            # Cryptographic utilities for both signature schemes
├── main.py                    # Main application entry point
├── performance_test.py        # Dilithium-only performance test
├── comparative_test.py        # Dilithium vs ECDSA comparison test
├── quantum_security_analysis.py # Security analysis visualization
├── app.py                     # Flask web interface
│
├── requirements.txt           # Dependencies list
│
├── results/                   # Generated when tests are run
│   ├── metrics.json           # Dilithium performance metrics
│   ├── ecdsa_metrics.json     # ECDSA performance metrics
│   ├── comparative_metrics.json # Comparison metrics
│   ├── charts/                # Generated comparison charts
│   └── quantum_analysis/      # Quantum security analysis results
│
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quantum-resistant-blockchain.git
cd quantum-resistant-blockchain
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Application

The main application provides several options:

```bash
python main.py
```

This will present a menu with the following options:
1. Run basic functionality test
2. Run Dilithium performance test (1,000 transactions)
3. Run comparative test (Dilithium vs ECDSA)
4. Run quantum security analysis
5. Run all tests

### Running Specific Tests

You can also run specific tests directly:

```bash
# For Dilithium performance test
python performance_test.py

# For comparative test (Dilithium vs ECDSA)
python comparative_test.py

# For quantum security analysis
python quantum_security_analysis.py
```

### Web Interface

To run the web interface:

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5001`.

## Results

After running the tests, results will be available in the `results` directory:

- `metrics.json`: Dilithium performance metrics
- `ecdsa_metrics.json`: ECDSA performance metrics
- `comparative_metrics.json`: Comparison between both schemes
- `charts/`: Visual comparisons of performance metrics
- `quantum_analysis/`: Security analysis data and visualizations

## Key Findings

The implementation demonstrates that:

1. Dilithium signatures are significantly larger (~39x) than ECDSA signatures
2. Dilithium verification is slower (~10x) than ECDSA verification
3. Despite these tradeoffs, Dilithium provides quantum resistance that ECDSA lacks
4. The blockchain can still achieve reasonable throughput with Dilithium signatures

## Requirements

- Python 3.8+
- pycryptodome
- flask
- matplotlib
- numpy

## Note for macOS Users

If you're using macOS and encounter port conflicts when running the web interface, use the following command instead:

```bash
python app.py
```

The app is configured to use port 5001 to avoid conflicts with AirPlay.
