from app import main
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-b', '--bind', help='Binds the socket to this ip. Acts as host for game', action='store_true')
group.add_argument('-ip', '--address', help='Ip address of the host', type=str)
parser.add_argument('-p', '--port', help='Port to connect to', type=int, required=True)
args = parser.parse_args()


main(host=args.bind, port=args.port, ip=args.address)
