import logging
import sys

import click
from keepasshttp import keepasshttp
from fortic.fortinet import FortiClient


@click.group()
@click.option("--path", "-p", type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
              help="Directory or path to FortiSSLVPNclient.exe")
@click.help_option("-h", "--help")
@click.pass_context
def main(ctx, path):
    """
    Connect to Fortinet SSL VPN Gateway

    I need FortiSSLVPNclient.exe and will search in:

    \b
    - C:\\Program Files (x86)\\Fortinet\\SslvpnClient
    - C:\\Program Files\\Fortinet\\SslvpnClient
    - in -p/--path given to the command (as file or directory)
    - in FORTISSLVPN_HOME environment variable
    - availability in PATH variable
    """
    ctx.obj = path
    pass


@click.command(help="Endpoint address")
@click.argument("url")
@click.pass_context
def connect(ctx, url):
    try:
        client = FortiClient(ctx.obj)
        creds = get_credentials(url)
        client.connect(url, creds.login, creds.password)
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


@click.command(help="Disconnect")
@click.pass_context
def disconnect(ctx):
    try:
        client = FortiClient(ctx.obj)
        client.disconnect()
        sys.exit(0)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


main.add_command(connect)
main.add_command(disconnect)


def get_credentials(url):
    logging.info("Retrieve credentials for '" + url + "'")
    credentials = keepasshttp.get(url)
    if credentials is None:
        raise Exception(
            "KeePass entry for '" + url + "' not found! Please add an entry with '" + url + "' as name or url")

    logging.info(f"Credentials found (User: {credentials.login})")
    return credentials


if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)-5s] %(message)s", stream=sys.stdout, level=logging.DEBUG)
    main()
