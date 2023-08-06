import os
import sys

__dir__ = os.path.dirname(__file__)
sys.path.append(os.path.join(__dir__, '../../'))


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('command', type=str, default='start',
                        help='"start": start rpc server, "config": config rpc server')

    parser.add_argument('-sid', type=str, default='default', help='Server ID')
    parser.add_argument('-host', type=str, default='127.0.0.1', help='Host IP')
    parser.add_argument('-port', type=int, default=9900, help='Host Port')
    parser.add_argument('-key', type=str, default=None, help='Host Authkey')
    parser.add_argument('-f', type=str, default=None, help='Load config File(copy for ~/.adk)')

    return parser.parse_args()


def main():
    params = parse_args()
    cmd = params.command
    if cmd == 'config':
        from adk.rpc.rpc_cfg import set_rpc_config
        set_rpc_config(host=params.host, port=params.port, key=params.key,
                       server_id=params.sid, filename=params.f)
    elif cmd == 'start':
        from adk.rpc.rpc_manager import start_rpc_server
        start_rpc_server()


if __name__ == '__main__':
    main()
