# fortic
Fortinet SSLVPN client command line with KeePass support

# Installation
SSLVPNcmdline tools from Fortinet are required (FortiSSLVPNclient.exe)  
`pip install fortic`

# Usage
```
Usage: fortic.py [OPTIONS] COMMAND [ARGS]...

  Connect to Fortinet SSL VPN Gateway

  I need FortiSSLVPNclient.exe and will search in:

  - C:\Program Files (x86)\Fortinet\SslvpnClient
  - C:\Program Files\Fortinet\SslvpnClient
  - in -p/--path given to the command (as file or directory)
  - in FORTISSLVPN_HOME environment variable
  - availability in PATH variable

Options:
  -p, --path PATH  Directory or path to FortiSSLVPNclient.exe
  -h, --help       Show this message and exit.

Commands:
  connect     Endpoint address
  disconnect  Disconnect
```

# Examples
Entry in KeePass must be named or have a configured URL equal vpn-server-url.
```
fortic connect vpn.example.com
fortic disconnect
```

# Changelog
## v0.1
- Initial version with basic features