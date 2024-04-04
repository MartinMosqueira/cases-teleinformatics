from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Host, OVSKernelSwitch, Node
from mininet.topo import Topo
from mininet.log import setLogLevel, info

class CustomSwitch(OVSKernelSwitch):
    OVSVersion = '2.17.9'

class CustomTopology(Topo):
    def build(self):
        info('*** Add switches\n')
        s1 = self.addSwitch('s1', cls=CustomSwitch, failMode='standalone')

        info('*** Add hosts\n')
        h1 = self.addHost('h1', cls=Host, ip='10.0.1.2/24', defaultRoute='via 10.0.1.1')
        h2 = self.addHost('h2', cls=Host, ip='10.0.1.254/24', defaultRoute='via 10.0.1.1')

        info('*** Add router\n')
        r1 = self.addHost('r1', cls=Node, ip='10.0.1.1/24')
        r1_wan = self.addHost('r1_wan', cls=Node, ip='192.168.100.1/29')



        info('*** Add links switch\n')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(r1, s1, intfName1='r1-eth0', params1={'ip': '10.0.1.1/24'})
        r1.cmd('sysctl -w net.ipv4.ip_forward=1')


def myNetwork():
    topo = CustomTopology()
    net = Mininet(topo=topo, controller=None)
    net.start()

    
    
    r1 = net.get('r1')
    r1.cmd('ip route add 10.0.1.0/24 via 192.168.100.1 dev r1-eth0')

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
