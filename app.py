from flask import Flask, jsonify, request, render_template_string
from blockchain import Blockchain
from crypto_utils import Wallet, CryptoManager
import binascii
import json
import time
import os

app = Flask(__name__)

# Initialize blockchain
blockchain = Blockchain(difficulty=2)  # Lower difficulty for demo

# Create wallets
dilithium_wallet = Wallet('dilithium')
ecdsa_wallet = Wallet('ecdsa')

# Simple HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Quantum-Resistant Blockchain</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #333;
        }
        .container {
            background-color: #f9f9f9;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
        pre {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
            margin-bottom: 20px;
        }
        .tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            color: black;
        }
        .tab button:hover {
            background-color: #ddd;
        }
        .tab button.active {
            background-color: #ccc;
        }
        .tabcontent {
            display: none;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-top: none;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        .chart-container {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Quantum-Resistant Blockchain Comparison</h1>
    
    <div class="tab">
        <button class="tablinks active" onclick="openTab(event, 'Blockchain')">Blockchain</button>
        <button class="tablinks" onclick="openTab(event, 'Dilithium')">Dilithium</button>
        <button class="tablinks" onclick="openTab(event, 'ECDSA')">ECDSA</button>
        <button class="tablinks" onclick="openTab(event, 'Comparison')">Comparison</button>
        <button class="tablinks" onclick="openTab(event, 'Security')">Security Analysis</button>
    </div>
    
    <div id="Blockchain" class="tabcontent" style="display: block;">
        <h2>Blockchain Operations</h2>
        
        <div class="container">
            <h3>Mine a Block</h3>
            <button id="mineDilithiumButton">Mine with Dilithium</button>
            <button id="mineECDSAButton">Mine with ECDSA</button>
            <div id="mineResult"></div>
        </div>
        
        <div class="container">
            <h3>View Blockchain</h3>
            <button id="viewBlockchainButton">View Blockchain</button>
            <pre id="blockchainData"></pre>
        </div>
    </div>
    
    <div id="Dilithium" class="tabcontent">
        <h2>Dilithium Performance Metrics</h2>
        
        <div class="container">
            <h3>Dilithium Metrics</h3>
            <button id="viewDilithiumMetricsButton">View Metrics</button>
            <pre id="dilithiumMetricsData"></pre>
        </div>
    </div>
    
    <div id="ECDSA" class="tabcontent">
        <h2>ECDSA Performance Metrics</h2>
        
        <div class="container">
            <h3>ECDSA Metrics</h3>
            <button id="viewECDSAMetricsButton">View Metrics</button>
            <pre id="ecdsaMetricsData"></pre>
        </div>
    </div>
    
    <div id="Comparison" class="tabcontent">
        <h2>Comparison: Dilithium vs ECDSA</h2>
        
        <div class="container">
            <h3>Comparative Metrics</h3>
            <button id="viewComparisonButton">View Comparison</button>
            <div id="comparisonResult">
                <table id="comparisonTable" style="display: none;">
                    <tr>
                        <th>Metric</th>
                        <th>ECDSA</th>
                        <th>Dilithium</th>
                        <th>Difference</th>
                    </tr>
                    <tbody id="comparisonTableBody">
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="container">
            <h3>Comparison Charts</h3>
            <div class="chart-container">
                <h4>Signature Size</h4>
                <img id="signatureSizeChart" src="/charts/signature_size_comparison.png" style="display: none; max-width: 100%;">
            </div>
            <div class="chart-container">
                <h4>Verification Time</h4>
                <img id="verificationTimeChart" src="/charts/verification_time_comparison.png" style="display: none; max-width: 100%;">
            </div>
            <div class="chart-container">
                <h4>Storage Requirements</h4>
                <img id="storageChart" src="/charts/storage_comparison.png" style="display: none; max-width: 100%;">
            </div>
            <div class="chart-container">
                <h4>Transactions Per Second</h4>
                <img id="tpsChart" src="/charts/tps_comparison.png" style="display: none; max-width: 100%;">
            </div>
        </div>
    </div>
    
    <div id="Security" class="tabcontent">
        <h2>Quantum Security Analysis</h2>
        
        <div class="container">
            <h3>Security Levels</h3>
            <button id="viewSecurityButton">View Security Analysis</button>
            <pre id="securityData"></pre>
            <div class="chart-container">
                <h4>Security Against Classical vs Quantum Attacks</h4>
                <img id="securityChart" src="/quantum_analysis/security_comparison.png" style="display: none; max-width: 100%;">
            </div>
        </div>
    </div>
    
    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            tablinks = document.getElementsByClassName("tablinks");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        
        document.getElementById('mineDilithiumButton').addEventListener('click', async () => {
            const response = await fetch('/mine/dilithium');
            const data = await response.json();
            document.getElementById('mineResult').innerHTML = `
                <p>Block mined successfully with Dilithium!</p>
                <p>Block Index: ${data.block_index}</p>
                <p>Block Hash: ${data.block_hash}</p>
            `;
        });
        
        document.getElementById('mineECDSAButton').addEventListener('click', async () => {
            const response = await fetch('/mine/ecdsa');
            const data = await response.json();
            document.getElementById('mineResult').innerHTML = `
                <p>Block mined successfully with ECDSA!</p>
                <p>Block Index: ${data.block_index}</p>
                <p>Block Hash: ${data.block_hash}</p>
            `;
        });
        
        document.getElementById('viewBlockchainButton').addEventListener('click', async () => {
            const response = await fetch('/blockchain');
            const data = await response.json();
            document.getElementById('blockchainData').textContent = JSON.stringify(data, null, 2);
        });
        
        document.getElementById('viewDilithiumMetricsButton').addEventListener('click', async () => {
            const response = await fetch('/metrics/dilithium');
            const data = await response.json();
            document.getElementById('dilithiumMetricsData').textContent = JSON.stringify(data, null, 2);
        });
        
        document.getElementById('viewECDSAMetricsButton').addEventListener('click', async () => {
            const response = await fetch('/metrics/ecdsa');
            const data = await response.json();
            document.getElementById('ecdsaMetricsData').textContent = JSON.stringify(data, null, 2);
        });
        
        document.getElementById('viewComparisonButton').addEventListener('click', async () => {
            const response = await fetch('/comparison');
            const data = await response.json();
            
            // Populate comparison table
            const tableBody = document.getElementById('comparisonTableBody');
            tableBody.innerHTML = '';
            
            // Add rows for each metric
            const metrics = [
                { name: 'Signature Size (bytes)', ecdsa: data.ecdsa.avg_signature_size_bytes, dilithium: data.dilithium.avg_signature_size_bytes },
                { name: 'Public Key Size (bytes)', ecdsa: data.ecdsa.avg_public_key_size_bytes, dilithium: data.dilithium.avg_public_key_size_bytes },
                { name: 'Private Key Size (bytes)', ecdsa: data.ecdsa.avg_private_key_size_bytes, dilithium: data.dilithium.avg_private_key_size_bytes },
                { name: 'Verification Time (ms)', ecdsa: data.ecdsa.avg_verification_time_ms, dilithium: data.dilithium.avg_verification_time_ms },
                { name: 'Signing Time (ms)', ecdsa: data.ecdsa.avg_signing_time_ms, dilithium: data.dilithium.avg_signing_time_ms },
                { name: 'Storage for 1,000 TX (MB)', ecdsa: data.ecdsa.total_signature_storage_mb, dilithium: data.dilithium.total_signature_storage_mb },
                { name: 'Transactions Per Second', ecdsa: data.ecdsa.transactions_per_second, dilithium: data.dilithium.transactions_per_second }
            ];
            
            metrics.forEach(metric => {
                const row = document.createElement('tr');
                const diff = metric.dilithium / metric.ecdsa;
                
                row.innerHTML = `
                    <td>${metric.name}</td>
                    <td>${metric.ecdsa.toFixed(2)}</td>
                    <td>${metric.dilithium.toFixed(2)}</td>
                    <td>${diff.toFixed(2)}x ${diff > 1 ? 'larger' : 'smaller'}</td>
                `;
                
                tableBody.appendChild(row);
            });
            
            document.getElementById('comparisonTable').style.display = 'table';
            
            // Show charts
            document.getElementById('signatureSizeChart').style.display = 'block';
            document.getElementById('verificationTimeChart').style.display = 'block';
            document.getElementById('storageChart').style.display = 'block';
            document.getElementById('tpsChart').style.display = 'block';
        });
        
        document.getElementById('viewSecurityButton').addEventListener('click', async () => {
            const response = await fetch('/security');
            const data = await response.json();
            document.getElementById('securityData').textContent = JSON.stringify(data, null, 2);
            document.getElementById('securityChart').style.display = 'block';
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'previous_hash': block.previous_hash,
            'hash': block.hash,
            'nonce': block.nonce
        })
    
    return jsonify({
        'chain': chain_data,
        'length': len(chain_data)
    })

@app.route('/mine/<scheme>', methods=['GET'])
def mine(scheme):
    if scheme == 'dilithium':
        wallet = dilithium_wallet
        recipient = binascii.hexlify(dilithium_wallet.public_key).decode()
    else:  # ECDSA
        wallet = ecdsa_wallet
        recipient = binascii.hexlify(ecdsa_wallet.public_key.export_key(format='DER')).decode()
    
    # Create a test transaction
    transaction = wallet.create_transaction(recipient, 0.1)
    blockchain.add_transaction_with_verification(transaction)
    
    # Mine the block
    blockchain.mine_pending_transactions(recipient)
    
    return jsonify({
        'message': f'New Block Forged with {scheme.upper()}',
        'block_index': blockchain.get_latest_block().index,
        'block_hash': blockchain.get_latest_block().hash
    })

@app.route('/metrics/<scheme>', methods=['GET'])
def get_metrics(scheme):
    try:
        with open(f'results/{scheme}_metrics.json', 'r') as f:
            metrics = json.load(f)
        return jsonify(metrics)
    except FileNotFoundError:
        return jsonify({"error": f"No {scheme} metrics available yet. Run a performance test first."})

@app.route('/comparison', methods=['GET'])
def get_comparison():
    try:
        with open('results/comparative_metrics.json', 'r') as f:
            metrics = json.load(f)
        return jsonify(metrics)
    except FileNotFoundError:
        return jsonify({"error": "No comparison metrics available yet. Run the comparative test first."})

@app.route('/security', methods=['GET'])
def get_security():
    try:
        with open('results/quantum_analysis/security_levels.json', 'r') as f:
            security = json.load(f)
        return jsonify(security)
    except FileNotFoundError:
        return jsonify({"error": "No security analysis available yet. Run the quantum security analysis first."})

@app.route('/charts/<path:filename>')
def get_chart(filename):
    return app.send_static_file(f'charts/{filename}')

@app.route('/quantum_analysis/<path:filename>')
def get_security_chart(filename):
    return app.send_static_file(f'quantum_analysis/{filename}')

@app.before_first_request
def setup_static_dirs():
    os.makedirs('static/charts', exist_ok=True)
    os.makedirs('static/quantum_analysis', exist_ok=True)
    
    # Copy charts if they exist
    if os.path.exists('results/charts'):
        for file in os.listdir('results/charts'):
            if file.endswith('.png'):
                import shutil
                shutil.copy(f'results/charts/{file}', f'static/charts/{file}')
    
    # Copy security analysis if it exists
    if os.path.exists('results/quantum_analysis'):
        for file in os.listdir('results/quantum_analysis'):
            if file.endswith('.png'):
                import shutil
                shutil.copy(f'results/quantum_analysis/{file}', f'static/quantum_analysis/{file}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Using port 5001 to avoid conflicts
