import json
import subprocess


class NetStool:

    def __init__(self):
        self.cmd = []

    def network_interfaces(self, state='up'):
        _cmd = "ip -br -j addr show".split(" ")
        self.cmd.extend(_cmd)
        _data = self._run()
        return [inter for inter in _data if inter['operstate'].lower() == state]

    def trace_route(self, url: str):
        pass

    def _run(self):
        result = subprocess.run(self.cmd, capture_output=True, text=True)
        return json.loads(result.stdout)


ns = NetStool()
data = ns.network_interfaces()
print(data)
