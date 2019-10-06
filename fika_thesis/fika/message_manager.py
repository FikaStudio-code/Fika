import json
# Message Form (default)->
# {
#   "from": STRING,
#   "msg_type": STRING,
#   "payload": JSON(default = None),
# }
#

MSG_BLOCK = "BLOCK"
MSG_CHAIN = "CHAIN"
MSG_RSP_CHAIN = "RSP_CHAIN"
MSG_TEST = "TEST"
cmd_list = [MSG_BLOCK, MSG_CHAIN, MSG_TEST, MSG_RSP_CHAIN]

class MessageManager:
    def __init__(self):
        pass

    def build(self, sender, msg_type, payload):
        message = {
            "from": sender,
            "msg_type": msg_type,
            "payload": payload,
        }
        return json.dumps(message, sort_keys = True, indent = 4)

    def parse(self, conn):
        data_sum = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_sum += data.decode()
        with open("/fika/output/log.txt", "a") as f:
            f.write("\n===== Data =====\n{0}\n===== END =====".format(data_sum))
        dict_data = json.loads(data_sum)
        if dict_data["msg_type"] in cmd_list:
            return ("OK", dict_data["from"], dict_data["msg_type"], dict_data["payload"])
        else:
            return ("NO", "", "", "")
