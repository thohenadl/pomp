from util.concatFilesUtil import *
from util.csvUtil import *

if __name__ == "__main__":
    # Edit the path to navigate to the CSV files
    file_path = "logs/uilogs"
    data = read_multiple_csv_files(file_path)
    store_log(data, file_path, "concatenated_file.csv", ",")