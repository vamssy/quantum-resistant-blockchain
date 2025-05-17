from blockchain import Blockchain
from crypto_utils import Wallet, CryptoManager
import time
import binascii
import json
import os


def run_performance_test(num_transactions=1000):
    """Run a performance test with the specified number of transactions"""
    print(f"\n=== Running Performance Test with {num_transactions} Transactions ===")
    
    # Create blockchain with lower difficulty for faster testing
    blockchain = Blockchain(difficulty=1)
    
    # Create wallets
    print("Creating wallets...")
    wallet1 = Wallet('dilithium')
    wallet2 = Wallet('dilithium')
    
    # Process transactions
    print(f"Processing {num_transactions} transactions...")
    start_time = time.time()
    
    for i in range(num_transactions):
        if i % 100 == 0:
            print(f"  - Processed {i} transactions...")
        
        # Create a transaction
        transaction = wallet1.create_transaction(
            binascii.hexlify(wallet2.public_key).decode(), 
            0.01  # Small amount for testing
        )
        
        # Add transaction to blockchain
        try:
            blockchain.add_transaction_with_verification(transaction)
            
            # Mine every 10 transactions to keep the blockchain moving
            if i % 10 == 0:
                blockchain.mine_pending_transactions(binascii.hexlify(wallet1.public_key).decode())
        except Exception as e:
            print(f"Error processing transaction {i}: {e}")
    
    # Mine any remaining transactions
    blockchain.mine_pending_transactions(binascii.hexlify(wallet1.public_key).decode())
    
    total_time = time.time() - start_time
    
    # Save metrics
    metrics = wallet1.crypto_manager.save_metrics('dilithium')
    
    # Add blockchain metrics
    metrics.update({
        'total_processing_time_seconds': total_time,
        'transactions_per_second': num_transactions / total_time,
        'blockchain_size_blocks': len(blockchain.chain),
        'average_transactions_per_block': sum(len(block.transactions) for block in blockchain.chain) / len(blockchain.chain)
    })
    
    # Save updated metrics
    with open('results/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
    
    # Print summary
    print("\n=== Performance Test Results ===")
    print(f"Total transactions processed: {num_transactions}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Transactions per second: {num_transactions / total_time:.2f}")
    print(f"Average signature size: {metrics['avg_signature_size_bytes']:.2f} bytes")
    print(f"Total signature storage: {metrics['total_signature_storage_mb']:.2f} MB")
    print(f"Average verification time: {metrics['avg_verification_time_ms']:.2f} ms")
    print(f"Blockchain size: {len(blockchain.chain)} blocks")
    
    return metrics


if __name__ == "__main__":
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Run the performance test with 1,000 transactions
    metrics = run_performance_test(1000)
    
    print("\nTest completed. Results saved to results/metrics.json")
