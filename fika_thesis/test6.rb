#!/usr/local/bin/ruby
require File.expand_path(File.dirname(__FILE__) + '/vitocha.rb')

$jails='/jails'
op = Operator.new

op.setupserver("test_n1")
op.setupserver("test_n2")
op.setupserver("test_n3")
op.setuprouter("test_r1")
op.setuprouter("test_r2")
op.setuprouter("test_r3")
op.setupbridge("bridge1")
op.setupbridge("bridge2")
op.setupbridge("bridge3")
op.setupbridge("bridge001")
op.setupbridge("bridge002")

######################################
### ISP1 ###
######################################
epaira, epairb = op.createpair
op.connect("test_n1", epaira)
op.connect("bridge1", epairb)
op.assignip("test_n1", epaira, "192.168.1.2", "255.255.255.0")
op.up("test_n1", epaira)
op.up("bridge1", epairb)
op.assigngw("test_n1", "192.168.1.1")

epaira, epairb = op.createpair
op.connect("test_r1", epaira)
op.connect("bridge1", epairb)
op.assignip("test_r1", epaira, "192.168.1.1", "255.255.255.0", "65001")
op.up("test_r1", epaira)
op.up("bridge1", epairb)

# ISP1 -> IX #
epaira, epairb = op.createpair
op.connect("test_r1", epaira)
op.connect("bridge001", epairb)
op.assignip("test_r1", epaira, "172.16.1.1", "255.255.255.0")
op.up("test_r1", epaira)
op.up("bridge001", epairb)
######################################

######################################
### ISP2 ###
######################################
epaira, epairb = op.createpair
op.connect("test_n2", epaira)
op.connect("bridge2", epairb)
op.assignip("test_n2", epaira, "192.168.2.2", "255.255.255.0")
op.up("test_n2", epaira)
op.up("bridge2", epairb)
op.assigngw("test_n2", "192.168.2.1")

epaira, epairb = op.createpair
op.connect("test_r2", epaira)
op.connect("bridge2", epairb)
op.assignip("test_r2", epaira, "192.168.2.1", "255.255.255.0", "65002")
op.up("test_r2", epaira)
op.up("bridge2", epairb)

# ISP2 -> IX #
epaira, epairb = op.createpair
op.connect("test_r2", epaira)
op.connect("bridge001", epairb)
op.assignip("test_r2", epaira, "172.16.1.2", "255.255.255.0")
op.up("test_r2", epaira)
op.up("bridge001", epairb)

epaira, epairb = op.createpair
op.connect("test_r2", epaira)
op.connect("bridge002", epairb)
op.assignip("test_r2", epaira, "172.16.2.1", "255.255.255.0")
op.up("test_r2", epaira)
op.up("bridge002", epairb)
######################################

######################################
### ISP3 ###
######################################
epaira, epairb = op.createpair
op.connect("test_n3", epaira)
op.connect("bridge3", epairb)
op.assignip("test_n3", epaira, "192.168.3.2", "255.255.255.0")
op.up("test_n3", epaira)
op.up("bridge3", epairb)
op.assigngw("test_n3", "192.168.3.1")

epaira, epairb = op.createpair
op.connect("test_r3", epaira)
op.connect("bridge3", epairb)
op.assignip("test_r3", epaira, "192.168.3.1", "255.255.255.0", "65003")
op.up("test_r3", epaira)
op.up("bridge3", epairb)

# ISP -> IX
epaira, epairb = op.createpair
op.connect("test_r3", epaira)
op.connect("bridge002", epairb)
op.assignip("test_r3", epaira, "172.16.2.2", "255.255.255.0")
op.up("test_r3", epaira)
op.up("bridge002", epairb)
######################################

op.start("test_r1", "quagga")
op.start("test_r2", "quagga")
op.start("test_r3", "quagga")
