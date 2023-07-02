import paramiko

# SSH connection details
hostname = 'your_router_ip'
username = 'your_username'
password = 'your_password'
port = 22

# Commands to run
commands = [
    'ip firewall filter',
    'add chain=input protocol=tcp psd=21,3s,3,1 action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w comment="Port scanners to list " disabled=no',
    'add chain=input protocol=tcp tcp-flags=fin,!syn,!rst,!psh,!ack,!urg action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w comment="NMAP FIN Stealth scan"',
    'add chain=input protocol=tcp tcp-flags=fin,syn action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w comment="SYN/FIN scan"',
    'add chain=input protocol=tcp tcp-flags=syn,rst action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w comment="SYN/RST scan"',
    'add chain=input protocol=tcp tcp-flags=fin,psh,urg,!syn,!rst,!ack action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w comment="FIN/PSH/URG scan"',
    'add chain=input protocol=tcp tcp-flags=fin,syn,rst,psh,ack,urg action=add-src-to-address-list address-list="port scanners" address-list-timeout=2w comment="ALL/ALL scan"',
    'add chain=input src-address-list="port scanners" action=drop comment="dropping port scanners" disabled=no',
    '/ip service disable [find name=telnet]',
    '/ip service disable [find name=ftp]',
    '/ip service disable [find name=www]',
    '/ip service disable [find name=www-ssl]',
    '/ip service disable [find name=api]',
    '/ip service disable [find name=api-ssl]',
    '/tool bandwidth-server set enabled=no',
    '/ip dns set allow-remote-requests=no',
    '/ip socks set enabled=no',
    '/tool romon set enabled=no',
    '/ip ssh set strong-crypto=yes',
    '/system package disable ipv6',
    '/system package disable mpls',
    '/system package disable hotspot',
    '/ip service set ssh port='your_port'',
    '/ip service set winbox port='your_port'',
]

# Establish SSH connection
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, port, username, password)

# Execute commands
for command in commands:
    stdin, stdout, stderr = client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        print(f'Command execution failed for "{command}" with exit status {exit_status}')

# Close SSH connection
client.close()
