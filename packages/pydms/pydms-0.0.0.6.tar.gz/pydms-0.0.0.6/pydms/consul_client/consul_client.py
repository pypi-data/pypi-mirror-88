import consul

class ConsulClient(object):
    def __init__(self, host, port):
        '''初始化，连接consul服务器'''
        self._consul = consul.Consul(host, port)

    def registerService(self, name, host, port, tags=None):
        tags = tags or []
        # 注册服务
        self._consul.agent.service.register(
            name,
            name,
            host,
            port,
            tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
            check=consul.Check().tcp(host, port, "5s", "30s", "30s"))

    def getService(self, name):
        services = self._consul.agent.services()
        service = services.get(name)
        if not service:
            return None, None
        addr = "{0}:{1}".format(service['Address'], service['Port'])
        return service, addr

def consul_check_tcp( host, port, interval, timeout=None, deregister=None):
    return consul.Check.tcp(host,port,interval,timeout,deregister)


def demo():
    host = "127.0.0.1"  # consul服务器的ip
    port = "8500"  # consul服务器对外的端口
    consul_client = ConsulClient(host, port)

    name = "maple"
    host = "127.0.0.1"
    port = 8510
    consul_client.registerService(name, host, port)

    check = consul.Check().tcp(host, port, "5s", "30s", "30s")
    print(check)
    res = consul_client.getService("maple")
    print(res)


if __name__ == '__main__':
    demo()