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

        if self.has(obj, 'data'):
            if self.has(obj.data, args[0]):
                return obj.data.__getattribute__(args[0])
            else:
                return None
        if self.has(obj, args[0]):
            return obj.__getattribute__(args[0])
        return None

    def has(self, obj, *args):
        """ has """
        if isinstance(obj, dict):
            j = obj
            for anarg in args[:-1]:
                j = j[anarg]
            return j.__contains__(args[-1]) and (j[args[-1]] is not None)
        if args.__len__() != 1:
            raise Exception("fieldMeasure", "only one arg allowed")
        if args[0] != 'data' and hasattr(obj, 'data'):
            return hasattr(obj.data, args[0]) and (obj.data.__getattribute__(args[0]) is not None)
        if hasattr(obj, args[0]):
            return hasattr(obj, args[0]) and (obj.__getattribute__(args[0]) is not None)
        return False

    def is_max(self, obj, value, *args):
        """ max """
        if self.has(obj, *args) is False:
            return True
        if isinstance(obj, dict):
            j = obj
            for anarg in args[:-1]:
                j = j[anarg]
            if j.__contains__(args[-1]):
                return [args[-1]] < value
            return False
        if args.__len__() != 1:
            raise Exception("fieldMeasure", "only one arg allowed")
        if self.has(obj, 'data'):
            if self.has(obj.data, args[0]):
                return obj.data.__getattribute__(args[0]) < value
            return False
        if self.has(obj, args[0]):
            return obj.__getattribute__(args[0]) < value
        return False

    def is_min(self, obj, value, *args):
        """ max """
        if self.has(obj, *args) is False:
            return True
        if isinstance(obj, dict):
            j = obj
            for anarg in args[:-1]:
                j = j[anarg]
            if j.__contains__(args[-1]):
                return [args[-1]] > value
            return False
        if args.__len__() != 1:
            raise Exception("fieldMeasure", "only one arg allowed")
        if self.has(obj, 'data'):
            if self.has(obj.data, args[0]):
                return obj.data.__getattribute__(args[0]) > value
            return False
        if self.has(obj, args[0]):
            return obj.__getattribute__(args[0]) > value
        return False

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
        if self.has(obj, 'data'):
            if self.has(obj.data, args[0]):
                obj.data.__setattr__(args[0], str(obj.data.__getattribute__(args[0]) + value))
            else:
                obj.data.__setattr__(args[0], str(value))
            return
        if self.has(obj, args[0]):
            obj.__setattr__(args[0], obj.__getattribute__(args[0]) + value)
        else:
            obj.__setattr__(args[0], value)
        return

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
        if self.has(obj, 'data'):
            obj.data.__setattr__(args[0], value)
            return
        if self.has(obj, args[0]):
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
