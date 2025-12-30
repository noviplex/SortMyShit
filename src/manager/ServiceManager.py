from inspect import signature


class ServiceManager:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self.service_container = {}
        self.aliases = {}
        self._initialized = True

    def get_service(self, service_name):
        return self.service_container[service_name]

    def register_service(self, service):
        dependencies = signature(service).parameters
        if len(dependencies) == 0:
            instantiated_service = service()
            self.service_container[service.__name__] = instantiated_service
            return instantiated_service
        else:
            instantiated_dependencies = []
            for dependency_name in dependencies:
                dependency = dependencies[dependency_name].annotation

                if dependency.__name__ in self.aliases:
                    dependency = self.aliases[dependency.__name__]

                if dependency.__name__ in self.service_container:
                    instantiated_dependencies.append(self.service_container[dependency.__name__])
                else:
                    instantiated_dependencies.append(self.register_service(dependency))

            instantiated = service(*instantiated_dependencies)
            self.service_container[service.__name__] = instantiated
            return instantiated

    def register_services(self, services):
        for service in services:
            self.register_service(service)

    def register_aliases(self, alias_services):
        self.aliases = alias_services
