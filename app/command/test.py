import traceback


def func():
    return func3()


def func3():
    func2()


def func2():
    a = c = 2
    arr = [1, 2, 3]
    while a >= 0:
        if arr[a] != 1:
            del arr[a]
        if a == 0:
            c = 1 / 0
        a -= 1
    return c

#  sys.argv
if __name__ == "__main__":
    try:
        func()

    except Exception as exc:
        # parts = ["Traceback (most recent call last):\n"]
        # parts.extend(traceback.format_stack(limit=25)[:-2])
        # parts.extend(traceback.format_exception(*sys.exc_info())[1:])
        # print("".join(parts))

        stack = traceback.extract_stack()[:-3] + traceback.extract_tb(exc.__traceback__)  # add limit=??
        pretty = traceback.format_list(stack)
        pretty2 = []
        idx = pretty.__len__()
        idx2 = 4
        while idx2 > 0 and idx > 0:
            idx2 -= 1
            idx -= 1
            pretty2.append(pretty[idx])
        print('==>' + ''.join(pretty2))
        # print(''.format(exc.__class__, exc))
        print('=> ' + str(exc.__class__) + ':' + str(exc))
