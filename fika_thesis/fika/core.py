import sys
import signal
import socket
import json
import threading
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from message_manager import MessageManager
from blockchain.blockchain_manager import BlockchainManager
from blockchain.block_miner import BlockMiner

MSG_BLOCK = "BLOCK"
MSG_CHAIN = "CHAIN"
MSG_RSP_CHAIN = "RSP_CHAIN"
MSG_TEST = "TEST"

MINING_INTERVAL = 10

class NodeCore:
    def __init__(self):
        self.name = sys.argv[-1]
        self.make_table()
        self.port = 11111
        with open("/fika/output/log.txt", "w") as f:
            f.write("Hello")
        self.lock = threading.Lock()
        self.mm = MessageManager()
        self.bm = BlockchainManager()
        self.miner = BlockMiner()
        genesis_block = self.miner.mine_gblock()
        self.bm.chained(genesis_block)
        self.previous_hash = self.bm.get_hash(genesis_block)

        self.MINING_NOW = False
        self.STOP_MINING = False
        signal.signal(signal.SIGINT, self.__KeyboardInterruptHandler)
        self.wait_thread = threading.Thread(target = self.__wait_access)
        self.wait_thread.start()
        self.mining_timer = threading.Timer(MINING_INTERVAL, self.__start_mining)
        self.mining_timer.start()

    def make_table(self):
        with open("/fika/ip_info.txt", "r") as f:
            info = json.loads(f.read())
        with open("/fika/logicnet_info.txt", "r") as f:
            my_info = json.loads(f.read())
        self.peer = dict()
        self.ip = info[self.name]
        my_info = my_info[self.name]
        for i in my_info:
            self.peer[i] = info[i]


    def __wait_access(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(0)

        executor = ThreadPoolExecutor(max_workers = 10)

        while True:
            conn, addr = s.accept()
            executor.submit(self.__handle_message, conn)

    def __start_mining(self):
        while self.STOP_MINING is not True:
            self.MINING_NOW = True
            with open("/fika/output/log.txt", "a") as f:
                f.write("\nMining start!!!")
            self.MINING_NOW = True
            length = self.bm.get_length() + 1
            block = self.miner.mine_block(length, self.previous_hash)
            if (block["previous_hash"] != self.previous_hash) or (block["height"] != self.bm.get_length() + 1):
                with open("/fika/output/log.txt", "a") as f:
                    f.write("\nOops! I might have lost mining competition")
                break
            self.bm.chained(block)
            self.previous_hash = self.bm.get_hash(block)
            message = self.mm.build(self.ip, MSG_BLOCK, block)
            self.broadcast(message, self.ip)
            self.STOP_MINING = True
        self.STOP_MINING = False
        self.MINING_NOW = False
        self.mining_timer = threading.Timer(MINING_INTERVAL, self.__start_mining)
        self.mining_timer.start()

    def broadcast(self, message, sender):
        for ip in self.peer.values():
            if (ip != self.ip and ip != sender):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, 11111))
                    s.sendall(message.encode())
                    s.close()
                except:
                    with open("/fika/output/log.txt", "a") as f:
                        f.write("\nConnection failed...")
            else:
                continue

    def __handle_message(self, conn):
        result, sender, msg_type, payload = self.mm.parse(conn)
        if result == "OK":
            if msg_type == MSG_TEST:
                self.broadcast(message, sender)

            elif msg_type == MSG_BLOCK:
                result, result2 = self.bm.verify_block(self.previous_hash, payload)
                if result is True:
                    if MINING_NOW:
                        STOP_MINING = True
                    self.bm.chained(payload)
                    self.previous_hash = self.bm.get_hash(payload)
                    with open("/fika/output/log.txt", "a") as f:
                        f.write("\nprevious_hash is changed...{0}".format(self.previous_hash))
                    self.mining_timer = threading.Timer(MINING_INTERVAL, self.__start_mining)
                    self.mining_timer.start()

                    message = self.mm.build(self.ip, MSG_BLOCK, payload)
                    self.broadcast(message, sender)
                else:
                    if result2 == 1:
                        message = self.mm.build(self.ip, MSG_CHAIN, None)
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((sender, 11111))
                        s.sendall(message.encode())
                        s.close()

            elif msg_type == MSG_CHAIN:
                chain = self.bm.get_mychain()
                message = self.mm.build(self.ip, MSG_RSP_CHAIN, chain)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((sender, 11111))
                s.sendall(message.encode())
                s.close()

            elif msg_type == MSG_RSP_CHAIN:
                with self.lock:
                    result = self.bm.verify_chain(payload)
                    if result:
                        last_block = self.bm.get_lastblock()
                        self.previous_hash = self.bm.get_hash(last_block)
                    else:
                        with open("/fika/output/log.txt", "a") as f:
                            f.write("\nReceived Blockchain is useless")
        else:
            with open("/fika/output/log.txt", "a") as f:
                f.write("\nERROR")



    def __KeyboardInterruptHandler(self, signal, frame):
        with open("/fika/output/log.txt", "a") as f:
            f.write("\nCtrl+C!!!")
        chain = self.bm.get_mychain()
        with open("/fika/output/blockchain.txt", "w") as f:
            f.write(json.dumps(chain, indent = 4, sort_keys = True))
        sys.exit(0)

if __name__ == "__main__":
    NodeCore()
