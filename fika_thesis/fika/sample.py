from fika import Operator
import subprocess
import start_node

global jails
jails = "/jails"

op = Operator()

op.setupnode("n1")
op.setupnode("n2")
op.setupnode("n3")
op.setupnode("n4")
op.setupnode("n5")
op.setupnode("n6")
op.setupnode("n7")
op.setupnode("n8")
op.setupnode("n9")
op.setupnode("n10")
op.setuprouter("r1")
op.setuprouter("r2")
op.setuprouter("r3")
op.setuprouter("r4")
op.setuprouter("r5")
op.setuprouter("r6")
op.setuprouter("r7")
op.setuprouter("r8")
op.setupbridge("bridge1")
op.setupbridge("bridge2")
op.setupbridge("bridge3")
op.setupbridge("bridge4")
op.setupbridge("bridge5")
op.setupbridge("bridge001")
op.setupbridge("bridge002")
op.setupbridge("bridge003")
op.setupbridge("bridge004")
op.setupbridge("bridge005")
op.setupbridge("bridge006")
op.setupbridge("bridge007")
op.setupbridge("bridge008")
op.setupbridge("bridge009")
op.setupbridge("bridge010")
op.setupbridge("bridge011")

######################################
### ISP1 ###
######################################
epaira, epairb = op.createpair()
op.connect("n1", epaira)
op.connect("bridge1", epairb)
op.assignip("n1", epaira, "192.168.1.2", "255.255.255.0")
op.up("n1", epaira)
op.up("bridge1", epairb)
op.assigngw("n1", "192.168.1.1")

epaira, epairb = op.createpair()
op.connect("n2", epaira)
op.connect("bridge1", epairb)
op.assignip("n2", epaira, "192.168.1.3", "255.255.255.0")
op.up("n2", epaira)
op.up("bridge1", epairb)
op.assigngw("n2", "192.168.1.1")

epaira, epairb = op.createpair()
op.connect("n3", epaira)
op.connect("bridge1", epairb)
op.assignip("n3", epaira, "192.168.1.4", "255.255.255.0")
op.up("n3", epaira)
op.up("bridge1", epairb)
op.assigngw("n3", "192.168.1.1")

epaira, epairb = op.createpair()
op.connect("r1", epaira)
op.connect("bridge1", epairb)
op.assignip("r1", epaira, "192.168.1.1", "255.255.255.0", "65001")
op.up("r1", epaira)
op.up("bridge1", epairb)

# ISP1 -> IX #
epaira, epairb = op.createpair()
op.connect("r1", epaira)
op.connect("bridge001", epairb)
op.assignip("r1", epaira, "172.1.1.0", "255.255.0.0")
op.up("r1", epaira)
op.up("bridge001", epairb)

epaira, epairb = op.createpair()
op.connect("r1", epaira)
op.connect("bridge002", epairb)
op.assignip("r1", epaira, "172.2.1.0", "255.255.0.0")
op.up("r1", epaira)
op.up("bridge002", epairb)

epaira, epairb = op.createpair()
op.connect("r1", epaira)
op.connect("bridge003", epairb)
op.assignip("r1", epaira, "172.3.1.0", "255.255.0.0")
op.up("r1", epaira)
op.up("bridge003", epairb)
######################################

######################################
### ISP2 ###
######################################
epaira, epairb = op.createpair()
op.connect("n4", epaira)
op.connect("bridge2", epairb)
op.assignip("n4", epaira, "192.168.2.2", "255.255.255.0")
op.up("n4", epaira)
op.up("bridge2", epairb)
op.assigngw("n4", "192.168.2.1")

epaira, epairb = op.createpair()
op.connect("n5", epaira)
op.connect("bridge2", epairb)
op.assignip("n5", epaira, "192.168.2.3", "255.255.255.0")
op.up("n5", epaira)
op.up("bridge2", epairb)
op.assigngw("n5", "192.168.2.1")

epaira, epairb = op.createpair()
op.connect("r2", epaira)
op.connect("bridge2", epairb)
op.assignip("r2", epaira, "192.168.2.1", "255.255.255.0", "65002")
op.up("r2", epaira)
op.up("bridge2", epairb)

# ISP1 -> IX #
epaira, epairb = op.createpair()
op.connect("r2", epaira)
op.connect("bridge001", epairb)
op.assignip("r2", epaira, "172.1.2.0", "255.255.0.0")
op.up("r2", epaira)
op.up("bridge001", epairb)

epaira, epairb = op.createpair()
op.connect("r2", epaira)
op.connect("bridge004", epairb)
op.assignip("r2", epaira, "172.4.1.0", "255.255.0.0")
op.up("r2", epaira)
op.up("bridge004", epairb)

epaira, epairb = op.createpair()
op.connect("r2", epaira)
op.connect("bridge005", epairb)
op.assignip("r2", epaira, "172.5.1.0", "255.255.0.0")
op.up("r2", epaira)
op.up("bridge005", epairb)
######################################

######################################
### ISP3 ###
######################################
# ISP -> IX
epaira, epairb = op.createpair()
op.connect("r3", epaira)
op.connect("bridge003", epairb)
op.assignip("r3", epaira, "172.3.2.0", "255.255.0.0")
op.up("r3", epaira)
op.up("bridge003", epairb)

epaira, epairb = op.createpair()
op.connect("r3", epaira)
op.connect("bridge006", epairb)
op.assignip("r3", epaira, "172.6.1.0", "255.255.0.0")
op.up("r3", epaira)
op.up("bridge006", epairb)
######################################

######################################
### ISP4 ###
######################################
# ISP -> IX
epaira, epairb = op.createpair()
op.connect("r4", epaira)
op.connect("bridge002", epairb)
op.assignip("r4", epaira, "172.2.2.0", "255.255.0.0")
op.up("r4", epaira)
op.up("bridge002", epairb)

epaira, epairb = op.createpair()
op.connect("r4", epaira)
op.connect("bridge004", epairb)
op.assignip("r4", epaira, "172.4.2.0", "255.255.0.0")
op.up("r4", epaira)
op.up("bridge004", epairb)

epaira, epairb = op.createpair()
op.connect("r4", epaira)
op.connect("bridge007", epairb)
op.assignip("r4", epaira, "172.7.1.0", "255.255.0.0")
op.up("r4", epaira)
op.up("bridge007", epairb)

epaira, epairb = op.createpair()
op.connect("r4", epaira)
op.connect("bridge008", epairb)
op.assignip("r4", epaira, "172.8.1.0", "255.255.0.0")
op.up("r4", epaira)
op.up("bridge008", epairb)

epaira, epairb = op.createpair()
op.connect("r4", epaira)
op.connect("bridge009", epairb)
op.assignip("r4", epaira, "172.9.1.0", "255.255.0.0")
op.up("r4", epaira)
op.up("bridge009", epairb)
######################################

######################################
### ISP5 ###
######################################
# ISP -> IX
epaira, epairb = op.createpair()
op.connect("r5", epaira)
op.connect("bridge005", epairb)
op.assignip("r5", epaira, "172.5.2.0", "255.255.0.0")
op.up("r5", epaira)
op.up("bridge005", epairb)

epaira, epairb = op.createpair()
op.connect("r5", epaira)
op.connect("bridge010", epairb)
op.assignip("r5", epaira, "172.10.1.0", "255.255.0.0")
op.up("r5", epaira)
op.up("bridge010", epairb)
######################################


######################################
### ISP6 ###
######################################
epaira, epairb = op.createpair()
op.connect("n6", epaira)
op.connect("bridge3", epairb)
op.assignip("n6", epaira, "192.168.6.2", "255.255.255.0")
op.up("n6", epaira)
op.up("bridge3", epairb)
op.assigngw("n6", "192.168.6.1")

epaira, epairb = op.createpair()
op.connect("n7", epaira)
op.connect("bridge3", epairb)
op.assignip("n7", epaira, "192.168.6.3", "255.255.255.0")
op.up("n7", epaira)
op.up("bridge3", epairb)
op.assigngw("n7", "192.168.6.1")

epaira, epairb = op.createpair()
op.connect("r6", epaira)
op.connect("bridge3", epairb)
op.assignip("r6", epaira, "192.168.6.1", "255.255.255.0", "65006")
op.up("r6", epaira)
op.up("bridge3", epairb)

# ISP -> IX
epaira, epairb = op.createpair()
op.connect("r6", epaira)
op.connect("bridge006", epairb)
op.assignip("r6", epaira, "172.6.2.0", "255.255.0.0")
op.up("r6", epaira)
op.up("bridge006", epairb)

epaira, epairb = op.createpair()
op.connect("r6", epaira)
op.connect("bridge007", epairb)
op.assignip("r6", epaira, "172.7.2.0", "255.255.0.0")
op.up("r6", epaira)
op.up("bridge007", epairb)
######################################

######################################
### ISP7 ###
######################################
epaira, epairb = op.createpair()
op.connect("n8", epaira)
op.connect("bridge4", epairb)
op.assignip("n8", epaira, "192.168.7.2", "255.255.255.0")
op.up("n8", epaira)
op.up("bridge4", epairb)
op.assigngw("n8", "192.168.7.1")

epaira, epairb = op.createpair()
op.connect("n9", epaira)
op.connect("bridge4", epairb)
op.assignip("n9", epaira, "192.168.7.3", "255.255.255.0")
op.up("n9", epaira)
op.up("bridge4", epairb)
op.assigngw("n9", "192.168.7.1")

epaira, epairb = op.createpair()
op.connect("r7", epaira)
op.connect("bridge4", epairb)
op.assignip("r7", epaira, "192.168.7.1", "255.255.255.0")
op.up("r7", epaira)
op.up("bridge4", epairb)

# ISP -> IX
epaira, epairb = op.createpair()
op.connect("r7", epaira)
op.connect("bridge008", epairb)
op.assignip("r7", epaira, "172.8.2.0", "255.255.0.0")
op.up("r7", epaira)
op.up("bridge008", epairb)

epaira, epairb = op.createpair()
op.connect("r7", epaira)
op.connect("bridge011", epairb)
op.assignip("r7", epaira, "172.11.1.0", "255.255.0.0")
op.up("r7", epaira)
op.up("bridge011", epairb)
######################################

######################################
### ISP8 ###
######################################
epaira, epairb = op.createpair()
op.connect("n10", epaira)
op.connect("bridge5", epairb)
op.assignip("n10", epaira, "192.168.8.2", "255.255.255.0")
op.up("n10", epaira)
op.up("bridge5", epairb)
op.assigngw("n10", "192.168.8.1")

epaira, epairb = op.createpair()
op.connect("r8", epaira)
op.connect("bridge5", epairb)
op.assignip("r8", epaira, "192.168.8.1", "255.255.255.0")
op.up("r8", epaira)
op.up("bridge5", epairb)

# ISP -> IX
epaira, epairb = op.createpair()
op.connect("r8", epaira)
op.connect("bridge009", epairb)
op.assignip("r8", epaira, "172.9.2.0", "255.255.0.0")
op.up("r8", epaira)
op.up("bridge009", epairb)

epaira, epairb = op.createpair()
op.connect("r8", epaira)
op.connect("bridge010", epairb)
op.assignip("r8", epaira, "172.10.2.0", "255.255.0.0")
op.up("r8", epaira)
op.up("bridge010", epairb)

epaira, epairb = op.createpair()
op.connect("r8", epaira)
op.connect("bridge011", epairb)
op.assignip("r8", epaira, "172.11.2.0", "255.255.0.0")
op.up("r8", epaira)
op.up("bridge011", epairb)
######################################

op.start("r1", "quagga")
op.start("r2", "quagga")
op.start("r3", "quagga")
op.start("r4", "quagga")
op.start("r5", "quagga")
op.start("r6", "quagga")
op.start("r7", "quagga")
op.start("r8", "quagga")

start_node.main()
