def convert_octets(size):
    for x in ['octets', 'Ko', 'Mo', 'Go', 'To']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
