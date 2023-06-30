Policy Routing
Overview
Policy routing is the method to steer traffic matching certain criteria to a certain gateway. This can be used to force some customers or specific protocols from the servers (for example HTTP traffic) to always be routed to a certain gateway. It can even be used to steer local and overseas traffic to different gateways.
RouterOS implements several components that can be used to achieve said task:
routing tables
routing rules
firewall mangle marking

Routing Tables
A router can have multiple routing tables with its own set of routes routing the same destination to different gateways.
Tables can be seen and configured from the /routing/table menu.
By default, RouterOS has only the 'main' routing table:
[admin@rack1_b33_CCR1036] /routing/table> print
Flags: D - dynamic; X - disabled, I - invalid; U - used
0 D name="main" fib
If a custom routing table is required, it should be defined in this menu prior to using it anywhere in the configuration.
Let's consider a basic example where we have two gateways 172.16.1.1 and 172.16.2.1 and we want to resolve 8.8.8.8 only in the routing table named 'myTable' to the gateway 172.16.2.1:
/routing table add name=myTable fib
/ip route add dst-address=8.8.8.8 gateway=172.16.1.1
/ip route add dst-address=8.8.8.8 gateway=172.16.2.1@main routing-table=myTable
For a user-created table to be able to resolve the destination, the main routing table should be able to resolve the destination too.
In our example, the main routing table should also have a route to destination 8.8.8.8 or at least a default route, since the default route is dynamically added by the DHCP for safety reasons it is better to add 8.8.8.8 also in the main table.
