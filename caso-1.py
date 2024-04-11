from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.node import Node

class CustomSwitch(OVSKernelSwitch):
    OVSVersion = '2.17.9'

def create_topology():
    net = Mininet(controller=RemoteController)

    # Agregar controlador
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # SUCURSAL 1

    # Agregar switch
    s1 = net.addSwitch('s1', cls=CustomSwitch, failMode='standalone')    

    # Agregar nodos
    rc = net.addHost('rc', cls=Node, ip=None)
    r1 = net.addHost('r1', cls=Node, ip=None)
    h1 = net.addHost('h1', ip='10.0.1.2/24')
    h2 = net.addHost('h2', ip='10.0.1.254/24')

    # Agregar enlaces
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(r1, s1, intfName1='router-eth0', params={'ip': '10.0.1.1/24'})
    net.addLink(rc, r1, intfName1='router-eth0', intfName2='router-eth1')

    # Configurar las interfaces del router
    rc.cmd('ifconfig router-eth0 192.168.100.6 netmask 255.255.255.248')
    rc.cmd('ifconfig router-eth1 192.168.100.14 netmask 255.255.255.248')

    r1.cmd('ifconfig router-eth0 10.0.1.1 netmask 255.255.255.0')
    r1.cmd('ifconfig router-eth1 192.168.100.1 netmask 255.255.255.248')

    # SUCURSAL 2

    # Agregar switch
    s2 = net.addSwitch('s2', cls=CustomSwitch, failMode='standalone')

    # Agregar nodos
    r2 = net.addHost('r2', cls=Node, ip=None)
    h3 = net.addHost('h3', ip='10.0.2.2/24')
    h4 = net.addHost('h4', ip='10.0.2.254/24')

    # Agregar enlaces
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(r2, s2, intfName1='router-eth0', params={'ip': '10.0.2.1/24'})
    net.addLink(rc, r2, intfName1='router-eth1', intfName2='router-eth1')

    # Configurar las interfaces del router
    r2.cmd('ifconfig router-eth0 10.0.2.1 netmask 255.255.255.0')
    r2.cmd('ifconfig router-eth1 192.168.100.9 netmask 255.255.255.248')

    net.build()
    net.start()

    # Configurar rutas estáticas en el router
    # SUCURSAL 1
    rc.cmd('route add default gw 192.168.100.6 router-eth0')
    rc.cmd('route add default gw 192.168.100.14 router-eth1')

    r1.cmd('route add default gw 10.0.1.1 router-eth0')
    r1.cmd('route add default gw 192.168.100.1 router-eth1')

    h1.cmd('route add default gw 10.0.1.1')
    h2.cmd('route add default gw 10.0.1.1')

    # SUCURSAL 2
    r2.cmd('route add default gw 10.0.2.1 router-eth0')
    r2.cmd('route add default gw 192.168.100.9 router-eth1')

    h3.cmd('route add default gw 10.0.2.1')
    h4.cmd('route add default gw 10.0.2.1')

    # Enrutamiento entre las redes
    rc.cmd('ip route add 10.0.1.0/24 via 192.168.100.1 dev router-eth0')
    rc.cmd('ip route add 10.0.2.0/24 via 192.168.100.9 dev router-eth1')

    r1.cmd('ip route add 10.0.2.0/24 via 192.168.100.6 dev router-eth1')
    r1.cmd('ip route add 192.168.100.8/29 via 192.168.100.6 dev router-eth1')

    r2.cmd('ip route add 10.0.1.0/24 via 192.168.100.14 dev router-eth1')
    r2.cmd('ip route add 192.168.100.0/29 via 192.168.100.14 dev router-eth1')


    CLI(net)
    net.stop()

if __name__ == '__main__':
    create_topology()