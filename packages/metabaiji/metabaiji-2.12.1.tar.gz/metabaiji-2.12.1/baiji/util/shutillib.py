def mkdir_p(path):
    '''
    Implements ``mkdir -p``.
    '''
    import errno
    import os
    if path:
        try:
            os.makedirs(path)
        except OSError as ex:
            if ex.errno == errno.EEXIST:
                pass
            else:
                raise
