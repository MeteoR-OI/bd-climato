import json


class GetterSetter():
    """ FieldMeasure: abstraction for getter/setter of differents sources """
    def get(self, obj, *args):
        """ getter """
        if isinstance(obj, dict):
            j = obj
            for anarg in args:
                j = j[anarg]
            return j
        if args.__len__() != 1:
            raise Exception("fieldMeasure", "only one arg allowed")

        if hasattr(obj, 'data'):
            if hasattr(obj.data, args[0]):
                return obj.data.__getattribute__(args[0])
            else:
                return None
        if hasattr(obj.data, args[0]):
            return obj.__getattribute__(args[0])
        raise Exception("fieldMeasure", "unknown object " + obj.__class__)

    def has(self, obj, value, *args):
        """ has """
        if isinstance(obj, dict):
            j = obj
            for anarg in args[:-1]:
                j = j[anarg]
            return j.__contains__(args[-1])
        if args.__len__() != 1:
            raise Exception("fieldMeasure", "only one arg allowed")
        if hasattr(obj, 'data'):
            return hasattr(obj.data, args[0])
        if hasattr(obj.data, args[0]):
            return hasattr(obj.data, args[0])
        raise Exception("fieldMeasure", "unknown object " + obj.__class__)

    def add(self, obj, value, *args):
        """ add """
        if isinstance(obj, dict):
            j = obj
            for anarg in args[:-1]:
                j = j[anarg]
            if j.__contains__(args[-1]):
                j[args[-1]] += value
            else:
                j[args[-1]] = value
            return
        if args.__len__() != 1:
            raise Exception("fieldMeasure", "only one arg allowed")
        if hasattr(obj, 'data'):
            if hasattr(obj.data, args[0]):
                obj.data.__setattr__(args[0], obj.data.__getattribute__(args[0]) + value)
            else:
                obj.data.__setattr__(args[0], value)
            return
        if hasattr(obj.data, args[0]):
            if hasattr(obj.data, args[0]):
                obj.__setattr__(args[0], obj.__getattribute__(args[0]) + value)
            else:
                obj.__setattr__(args[0], value)
            return
        raise Exception("fieldMeasure", "unknown object " + obj.__class__)

    def set(self, obj, value, *args):
        """ setter """
        if isinstance(obj, dict):
            j = obj
            for anarg in args[:-1]:
                j = j[anarg]
            j[args[-1]] = value
            return
        if args.__len__() != 1:
            raise Exception("fieldMeasure", "only one arg allowed")
        if hasattr(obj, 'data'):
            if hasattr(obj.data, args[0]):
                obj.data.__setattr__(args[0], value)
                return
        if hasattr(obj.data, args[0]):
            obj.__setattr__(args[0], value)
            return
        raise Exception("fieldMeasure", "unknown object " + obj.__class__)


if __name__ == "__main__":
    # execute only if run as a script
    gs = GetterSetter()
    json_string = """
    {
        "meteor" : "BBF015",
        "info" : {
            "blabla": "blabla"
        },
        "data":
        [
            {
                "current":
                    {
                        "out_temp": 22
                    }
            }
        ]
    } """
    j = json.loads(json_string)
    print('j = meteor: ' + gs.get(j, 'meteor') + ', info.blabla: ' + gs.get(j, 'info', 'blabla') + ', data[0].current.out_temp: ' + str(gs.get(j, 'data', 0, 'current', 'out_temp')))

    print('Before set, j = ' + json.dumps(j))
    gs.set(j, 'new Meteor', 'meteor')
    gs.set(j, 'coze', 'info', 'blabla')
    gs.set(j, 25.6, 'data', 0, 'current', 'out_temp')
    print('After set, j = ' + json.dumps(j))
