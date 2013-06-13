from wikipedia import Page
from pagegenerators import ReferringPageGenerator
import re

class Template(Page):
    """
    Subclass of Page that has some special tricks that only work for
    Template
    """
    REG_GET_FIELDS = re.compile(r'\{\{\{[^}]*\}\}\}')
    REG_DEL_AFTERPIPE = re.compile(r'\|.*$')

    def __init__(self, site, title, insite=None, defaultNamespace=10):
		super(Template,self).__init__(site=site, title=title, insite=insite, defaultNamespace=10)

    def get_fields(self):
        """
        Return a list of srings representing fields of models.
        """
        text = self.get()
        fields = REG_GET_FIELDS.findall(text)
        fields = [ f[3:-3] for f in fields ]
        fields = [ REG_DEL_AFTERPIPE.sub('',f) for f in fields ]
        return fields
