from inspect import signature


class ServiceManager:
    def __new__(serviceManager):
        if not hasattr(serviceManager, 'instance'):
            serviceManager.instance = super(serviceManager, serviceManager).__new__(serviceManager)
        return serviceManager.instance

    def __init__(self):
        self.serviceContainer = {}
        self.aliases = {}

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

                if dependency.__name__ in self.aliases:
                    dependency = self.aliases[dependency.__name__]

                if dependency.__name__ in self.serviceContainer:
                    instantiatedDependencies.append(self.serviceContainer[dependency.__name__])
                else:
                    instantiatedDependencies.append(self.registerService(dependency))

            self.serviceContainer[service.__name__] = service(*instantiatedDependencies)

    def registerServices(self, services):
        for service in services:
            self.registerService(service)

    def registerAliases(self, aliasServices):
        self.aliases = aliasServices
