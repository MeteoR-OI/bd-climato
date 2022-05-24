import traceback


def func1():
    try:
        func2()
    except Exception as exc:
        traceback.print_exc()
    finally:
        print('bye')


def func2():
    try:
        func3()
    except Exception as exc:
        traceback.print_exc()
        raise(exc)


def func3():
    raise Exception('in func3')


if __name__ == '__main__':
    func1()