from operator import attrgetter


def use_services(*services):
    """用于依赖注入"""

    def outer(func):
        def wrapper(s=services):
            return func(*s)

        return wrapper

    return outer


def clear_form(*forms):
    """清空form表单中已经填充的字段"""
    for form in forms:
        for fieldname in form.data.keys():
            field = attrgetter(fieldname)(form)
            field.data = None
