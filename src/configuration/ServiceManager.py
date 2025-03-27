class ServiceManager:
    def __new__(serviceManager):
        if not hasattr(serviceManager, 'instance'):
            serviceManager.instance = super(serviceManager, serviceManager).__new__(serviceManager)
        return serviceManager.instance

    def __init__(self):
        self.serviceContainer = {}

    def get(self, serviceName):
        return self.serviceContainer[serviceName]
    
    def registerService(self, serviceName, service):
        if not isinstance(service, type):
            raise TypeError("Service must be a class")
        if serviceName not in self.serviceContainer:
            self.serviceContainer[serviceName] = service()

    def unregisterService(self, serviceName):
        del self.serviceContainer[serviceName]

    def registerServices(self, services):
        for serviceName, service in services.items():
            self.registerService(serviceName, service)