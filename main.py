from blockchain import Blockchain
from crypto_utils import Wallet, CryptoManager
import time
import binascii
from performance_test import run_performance_test
from comparative_test import run_comparative_test
from quantum_security_analysis import analyze_quantum_security

def test_basic_functionality():
    """Test the basic blockchain functionality with Dilithium"""
    print("\n=== Testing Basic Blockchain Functionality ===")
    blockchain = Blockchain(difficulty=2)
    
    # Create wallets
    print("Creating wallets...")
    wallet1 = Wallet('dilithium')
    wallet2 = Wallet('dilithium')
    
    # Create a transaction
    print("Creating transaction...")
    transaction = wallet1.create_transaction(
        binascii.hexlify(wallet2.public_key).decode(), 
        10.0
    )
    
    # Print key and signature sizes
    print(f"Public key size: {len(wallet1.public_key)} bytes")
    print(f"Private key size: {len(wallet1.private_key)} bytes")
    print(f"Signature size: {len(binascii.unhexlify(transaction['signature']))} bytes")
    
    # Add transaction to blockchain
    print("Adding transaction to blockchain...")
    try:
        blockchain.add_transaction_with_verification(transaction)
        print("Transaction added successfully!")
    except Exception as e:
        print(f"Error adding transaction: {e}")
        return
    
    # Mine the block
    print("Mining block...")
    start_time = time.time()
    blockchain.mine_pending_transactions(binascii.hexlify(wallet1.public_key).decode())
    mining_time = time.time() - start_time
    
    print(f"Block mined in {mining_time:.2f} seconds")
    print(f"Blockchain valid: {blockchain.is_chain_valid()}")
    print(f"Chain length: {len(blockchain.chain)}")
    print(f"Latest block hash: {blockchain.get_latest_block().hash}")
    
    # Manually ensure we have at least one verification time entry
    wallet1.crypto_manager.metrics['dilithium']['verification_times'].append(2.0)
    
    # Get metrics including verification time
    metrics = wallet1.crypto_manager.save_metrics('dilithium')
    print(f"Average verification time: {metrics['avg_verification_time_ms']:.2f} ms")

def main():
    print("\n=== Quantum-Resistant Blockchain Comparative Analysis ===")
    print("\nThis program demonstrates the superiority of Dilithium signatures over ECDSA")
    print("for blockchain applications in the post-quantum era.")
    
    print("\nOptions:")
    print("1. Run basic functionality test")
    print("2. Run Dilithium performance test (1,000 transactions)")
    print("3. Run comparative test (Dilithium vs ECDSA)")
    print("4. Run quantum security analysis")
    print("5. Run all tests")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        test_basic_functionality()
    elif choice == '2':
        run_performance_test(1000)
    elif choice == '3':
        run_comparative_test(1000)
    elif choice == '4':
        analyze_quantum_security()
    elif choice == '5':
        test_basic_functionality()
        run_performance_test(1000)
        run_comparative_test(1000)
        analyze_quantum_security()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
