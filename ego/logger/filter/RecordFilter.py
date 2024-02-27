from logging import Filter

from threading import current_thread as get_current_thread

from ego import applicationContext


class RecordFilter(Filter):
    def __init__(self, root_path, service_port=-1, name=""):
        super().__init__(name=name)
        self.root_path = root_path
        self.service_port = service_port
        self.uri = ""

    def filter(self, record):
        if record.threadName == "APScheduler":
            return None

        current_thread = get_current_thread()
        if not hasattr(applicationContext, "uri_dict") or current_thread.ident not in applicationContext.uri_dict:
            record.uri = "-"
        else:
            record.uri = applicationContext.uri_dict[current_thread.ident]

        if self.service_port and self.service_port > 0:
            record.service_port = self.service_port
        else:
            record.service_port = -1
        try:
            record.relate_path = record.pathname.split(self.root_path, 1)[1]
        except Exception:
            record.relate_path = record.pathname
        return record
