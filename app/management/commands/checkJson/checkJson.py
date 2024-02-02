import sys
from app.tools.jsonValidator import checkJson
from app.tools.jsonPlus import JsonPlus
#  sys.argv
if __name__ == "__main__":

    # uncomment to pass test filename in debug mode
    if sys.argv.__len__() == 1:
        sys.argv.append('./data/json_in_git/MTG320/obs.MTG320.2022-02-28T22:25.json')
        # data/json_in_git/json_examples/obs_daily.BBF015.2022_02_01.json')

    idx = 1
    while idx < sys.argv.__len__():
        filename = sys.argv[idx]

        with open(filename, "r") as f:
            file_content = f.readlines()
            json_str = ''
            for one_line in file_content:
                json_str += str(one_line)

            j_content = JsonPlus().loads(json_str)

            ret = checkJson(j_content, filename)
            if ret is None:
                print("file ok")
            else:
                print(ret)
            idx += 1
