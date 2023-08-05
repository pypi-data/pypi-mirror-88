from .Layer import Layer
from .Ospf import Ospf
from .Ibgp import Ibgp
from .Routing import Router
from seedsim.core import Node, Registry, ScopedRegistry, Graphable
from seedsim.core.enums import NetworkType, NodeRole
from typing import List, Tuple, Dict

MplsFileTemplates: Dict[str, str] = {}

MplsFileTemplates['frr_start_script'] = """\
#!/bin/bash
mount -o remount rw /proc/sys 2> /dev/null
echo '1048575' > /proc/sys/net/mpls/platform_labels
while read -r iface; do echo '1' > "/proc/sys/net/mpls/conf/$iface/input"; done < mpls_ifaces.txt
sed -i 's/ldpd=no/ldpd=yes/' /etc/frr/daemons
sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons
service frr start
"""

MplsFileTemplates['frr_config'] = """\
router-id {loopbackAddress}
{ospfInterfaces}
mpls ldp
 address-family ipv4
  discovery transport-address {loopbackAddress}
{ldpInterfaces}
 exit-address-family
router ospf
 redistribute connected
"""

MplsFileTemplates['frr_config_ldp_iface'] = """\
  interface {interface}
"""

# todo: make configurable hello/dead
MplsFileTemplates['frr_config_ospf_iface'] = """\
interface {interface}
 ip ospf area 0
 ip ospf dead-interval minimal hello-multiplier 2
"""

MplsFileTemplates['bird_ibgp_peer'] = '''
    ipv4 {{
        table t_bgp;
        import all;
        export all;
        igp table master4;
    }};
    local {localAddress} as {asn};
    neighbor {peerAddress} as {asn};
'''


class Mpls(Layer, Graphable):
    """!
    @brief The Mpls (MPLS) layer.

    This layer is a replacement for the iBGP full mesh setup for the transit
    provider's internal network. Instead of the traditional IP network, which
    requires every hop to have a copy of the full table, MPLS allows non-edge
    hops to hold only the MPLS forwarding table, which negated the need for the
    full table.

    MPLS layer will setup iBGP, LDP, and OSPF. FRRouting will do LDP and OSPF,
    and BIRD will still do BGP. When installed, the MPLS layer will treat all
    nodes with (1) no connection to IX and (2) no connection to a network with
    at least one host node as non-edge nodes and will not put it as part of the
    iBGP mesh network.
    
    The MPLS layer requires kernel modules support. Make sure you load the
    following modules:

    - mpls_router
    - mpls_iptunnel
    - mpls_gso

    Node with MPLS enabled will be privileged. This means the container
    potentially have full control over the docker host. Be careful when exposing
    the node to the public.
    """

    __reg = Registry()
    __additional_edges: List[Node]
    __enabled: List[int]

    def __init__(self):
        """!
        @brief Mpls layer constructor.
        """
        Graphable.__init__(self)
        self.__additional_edges = []
        self.__enabled = []

        # they are not really "dependency," we just need them to render after
        # us, in case we need to setup masks.
        self.addDependency('Ospf', True, True)
        self.addDependency('Ibgp', True, True)

        self.addDependency('Routing', False, False)

    def getName(self) -> str:
        return 'Mpls'

    def markAsEdge(self, node: Node):
        """!
        @brief Mark a node as edge node.

        By default, only nodes with connection to IX, or connection to a network
        with at least one host node, will be considered an edge router and be
        included in the iBGP mesh. Use this method to mark a node as edge
        manually.

        @param node node
        """
        self.__additional_edges.append(node)

    def enableOn(self, asn: int):
        """!
        @brief Use MPLS in an AS.

        MPLS is not enabled by default. Use this method to enable MPLS for an
        AS. This also automatically setup masks for OSPF and IBGP layer if they
        exist.

        @param asn ASN.
        """
        self.__enabled.append(asn)

    def __getEdgeNodes(self, scope: ScopedRegistry) -> Tuple[List[Node], List[Node]]:
        """!
        @brief Helper tool - get list of routers (edge, non-edge) of an AS.

        @param scope scope.
        """
        enodes: List[Node] = []
        nodes: List[Node] = []

        for obj in scope.getByType('rnode'):
            node: Node = obj

            if node in self.__additional_edges:
                enodes.append(node)
                continue

            is_edge = False
            for iface in node.getInterfaces():
                net = iface.getNet()
                if net.getType() == NetworkType.InternetExchange:
                    is_edge = True
                    break
                if True in (node.getRole() == NodeRole.Host for node in net.getAssociations()):
                    is_edge = True
                    break

            if is_edge: enodes.append(node)
            else: nodes.append(node)

        return (enodes, nodes)

    def __setUpLdpOspf(self, node: Router):
        """!
        @brief Setup LDP and OSPF on router.

        @param node node.
        """
        self._log('Setting up LDP and OSPF on as{}/{}'.format(node.getAsn(), node.getName()))

        node.setPrivileged(True)
        node.addSoftware('frr')

        ospf_ifaces = ''
        ldp_ifaces = ''
        mpls_iface_list = []

        # todo mask network from ospf?
        for iface in node.getInterfaces():
            net = iface.getNet()
            if net.getType() == NetworkType.InternetExchange: continue
            if not (True in (node.getRole() == NodeRole.Router for node in net.getAssociations())): continue
            ospf_ifaces += MplsFileTemplates['frr_config_ospf_iface'].format(interface = net.getName())
            ldp_ifaces += MplsFileTemplates['frr_config_ldp_iface'].format(interface = net.getName())
            mpls_iface_list.append(net.getName())
            net.setMtu(9000)

        node.setFile('/etc/frr/frr.conf', MplsFileTemplates['frr_config'].format(
            loopbackAddress = node.getLoopbackAddress(),
            ospfInterfaces = ospf_ifaces,
            ldpInterfaces = ldp_ifaces
        ))

        node.setFile('/frr_start', MplsFileTemplates['frr_start_script'])
        node.setFile('/mpls_ifaces.txt', '\n'.join(mpls_iface_list))
        node.addStartCommand('chmod +x /frr_start')
        node.addStartCommand('/frr_start')

    def __setUpIbgpMesh(self, nodes: List[Router]):
        """!
        @brief Setup IBGP full mesh.

        @param node list of nodes.
        """

        self._log('Setting up iBGP full mesh for edge nodes...')
        for local in nodes:

            n = 1
            for remote in nodes:
                if local == remote: continue

                local.addTable('t_bgp')
                local.addTablePipe('t_bgp')
                local.addTablePipe('t_direct', 't_bgp')
                local.addProtocol('bgp', 'ibgp{}'.format(n), MplsFileTemplates['bird_ibgp_peer'].format(
                    localAddress = local.getLoopbackAddress(),
                    peerAddress = remote.getLoopbackAddress(),
                    asn = local.getAsn()
                ))

                n += 1

    def onRender(self):
        for asn in self.__enabled:
            if self.__reg.has('seedsim', 'layer', 'Ospf'):
                self._log('Ospf layer exists, masking as{}'.format(asn))
                ospf: Ospf = self.__reg.get('seedsim', 'layer', 'Ospf')
                ospf.maskAsn(asn)

            if self.__reg.has('seedsim', 'layer', 'Ibgp'):
                self._log('Ibgp layer exists, masking as{}'.format(asn))
                ibgp: Ibgp = self.__reg.get('seedsim', 'layer', 'Ibgp')
                ibgp.mask(asn)

            scope = ScopedRegistry(str(asn))
            (enodes, nodes) = self.__getEdgeNodes(scope)

            for n in enodes: self.__setUpLdpOspf(n)
            for n in nodes: self.__setUpLdpOspf(n)
            self.__setUpIbgpMesh(enodes)

    def _doCreateGraphs(self):
        base: Base = self.__reg.get('seedsim', 'layer', 'Base')
        for asn in base.getAsns():
            if asn not in self.__enabled: continue
            asobj = base.getAutonomousSystem(asn)
            asobj.createGraphs()
            l2graph = asobj.getGraph('AS{}: Layer 2 Connections'.format(asn))
            mplsgraph = self._addGraph('AS{}: MPLS Topology'.format(asn), False)
            mplsgraph.copy(l2graph)
            for edge in mplsgraph.edges:
                edge.style = 'dotted'

            scope = ScopedRegistry(str(asn))
            (enodes, _) = self.__getEdgeNodes(scope)
            
            while len(enodes) > 0:
                a = enodes.pop()
                for b in enodes:
                    mplsgraph.addEdge('Router: {}'.format(a.getName()), 'Router: {}'.format(b.getName()), style = 'solid')

    def print(self, indent: int) -> str:
        out = ' ' * indent
        out += 'MplsLayer:\n'
        
        indent += 4
        out += ' ' * indent
        out += 'Enabled on:\n'

        indent += 4
        for asn in self.__enabled:
            out += ' ' * indent
            out += 'as{}\n'.format(asn)

        return out
            