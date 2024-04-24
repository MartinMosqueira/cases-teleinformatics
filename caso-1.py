from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.node import Node, Host

class CustomSwitch(OVSKernelSwitch):
    OVSVersion = '2.17.9'

def create_topology():
    net = Mininet(controller=RemoteController)

    # Agregar switch
    s1 = net.addSwitch('s1', cls=CustomSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=CustomSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=CustomSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=CustomSwitch, failMode='standalone')    

    # Agregar nodos
    rc = net.addHost('rc', cls=Node, ip='192.168.100.6')
    r1 = net.addHost('r1', cls=Node, ip='192.168.100.1')
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.9')

    h1 = net.addHost('h1', cls=Host, ip='10.0.1.2/24')
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.254/24')
    h3 = net.addHost('h3', cls=Host, ip='10.0.2.2/24')
    h4 = net.addHost('h4', cls=Host, ip='10.0.2.254/24')

    # Agregar enlaces

    # ROUTER CENTRAL
    net.addLink(rc, s1, intfName1='rcs1-eth0', params1={'ip': '192.168.100.6/29'})
    net.addLink(rc, s2, intfName1='rcs2-eth0', params1={'ip': '192.168.100.14/29'})

    # ROUTER SUCURSAL 1
    net.addLink(r1, s1, intfName1='r1s1-eth0', params1={'ip': '192.168.100.1/29'})
    net.addLink(r1, s3, intfName1='r1s3-eth0', params1={'ip': '10.0.1.1/24'})

    # ROUTER SUCURSAL 2
    net.addLink(r2, s2, intfName1='r2s2-eth0', params1={'ip': '192.168.100.9/29'})
    net.addLink(r2, s4, intfName1='r2s4-eth0', params1={'ip': '10.0.2.1/24'})

    # HOSTS
    net.addLink(h1, s3, intfName1='h1s3-eth0', params1={'ip': '10.0.1.2/24'})
    net.addLink(h2, s3, intfName1='h2s3-eth0', params1={'ip': '10.0.1.254/24'})

    net.addLink(h3, s4, intfName1='h3s4-eth0', params1={'ip': '10.0.2.2/24'})
    net.addLink(h4, s4, intfName1='h4s4-eth0', params1={'ip': '10.0.2.254/24'})

    net.build()
    net.start()

    # Enrutamiento entre las redes
    # ROTER CENTRAL
    rc.cmd('ip route add 10.0.1.0/24 via 192.168.100.1 dev rcs1-eth0')
    rc.cmd('ip route add 10.0.2.0/24 via 192.168.100.9 dev rcs2-eth0')

    # ROTER SUCURSAL 1
    r1.cmd('ip route add 10.0.2.0/24 via 192.168.100.6 dev r1s1-eth0')
    r1.cmd('ip route add 192.168.100.8/29 via 192.168.100.6 dev r1s1-eth0')
    
    # ROTER SUCURSAL 2
    r2.cmd('ip route add 10.0.1.0/24 via 192.168.100.14 dev r2s2-eth0')
    r2.cmd('ip route add 192.168.100.0/29 via 192.168.100.14 dev r2s2-eth0')

    # HOSTS
    h1.cmd('ip route add 192.168.100.0/29 via 10.0.1.1 dev h1s3-eth0')
    h1.cmd('ip route add 192.168.100.8/29 via 10.0.1.1 dev h1s3-eth0')
    h1.cmd('ip route add 10.0.2.0/24 via 10.0.1.1 dev h1s3-eth0')

    h2.cmd('ip route add 192.168.100.0/29 via 10.0.1.1 dev h2s3-eth0')
    h2.cmd('ip route add 192.168.100.8/29 via 10.0.1.1 dev h2s3-eth0')
    h2.cmd('ip route add 10.0.2.0/24 via 10.0.1.1 dev h2s3-eth0')

    h3.cmd('ip route add 192.168.100.0/29 via 10.0.2.1 dev h3s4-eth0')
    h3.cmd('ip route add 192.168.100.8/29 via 10.0.2.1 dev h3s4-eth0')
    h3.cmd('ip route add 10.0.1.0/24 via 10.0.2.1 dev h3s4-eth0')

    h4.cmd('ip route add 192.168.100.0/29 via 10.0.2.1 dev h4s4-eth0')
    h4.cmd('ip route add 192.168.100.8/29 via 10.0.2.1 dev h4s4-eth0')
    h4.cmd('ip route add 10.0.1.0/24 via 10.0.2.1 dev h4s4-eth0')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    create_topology()