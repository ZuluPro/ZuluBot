from django.contrib import messages

class Task_Result(dict):
    """
    Object for manipulate ZuluBot's method result.
    """
    TAGS = dict([ (v,k) for k,v in messages.DEFAULT_TAGS.items() ])
    STATUS = TAGS.keys()

    def __init__(self, **kwargs):
        super(Task_Result, self).__init__()
        self.success_msg = kwargs.get('success_msg','')
        self.info_msg = kwargs.get('info_msg','')
        self.warning_msg = kwargs.get('warning_msg','')
        self.error_msg = kwargs.get('error_msg','')
        # Set result list
        [ self.__setitem__(s, []) for s in self.STATUS ]
        # Set a dict for HTML strings
        self.pre_messages = dict([ (s,'') for s in self.STATUS ])
        
    def add_result(self,status,msg):
        """
        A shortcut to add result in list.
        """
        self[status].append(msg)

    def htmlize(self,status,header=''):
        """
        Convert results into one string.
        HTML is an unstyled unordered list like below:
        <ul class="unstyled">
         <li>Result #1</li>
         <li>Result #2</li>
        </ul>
        """
        self.pre_messages[status] = ''
        if header:
            self.pre_messages[status] += ('<p><b>%s</b></p>' % header)
        self.pre_messages[status] += '<ul class="unstyled">'
        for result in self[status]:
            self.pre_messages[status] += ('<li>%s</li>' % result )
        self.pre_messages[status] += '</ul>'
        return self.pre_messages[status]

    def make_messages(self, request, header=''):
        """
        Create messages from result and return them.
        """
        # Set dict of string which will contain HTML
        for status in self.TAGS:
            if self[status] :
                self.htmlize(status, header)
                # Create messages with HTML results
                messages.add_message(request, self.TAGS[status], self.pre_messages[status])
        return messages.get_messages(request)
