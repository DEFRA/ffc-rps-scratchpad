def get_filename(relative_link):
    """Derive a filename from the helpful url."""
    return relative_link.split('/')[-1] + '.txt'


def get_code(relative_link):
    """Recover the action's code from the url also"""
    output_filename = get_filename(relative_link)
    return output_filename.split('-')[0].upper()