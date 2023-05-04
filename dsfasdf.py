import os


def read_ticker_file():

    curr = os.getcwd()
    file_path = os.path.join(curr, "reza", "amiri", "hi.txt")
    with open(file_path, "r") as file:
        lines = file.readlines()
        print(lines)


read_ticker_file()