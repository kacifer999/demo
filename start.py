import sys
import main
from pathlib import Path


if __name__ == "__main__":
    sys.path.append(str(Path(__file__)))
    main.start()