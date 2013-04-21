class Task_Result(dict):
    def __init__(self):
        super(Task_Result, self).__init__()
		self.success_msg = kwargs.get('success_msg','')
		self.info_msg = kwargs.get('info_msg','')
		self.warning_msg = kwargs.get('warning_msg','')
		self.error_msg = kwargs.get('error_msg','')
        for status in 'success','info','warning','error':
            self[status] = []
		
	def add_result(self,msg,status):
		self[status].append(msg)

	def add_success(self,msg):
		self.add_result(msg,'success')

	def add_info(self,msg):
		self.add_result(msg,'info')

	def add_warning(self,msg):
		self.add_result(msg,'warning')

	def add_error(self,msg):
		self.add_result(msg,'error')
