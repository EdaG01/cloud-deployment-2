"""An example of using parameters to construct a profile with a variable
number of nodes.

Instructions:
Wait for the profile instance to start, and then log in to one or more of
the VMs via the ssh port(s) specified below.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec

# Describe the parameter(s) this profile script can accept.
portal.context.defineParameter( "n", "Number of VMs", portal.ParameterType.INTEGER, 4 )

# Retrieve the values the user specifies during instantiation.
params = portal.context.bindParameters()

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Check parameter validity.
if params.n < 1 or params.n > 4:
    portal.context.reportError( portal.ParameterError( "You must choose at least 1 and no more than 4 VMs." ) )

link = request.LAN("lan")

for i in range( params.n ):

    node = request.XenVM("node-" + str( i + 1))
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//CENTOS7-64-STD" 
    iface = node.addInterface("if")
    
    node.routable_control_ip = True 
    if( i + 1 == 1):
        iface = node.addInterface("if")
    
    # Create a XenVM and add it to the RSpec.
    iface.component_id = "eth1"
    iface.addAddress(rspec.IPv4Address("192.168.1." + str( i + 1), "255.255.255.0"))
    
    link.addInterface(iface)


# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
