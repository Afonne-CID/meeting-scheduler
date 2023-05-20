class ResourceCreationError(Exception):
    """Exception raised for errors in the creation of a resource."""

    def __init__(self, message="Resource creation failed"):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    """Exception raised for unauthorized actions."""

    def __init__(self, message="Unauthorized action"):
        self.message = message
        super().__init__(self.message)


class UnexpectedError(Exception):
    """Exception raised for an unexpected error."""

    def __init__(self, message="Unexpected error"):
        self.message = message
        super().__init__(self.message)
