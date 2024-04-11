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

    net.build()
    net.start()

    # Configurar rutas estáticas en el router si es necesario
    rc.cmd('route add default gw 192.168.100.6 router-eth0')
    rc.cmd('route add default gw 192.168.100.14 router-eth1')

    r1.cmd('route add default gw 10.0.1.1 router-eth0')
    r1.cmd('route add default gw 192.168.100.1 router-eth1')

    h1.cmd('route add default gw 10.0.1.1')
    h2.cmd('route add default gw 10.0.1.1')

    # Enrutamiento entre las redes
    rc.cmd('ip route add 10.0.1.0/24 via 192.168.100.1 dev router-eth0')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    create_topology()