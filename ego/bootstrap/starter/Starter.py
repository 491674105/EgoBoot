from ego.classloader.ApplicationLoader import ApplicationLoader


class Starter:
    def __init__(self):
        self.__is_running = True

        self.application_loader = None

    def start_up(self, service_name):
        self.application_loader = ApplicationLoader(service_name=service_name)
        self.application_loader.scanner()

        return self.application_loader.load()

    def query_service(self, service_name):
        self.application_loader = ApplicationLoader(service_name=service_name)
        self.application_loader.query()

    def query_all_service(self):
        self.application_loader = ApplicationLoader()
        self.application_loader.query_all()
