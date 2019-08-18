import pkg_resources

__version__ = pkg_resources.get_distribution(
    'autogames').version


from autogames import scripts  # NOQA
