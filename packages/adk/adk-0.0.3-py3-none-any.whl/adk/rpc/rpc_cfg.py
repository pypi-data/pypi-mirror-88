import os
import json

CFG_FN = os.path.expanduser('~/.adk')

__all__ = ['set_rpc_config', 'get_rpc_config', 'rpc_connect_args']


def _load_json(fn):
    with open(fn, 'r')as f:
        res_dic = json.load(f)
    return res_dic


def set_rpc_config(host='127.0.0.1', port=9900, key=None, server_id='default', filename=None):
    import base64
    if filename:
        cfg_dic = _load_json(filename)
    else:
        if os.path.exists(CFG_FN):
            cfg_dic = _load_json(CFG_FN)
        else:
            cfg_dic = {}
        cfg_dic.setdefault(server_id, {})
        key = key or base64.b64encode(os.urandom(32)).decode()
        cfg_dic[server_id].update(host=host, port=port, key=key)
    with open(CFG_FN, 'w')as f:
        json.dump(cfg_dic, f, indent=4)


def get_rpc_config(server_id='default'):
    return _load_json(CFG_FN)[server_id]


def rpc_connect_args(server=False, server_id='default'):
    cfg = get_rpc_config(server_id=server_id)
    host = '0.0.0.0' if server else cfg['host']
    port = cfg['port']
    key = cfg['key'].encode()
    return (host, port), key


if __name__ == '__main__':
    set_rpc_config()
