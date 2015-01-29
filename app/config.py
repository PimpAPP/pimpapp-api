class Config():

    """TODO: Docstring for Config. """

    config_dict = {
        'SECRET_KEY': 'AReallySecretKey'
    }

    def init_app(self,  app):
        """TODO: Docstring for init_app.

        :app: TODO
        :config_dict: TODO
        :returns: TODO

        """
        app.config.update(**self.config_dict)


class DevelopmentConfig(Config):

    """TODO: Docstring for DevelopmentConfig. """

    def __init__(self, app=None):
        """TODO: Docstring for __init__.

        :arg1: TODO

        :app: TODO
        :returns: TODO

        """
        if app:
            self.config_dict.update({
                'DEBUG': True,
            })
            self.init_app(app)


class TestingConfig(Config):

    """Docstring for TestingConfig. """

    def __init__(self, app=None):
        """TODO: Docstring for __init__.

        :arg1: TODO

        :app: TODO
        :returns: TODO

        """
        if app:
            self.init_app(app)


class ProductionConfig(Config):

    """Docstring for ProductionConfig. """

    def __init__(self, app=None):
        """TODO: Docstring for __init__.

        :arg1: TODO

        :app: TODO
        :returns: TODO

        """
        if app:
            self.init_app(app)
        
config = {
        'development': DevelopmentConfig,    
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
}
