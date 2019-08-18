import pkg_resources

__version__ = pkg_resources.get_distribution(
    'tictactoe').version


from tictactoe import scripts  # NOQA
