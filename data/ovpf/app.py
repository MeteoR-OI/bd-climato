import os


def get_files_in_subdirectories(directory):
    tmp_files = []
    i = 2007
    while i <= 2024:
        tmp_files.append([])
        i += 1
    for root, dirs, files in os.walk(directory):
        if root == '.' or root.startswith('./.venv'):
            continue
        year = int(root[2::]) - 2007

        for file in files:
            if file.endswith(".csv") or file.endswith(".txt"):
                tmp_files[year].append(os.path.join(file))
                # with open(file_path, "r") as f:
                # Do something with the file
                # For example, print its contents
                # print(f.read())
    # tmp_files.sort()
    return tmp_files


def process_files(all_files):
    i = 0
    while i < len(all_files):
        year = 2007 + i
        print("year: " + str(year))
        for file in all_files[i]:
            print(file)
            with open('./' + str(year) + '/' + file, "r") as f:
                # Do something with the file
                # For example, print its contents
                print(f.read())


# Usage example
directory_path = "."
all_files = get_files_in_subdirectories(directory_path)
process_files(all_files)
