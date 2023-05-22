class ResourceFetchError(Exception):
    '''Exception raised for errors in fetching a resource.
    '''
    def __init__(self, message='Resource fetching failed'):
        self.message = message
        super().__init__(self.message)

class ResourceCreationError(Exception):
    '''Exception raised for errors in the creation of a resource.
    '''
    def __init__(self, message='Resource creation failed'):
        self.message = message
        super().__init__(self.message)

class ResourceDeletionError(Exception):
    '''Exception raised for errors in the deletion of a resource.
    '''
    def __init__(self, message='Resource deletion failed'):
        self.message = message
        super().__init__(self.message)

class ResourceUpdateError(Exception):
    '''Exception raised for errors while updating a resource.
    '''
    def __init__(self, message='Resource update failed'):
        self.message = message
        super().__init__(self.message)

class UnauthorizedError(Exception):
    '''Exception raised for unauthorized actions.
    '''
    def __init__(self, message='Unauthorized action'):
        self.message = message
        super().__init__(self.message)


class UnexpectedError(Exception):
    '''Exception raised for an unexpected error.'''

    def __init__(self, error=None, message='Unexpected error'):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.error}'

