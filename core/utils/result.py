class Task_Result(dict):
    def __init__(self):
        super(Task_Result, self).__init__()
        for status in 'success','info','warning','error':
            self[status] = []
