# Import generic Python libraries
import argparse
import pandas as pd
import sys

# Import project specific
import util.csvUtil
from util.statsUtil import *
from const import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = '''Getting Metrics from Log files''',
        epilog      = """For more information see source code comments."""
    )
    # parser.add_argument('filename')   
    args = parser.parse_args()

    stats(path_to_untagged)

    sys.exit()