from inspect import signature

class ServiceManager:
    def __new__(serviceManager):
        if not hasattr(serviceManager, 'instance'):
            serviceManager.instance = super(serviceManager, serviceManager).__new__(serviceManager)
        return serviceManager.instance

    def __init__(self):
        self.serviceContainer = {}

    def get(self, serviceName):
        return self.serviceContainer[serviceName]
    
    def registerService(self, service):
        dependencies = signature(service).parameters
        if len(dependencies) == 0:
            instantiatedService = service()
            self.serviceContainer[service.__name__] = instantiatedService
            return instantiatedService
        else:
            instantiatedDependencies = []
            for dependencyName in dependencies:
                dependency = dependencies[dependencyName].annotation

                if not dependency.__name__ in self.serviceContainer:
                    instantiatedDependencies.append(self.registerService(dependency))
                else:
                    instantiatedDependencies.append(self.serviceContainer[dependency.__name__])
            self.serviceContainer[service.__name__] = service(*instantiatedDependencies)

    def registerServices(self, services):
        for service in services:
            self.registerService(service)