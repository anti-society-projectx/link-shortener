class LinkError(Exception):
    pass

class LinkNotFoundError(LinkError):
    pass


class LinkAlreadyExistsError(LinkError):
    pass
