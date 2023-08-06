# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import os

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def save(
    path: str,
    content: str,
    encoding: str = 'utf8'
) -> bool:
    try:
        data = None

        if encoding:
            data = content.encode('utf8')
        else:
            data = content

        with open(path, 'wb') as file:
            file.write(data)

            return True
    except Exception as e:
        print(e)

        return False

def load(
    path: str,
    encoding: str = 'utf8'
) -> Optional[str]:
    try:
        with open(path, 'rb') as file:
            binary_content = file.read()

        return binary_content if not encoding else binary_content.decode(encoding)
    except Exception as e:
        print(e)

        return None