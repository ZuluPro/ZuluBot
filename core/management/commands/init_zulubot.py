from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-n', '--nick', action='store', default=False, help="Set user's nick"),
        make_option('-f', '--family', action='store', default=False, help="Set user's family"),
        make_option('-l', '--language', action='store', default=False, help="Set user's language"),
        make_option('-u', '--url', action='store', default=False, help="Set wiki's URL"),
        make_option('-c', '--comment', action='store', default='', help="Set a comment for user")
    )

    def handle(self, *args, **options):
        for opt in 'nick','language','family','url':
            if not options[opt]:
                options[opt] = raw_input(opt.capitalize()+"> ")
        U = Wiki_User(
          nick=options['nick'],
          family=options['family'],
          language=options['language'],
          url=options['url'],
          comment=options['comment']
        )
        U.save()
