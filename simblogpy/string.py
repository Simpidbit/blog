import platform


def combine_multi_space__str(s) -> str:
    """Merge several consecutive spaces into one"""
    news = s.replace('  ', ' ')
    while news != s:
        s = news
        news = s.replace('  ', ' ')
    return news


def get_serious_name_from_path__str(filepath) -> str:
    """Get the file name based on the full path."""
    serious_name = filepath.split(SEP_SYMBOL)[-1]
    return serious_name
