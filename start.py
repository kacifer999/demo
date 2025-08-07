import sys
import cyai
from pathlib import Path


if __name__ == "__main__":
    sys.path.append(str(Path(__file__)))
    cyai.start()