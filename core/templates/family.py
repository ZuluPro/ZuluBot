# -*- coding: utf-8  -*-
# Family file created by ZuluBot

import family


class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = '{{ opts.family }}'
        self.langs = {
            '{{ opts.language }}': '{{ opts.family }}',
        }

    def version(self, code):
        return '{{ opts.version|default:"1.4.2"}}'

    def scriptpath(self, code):
        return '{{ scriptpath|default:"/wiki/" }}'
