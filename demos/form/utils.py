def use_services(*services):
    """用于依赖注入"""
    def outer(func):
        def wrapper(s=services):
            return func(*s)

        return wrapper

    return outer
