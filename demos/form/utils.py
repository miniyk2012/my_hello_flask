def use_services(*services):
    def outer(func):
        def wrapper(s=services):
            return func(*s)

        return wrapper

    return outer
