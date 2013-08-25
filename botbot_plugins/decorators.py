def listens_to_mentions(rule):
    """Decorator to add function and rule to routing table"""

    def decorator(func):
        func.route_rule = ('mentions', rule)
        return func
    return decorator

def listens_to_all(rule):
    """Decorator to add function and rule to routing table"""

    def decorator(func):
        func.route_rule = ('messages', rule)
        return func
    return decorator