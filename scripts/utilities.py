import re

def find_name(name, sentence):
    return re.match(r'(^({0})([ .!?,…]|(’s[ .!?,…])).*)|(.*[ …]{0}([ .!?,…]|(’s[ .!?,…])).*)|(.* ({0})$)'.format(name), sentence)