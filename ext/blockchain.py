import hashlib
import datetime
import random
import joblib as jb


class Clients:
    def __init__(self):
        admin = Client( "admin", 1915, "Cryptographic bot" )
        self.clients = [ admin ]

    def load_clients(self, clients):
        self.clients = clients
        return self

    def add(self, client ):
        for i in self.clients:
            if ( i.pub_key == client.pub_key ):
                return False, "user already exists"
            if (i.priv_key == client.priv_key ):
                return False, "user already exists"
        self.clients.append(client)
        jb.dump( self.clients, "db/clientchain" )
        return True
    def exists( self, pub ):
        for i in self.clients:
            if ( i.pub_key == pub ):
                return True
        return False
    def is_admin(self, pub, priv):

        if ( pub == self.clients[0].pub_key ):
            if ( priv == self.clients[0].priv_key ):
                return True
        return False


class Client:
    def __init__(self, pub, priv, name):
        self.priv_key = priv
        self.pub_key = pub
        self.name = name


class Block:
    def __init__(self, prev, pub_key, priv_key, transaction, stamp = datetime.datetime.now()):
        self.prev = prev
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.transaction = transaction
        self.stamp = stamp
        self.hash = self.fetch_hash()
    
    def fetch_hash(self):
        val = "%s-%s-%s-%s" % (self.prev.hash, self.pub_key, self.priv_key, self.stamp)
        val = hashlib.sha256( val.encode() ).hexdigest().encode()
        return hashlib.sha256( val ).hexdigest()


class Genesis(Block):
    def __init__(self):
        self.stamp = datetime.datetime.now()
        self.hash = self.fetch_hash()
    def fetch_hash(self):
        val = "0x0-%s" % (self.stamp)
        val = hashlib.sha256( val.encode() ).hexdigest().encode()
        return hashlib.sha256( val ).hexdigest()

class Transaction:
    def __init__(self, type, amount = 0, recv = "anonymous"):
        self.type = type
        self.amount = amount
        self.recv = recv


class BlockChain:
    def __init__(self):
        self.genesis = Genesis()
        self.chain = [self.genesis]
    
    def load_chain(self, chain):
        self.chain = chain
        return self

    def mine(self, block):
        # adds a block to the block chain

        # makes sure the block is legal
        if ( ( self.check_prev( block.prev ) == True ) and ( self.auth( block ) == True ) ):

            if ( block.transaction.type == 'transfer' ):

                if not ( clients.exists( block.transaction.recv ) ):
                    
                    return False, "Reciever does not exists"

                if ( self.amount( block.pub_key, block.priv_key ) < block.transaction.amount ):
                    return False, "Insufficient funds"
            
            # difficulty
            diff = random.randint(9000000, 10000000)
            # proof of work and pow validation
            self.proof_of_work(diff)
            del diff
            # adding the block
            self.chain.append( block )
            return True, "successful"

        jb.dump( self.chain, "db/blockchain" )
        return False, ""

    def proof_of_work(self, diff):
        nonce = 0
        while nonce < diff:
            nonce += 1
        return True
    
    def auth(self, block):
        # authenticate user with public and private keys
        x = False
        for client in clients.clients:
            if ( block.pub_key == client.pub_key ):
                if ( block.priv_key == client.priv_key ):
                    x = True
            else:
                continue
        return x

    def check_prev(self, prev):
        return True if prev.hash == self.chain[-1].hash else False
    
    def amount( self, pub, priv ):
        if ( clients.is_admin( pub, priv ) ):
            return float("inf")
        total = 0
        for block in self.chain[1:]:
            # authenticate public key
            if ( block.pub_key == pub ):
                # check if private key is correct
                if ( block.priv_key == priv ):
                    if ( block.transaction.type  == 'transfer' ):
                        total -= float( block.transaction.amount )
                else:
                    continue
            else:
                if ( block.transaction.type == 'transfer' ):
                    if ( block.transaction.recv == pub ):
                        total += float( block.transaction.amount )
                else:
                    continue
        return total

def load_chain():
    try:
        blocks = jb.load("db/blockchain")
        blockchain = BlockChain().load_chain()
    except:
        blockchain = BlockChain()
    return blockchain

def load_clients():
    try:
        clients = jb.load("db/clientchain")
        clients = Clients().load_clients( clients )
    except:
        clients = Clients()
    return clients
