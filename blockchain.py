import hashlib
import json
import time
from typing import List, Dict, Any


class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict], 
                 previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
    
    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), [], "0")
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict) -> int:
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1
    
    def mine_pending_transactions(self, mining_reward_address: str) -> None:
        reward_transaction = {
            "sender": "BLOCKCHAIN",
            "recipient": mining_reward_address,
            "amount": 1,  # Mining reward
            "timestamp": time.time()
        }
        self.pending_transactions.append(reward_transaction)
        
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
    
    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def add_transaction_with_verification(self, transaction: Dict) -> int:
        """Add a transaction after verifying its signature"""
        from crypto_utils import CryptoManager
        import binascii
        
        crypto_manager = CryptoManager()
        
        # Extract and convert signature from hex
        signature = binascii.unhexlify(transaction["signature"])
        
        # Make a copy of transaction without signature for verification
        tx_for_verification = transaction.copy()
        del tx_for_verification["signature"]
        
        # Determine signature type (Dilithium or ECDSA)
        signature_type = transaction.get("signature_type", "dilithium")
        
        # Convert sender public key from hex
        if signature_type == "dilithium":
            sender_public_key = binascii.unhexlify(transaction["sender"])
            is_valid = crypto_manager.verify_dilithium_transaction(
                tx_for_verification, signature, sender_public_key
            )
        else:  # ECDSA
            from Crypto.PublicKey import ECC
            sender_public_key = ECC.import_key(binascii.unhexlify(transaction["sender"]))
            is_valid = crypto_manager.verify_ecdsa_transaction(
                tx_for_verification, signature, sender_public_key
            )
        
        if not is_valid:
            raise Exception(f"Invalid {signature_type} transaction signature!")
        
        # Add to pending transactions
        self.pending_transactions.append(transaction)
        return self.get_latest_block().index + 1
