from util.concatFilesUtil import *
from util.csvUtil import *

if __name__ == "__main__":
    file_path = "C:/Users/tomho/OneDrive/Documents/Promotion/smartRPA-action_logger/logs/Cleaned_1"
    data = read_multiple_csv_files(file_path)
    store_log(data, file_path, "concatenated_file.csv", ",")