class ResourceFetchError(Exception):
    '''Exception raised for errors in fetching a resource.
    '''
    def __init__(self, error=None, message='Resource fetching failed'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.error}'

class ResourceCreationError(Exception):
    '''Exception raised for errors in the creation of a resource.
    '''
    def __init__(self, error=None, message='Resource creation failed'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.error}'

class ResourceDeletionError(Exception):
    '''Exception raised for errors in the deletion of a resource.
    '''
    def __init__(self, error=None, message='Resource deletion failed'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.error}'

class ResourceUpdateError(Exception):
    '''Exception raised for errors while updating a resource.
    '''
    def __init__(self, error=None, message='Resource update failed'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.error}'

class UnauthorizedError(Exception):
    '''Exception raised for unauthorized actions.
    '''
    def __init__(self, error=None, message='Unauthorized action'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.error}'


class UnexpectedError(Exception):
    '''Exception raised for an unexpected error.'''

    def __init__(self, error=None, message='Unexpected error'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.error}'

