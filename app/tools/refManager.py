
class RefManager:
    """
        RefManager


    """
    all_refs = {}

    @staticmethod
    def GetInstance():
        # return the instance
        if RefManager.__dict__.__contains__('my_instance') is False:
            RefManager.my_instance = RefManager()
        return RefManager.my_instance
    
    def AddRef(self, name: str, my_reference):
        if my_reference is None:
            self.all_refs.__delitem__(name)
        else:
            self.all_refs[name] = my_reference

    def GetRef(self, name: str):
        if self.all_refs.__contains__(name):
            return self.all_refs[name]
        return None

    def DelRef(self, name: str):
        self.all_refs.__delitem__(name)
