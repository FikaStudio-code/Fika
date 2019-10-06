#!/usr/local/bin/ruby
require File.expand_path(File.dirname(__FILE__) + '/vitocha.rb')

$jails='/jails'
op = Operator.new

op.setupserver("s1")
op.setupserver("s2")
op.setupserver("s3")
op.setupserver("s6")
op.setupserver("s7")
op.setuprouter("r1")
op.setuprouter("r112")
op.setuprouter("r113")
op.setuprouter("r3")
op.setuprouter("r332")
op.setuprouter("r6")
op.setuprouter("r662")
op.setupbridge("bridge1")
op.setupbridge("bridge2")
op.setupbridge("bridge3")
op.setupbridge("bridge002")
op.setupbridge("bridge003")
op.setupbridge("bridge006")

### ISP1 ###
epaira, epairb = op.createpair
op.connect("s1", epaira)
op.connect("bridge1", epairb)
op.assignip("s1", epaira, "192.168.1.2", "255.255.255.0")
op.up("s1", epaira)
op.up("bridge1", epairb)
op.assigngw("s1", "192.168.1.101")

epaira, epairb = op.createpair
op.connect("s2", epaira)
op.connect("bridge1", epairb)
op.assignip("s2", epaira, "192.168.1.3", "255.255.255.0")
op.up("s2", epaira)
op.up("bridge1", epairb)
op.assigngw("s2", "192.168.1.101")

epaira, epairb = op.createpair
op.connect("s3", epaira)
op.connect("bridge1", epairb)
op.assignip("s3", epaira, "192.168.1.4", "255.255.255.0")
op.up("s3", epaira)
op.up("bridge1", epairb)
op.assigngw("s3", "192.168.1.101")

epaira, epairb = op.createpair
op.connect("r1", epaira)
op.connect("bridge1", epairb)
op.assignip("r1", epaira, "192.168.1.101", "255.255.255.0", "65001")
op.up("r1", epaira)
op.up("bridge1", epairb)

epaira, epairb = op.createpair
op.connect("r112", epaira)
op.connect("bridge1", epairb)
op.assignip("r112", epaira, "192.168.1.102", "255.255.255.0", "65001")
op.up("r112", epaira)
op.up("bridge1", epairb)

epaira, epairb = op.createpair
op.connect("r113", epaira)
op.connect("bridge1", epairb)
op.assignip("r113", epaira, "192.168.1.103", "255.255.255.0", "65001")
op.up("r113", epaira)
op.up("bridge1", epairb)

# ISP1 -> IX #
epaira, epairb = op.createpair
op.connect("r112", epaira)
op.connect("bridge002", epairb)
op.assignip("r112", epaira, "172.16.1.2", "255.255.0.0")
op.up("r112", epaira)
op.up("bridge002", epairb)

epaira, epairb = op.createpair
op.connect("r113", epaira)
op.connect("bridge003", epairb)
op.assignip("r113", epaira, "172.16.1.3", "255.255.0.0")
op.up("r113", epaira)
op.up("bridge003", epairb)

### ISP3 ###
epaira, epairb = op.createpair
op.connect("r3", epaira)
op.connect("bridge2", epairb)
op.assignip("r3", epaira, "192.168.3.101", "255.255.255.0", "65003")
op.up("r3", epaira)
op.up("bridge2", epairb)

epaira, epairb = op.createpair
op.connect("r332", epaira)
op.connect("bridge2", epairb)
op.assignip("r332", epaira, "192.168.3.102", "255.255.255.0", "65003")
op.up("r332", epaira)
op.up("bridge2", epairb)

# ISP -> IX
epaira, epairb = op.createpair
op.connect("r3", epaira)
op.connect("bridge003", epairb)
op.assignip("r3", epaira, "172.16.3.1", "255.255.0.0")
op.up("r3", epaira)
op.up("bridge003", epairb)

epaira, epairb = op.createpair
op.connect("r332", epaira)
op.connect("bridge006", epairb)
op.assignip("r332", epaira, "172.16.3.2", "255.255.0.0")
op.up("r332", epaira)
op.up("bridge006", epairb)

### ISP6 ###
epaira, epairb = op.createpair
op.connect("s6", epaira)
op.connect("bridge3", epairb)
op.assignip("s6", epaira, "192.168.6.2", "255.255.255.0")
op.up("s6", epaira)
op.up("bridge3", epairb)
op.assigngw("s6", "192.168.6.101")

epaira, epairb = op.createpair
op.connect("s7", epaira)
op.connect("bridge3", epairb)
op.assignip("s7", epaira, "192.168.6.3", "255.255.255.0")
op.up("s7", epaira)
op.up("bridge3", epairb)
op.assigngw("s7", "192.168.6.101")

epaira, epairb = op.createpair
op.connect("r6", epaira)
op.connect("bridge3", epairb)
op.assignip("r6", epaira, "192.168.6.101", "255.255.255.0", "65006")
op.up("r6", epaira)
op.up("bridge3", epairb)

epaira, epairb = op.createpair
op.connect("r662", epaira)
op.connect("bridge3", epairb)
op.assignip("r662", epaira, "192.168.6.102", "255.255.0.0", "65006")
op.up("r662", epaira)
op.up("bridge3", epairb)

# ISP -> IX
epaira, epairb = op.createpair
op.connect("r6", epaira)
op.connect("bridge006", epairb)
op.assignip("r6", epaira, "172.16.6.1", "255.255.0.0")
op.up("r6", epaira)
op.up("bridge006", epairb)


op.start("r1", "quagga")
op.start("r112", "quagga")
op.start("r113", "quagga")
op.start("r3", "quagga")
op.start("r332", "quagga")
op.start("r6", "quagga")
op.start("r662", "quagga")
