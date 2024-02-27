from ego import applicationContext


class LazyLoader:
    @staticmethod
    def commit_lazy_load_module(module_id, loader, args: list, kwargs: dict):
        applicationContext.lazy_load_modules[module_id] = {
            "loader": loader,
            "args": args,
            "kwargs": kwargs
        }
        applicationContext.lazy_module_launched[module_id] = False
