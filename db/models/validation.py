import re

def is_valid(pattern, field):
        if re.fullmatch(pattern, field):
            return True
        else:
            return False