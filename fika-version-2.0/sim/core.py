import sys
import signal
import socket
import json
import threading
from time import time, sleep
from concurrent.futures import ThreadPoolExecutor
from message_manager import MessageManager
from concensus_layer.proof_of_work.pow import PoW
from network_layer.broadcast import Broadcast

MSG_BLOCK = "BLOCK"
MSG_CHAIN = "CHAIN"
MSG_RSP_CHAIN = "RSP_CHAIN"
MSG_TEST = "TEST"

STOP_MINING = False
MINING_INTERVAL = 30

class NodeCore:
    def __init__(self):
        global MINING_INTERVAL
        self.name = sys.argv[-1]
        self.NL = Broadcast(self.name)
        self.ip, self.port = self.NL.get_my_info()
        with open("/sim/output/{0}_log.txt".format(self.name), "w") as f:
            f.write("Hello")
        self.lock = threading.Lock()
        self.mm = MessageManager(self.name)
        self.CL = PoW(self.name)
        self.previous_hash = self.CL.mine_gblock()

        signal.signal(signal.SIGINT, self.__KeyboardInterruptHandler)
        self.wait_thread = threading.Thread(target = self.__wait_access)
        self.wait_thread.start()
        self.mining_timer = threading.Timer(MINING_INTERVAL, self.__start_mining)
        self.mining_timer.start()

    def __wait_access(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(0)

        executor = ThreadPoolExecutor(max_workers = 10)

        while True:
            conn, addr = s.accept()
            executor.submit(self.__handle_message, conn)

    def __start_mining(self):
        global STOP_MINING
        global MINING_INTERVAL
        t1 = self.CL.get_time()
        t2 = time()
        t3 = t2 - t1
        if t3 < MINING_INTERVAL:
            sleep(MINING_INTERVAL - t3)
        if STOP_MINING is False:
            result, block = self.CL.start_mining(self.previous_hash)
            if result == 0:
                message = self.mm.build((self.ip, self.port), MSG_BLOCK, block)
                self.NL.broadcast(message, (self.ip, self.port))
        STOP_MINING = False
        self.mining_timer = threading.Timer(MINING_INTERVAL, self.__start_mining)
        self.mining_timer.start()

    def __handle_message(self, conn):
        global MINING_INTERVAL
        global STOP_MINING
        result, sender, msg_type, payload = self.mm.parse(conn)
        if result == "OK":
            if msg_type == MSG_TEST:
                self.NL.broadcast(message, sender)

            elif msg_type == MSG_BLOCK:
                result, result2 = self.CL.verify_block(self.previous_hash, payload)
                if result is True:
                    STOP_MINING = True
                    self.CL.stop_mining()
                    self.CL.chained(payload)
                    self.previous_hash = self.CL.get_hash(payload)
                    with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                        f.write("\nprevious_hash is changed...{0}".format(self.previous_hash))
                    message = self.mm.build((self.ip, self.port), MSG_BLOCK, payload)
                    self.NL.broadcast(message, sender)
                else:
                    if result2 == 1:
                        message = self.mm.build((self.ip, self.port), MSG_CHAIN, None)
                        self.NL.send_message(message, sender)

            elif msg_type == MSG_CHAIN:
                chain = self.CL.get_mychain()
                message = self.mm.build((self.ip, self.port), MSG_RSP_CHAIN, chain)
                self.NL.send_message(message, sender)

            elif msg_type == MSG_RSP_CHAIN:
                with self.lock:
                    result = self.CL.verify_chain(payload)
                    if result:
                        last_block = self.CL.get_lastblock()
                        self.previous_hash = self.CL.get_hash(last_block)
                    else:
                        with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                            f.write("\nReceived Blockchain is useless")
        else:
            with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                f.write("\nERROR")

    def __KeyboardInterruptHandler(self, signal, frame):
        with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
            f.write("\nCtrl+C!!!")
        chain = self.CL.get_mychain()
        with open("/sim/output/{0}_blockchain.txt".format(self.name), "w") as f:
            f.write(json.dumps(chain, indent = 4, sort_keys = True))
        sys.exit(0)

if __name__ == "__main__":
    NodeCore()
