# Database router

class AkbashRouter(object):

    # always use the default database for writing
    def db_for_write(self, model, **hints):
        return 'default'
