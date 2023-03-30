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

    total_rows_count, total_files_count, unique_rows_count, unique_uis = stats(path_to_untagged)
    pickle_set(unique_uis)

    sys.exit()