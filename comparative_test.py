from blockchain import Blockchain
from crypto_utils import Wallet, CryptoManager
import time
import binascii
import json
import os
import matplotlib.pyplot as plt
import numpy as np

def run_comparative_test(num_transactions=1000):
    """Run a performance test comparing Dilithium and ECDSA"""
    print(f"\n=== Running Comparative Test with {num_transactions} Transactions ===")
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    os.makedirs('results/charts', exist_ok=True)
    
    # Test both signature schemes
    results = {}
    for scheme in ['ecdsa', 'dilithium']:
        print(f"\nTesting {scheme.upper()} signatures:")
        
        # Create blockchain with lower difficulty for faster testing
        blockchain = Blockchain(difficulty=1)
        
        # Create wallets
        print(f"Creating {scheme} wallets...")
        wallet1 = Wallet(scheme)
        wallet2 = Wallet(scheme)
        
        # Process transactions
        print(f"Processing {num_transactions} transactions with {scheme}...")
        start_time = time.time()
        
        for i in range(num_transactions):
            if i % 100 == 0:
                print(f"  - Processed {i} transactions...")
            
            # Create a transaction
            transaction = wallet1.create_transaction(
                binascii.hexlify(wallet2.public_key).decode() if scheme == 'dilithium' 
                else binascii.hexlify(wallet2.public_key.export_key(format='DER')).decode(), 
                0.01  # Small amount for testing
            )
            
            # Add transaction to blockchain
            try:
                blockchain.add_transaction_with_verification(transaction)
                
                # Mine every 10 transactions
                if i % 10 == 0:
                    blockchain.mine_pending_transactions(
                        binascii.hexlify(wallet1.public_key).decode() if scheme == 'dilithium'
                        else binascii.hexlify(wallet1.public_key.export_key(format='DER')).decode()
                    )
            except Exception as e:
                print(f"Error processing transaction {i}: {e}")
        
        # Mine any remaining transactions
        blockchain.mine_pending_transactions(
            binascii.hexlify(wallet1.public_key).decode() if scheme == 'dilithium'
            else binascii.hexlify(wallet1.public_key.export_key(format='DER')).decode()
        )
        
        total_time = time.time() - start_time
        
        # Save metrics
        metrics = wallet1.crypto_manager.save_metrics(scheme)
        
        # Add blockchain metrics
        metrics.update({
            'total_processing_time_seconds': total_time,
            'transactions_per_second': num_transactions / total_time,
            'blockchain_size_blocks': len(blockchain.chain),
            'average_transactions_per_block': sum(len(block.transactions) for block in blockchain.chain) / len(blockchain.chain)
        })
        
        results[scheme] = metrics
        
        # Print summary
        print(f"\n=== {scheme.upper()} Performance Results ===")
        print(f"Total transactions processed: {num_transactions}")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Transactions per second: {num_transactions / total_time:.2f}")
        print(f"Average signature size: {metrics['avg_signature_size_bytes']:.2f} bytes")
        print(f"Total signature storage: {metrics['total_signature_storage_mb']:.2f} MB")
        print(f"Average verification time: {metrics['avg_verification_time_ms']:.2f} ms")
    
    # Save combined results
    with open('results/comparative_metrics.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    # Generate comparative charts
    generate_comparison_charts(results)
    
    return results

def generate_comparison_charts(results):
    """Generate charts comparing ECDSA and Dilithium performance"""
    # Create charts directory
    os.makedirs('results/charts', exist_ok=True)
    
    # Signature Size Comparison
    plt.figure(figsize=(10, 6))
    sizes = [results['ecdsa']['avg_signature_size_bytes'], results['dilithium']['avg_signature_size_bytes']]
    plt.bar(['ECDSA', 'Dilithium'], sizes)
    plt.title('Signature Size Comparison')
    plt.ylabel('Size (bytes)')
    plt.yscale('log')  # Log scale to show the dramatic difference
    for i, v in enumerate(sizes):
        plt.text(i, v + 5, f"{v:.0f} bytes", ha='center')
    plt.savefig('results/charts/signature_size_comparison.png')
    
    # Verification Time Comparison
    plt.figure(figsize=(10, 6))
    times = [results['ecdsa']['avg_verification_time_ms'], results['dilithium']['avg_verification_time_ms']]
    plt.bar(['ECDSA', 'Dilithium'], times)
    plt.title('Verification Time Comparison')
    plt.ylabel('Time (ms)')
    for i, v in enumerate(times):
        plt.text(i, v + 0.1, f"{v:.2f} ms", ha='center')
    plt.savefig('results/charts/verification_time_comparison.png')
    
    # Storage Requirements for 1,000 Transactions
    plt.figure(figsize=(10, 6))
    storage = [results['ecdsa']['total_signature_storage_mb'], results['dilithium']['total_signature_storage_mb']]
    plt.bar(['ECDSA', 'Dilithium'], storage)
    plt.title('Storage Requirements for 1,000 Transactions')
    plt.ylabel('Storage (MB)')
    for i, v in enumerate(storage):
        plt.text(i, v + 0.1, f"{v:.2f} MB", ha='center')
    plt.savefig('results/charts/storage_comparison.png')
    
    # Transactions Per Second
    plt.figure(figsize=(10, 6))
    tps = [results['ecdsa']['transactions_per_second'], results['dilithium']['transactions_per_second']]
    plt.bar(['ECDSA', 'Dilithium'], tps)
    plt.title('Transactions Per Second')
    plt.ylabel('TPS')
    for i, v in enumerate(tps):
        plt.text(i, v + 1, f"{v:.2f} TPS", ha='center')
    plt.savefig('results/charts/tps_comparison.png')
    
    # Key Size Comparison
    plt.figure(figsize=(10, 6))
    pub_key_sizes = [results['ecdsa']['avg_public_key_size_bytes'], results['dilithium']['avg_public_key_size_bytes']]
    plt.bar(['ECDSA', 'Dilithium'], pub_key_sizes)
    plt.title('Public Key Size Comparison')
    plt.ylabel('Size (bytes)')
    plt.yscale('log')  # Log scale to show the dramatic difference
    for i, v in enumerate(pub_key_sizes):
        plt.text(i, v + 5, f"{v:.0f} bytes", ha='center')
    plt.savefig('results/charts/pubkey_size_comparison.png')
    
    print("Comparison charts generated in results/charts/ directory")

if __name__ == "__main__":
    # Run the comparative test with 1,000 transactions
    results = run_comparative_test(1000)
    
    print("\nTest completed. Results saved to results/comparative_metrics.json")
