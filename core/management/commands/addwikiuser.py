from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from core.models import Wiki_User
from optparse import make_option
from os import symlink, mkdir, chdir, system

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-n', '--nick', action='store', default=False, help="Set user's nick"),
        make_option('-f', '--family', action='store', default=False, help="Set user's family"),
        make_option('-l', '--language', action='store', default=False, help="Set user's language"),
        make_option('-u', '--url', action='store', default=False, help="Set wiki's URL"),
        make_option('-c', '--comment', action='store', default='', help="Set a comment for user"),
        make_option('-C', '--create-user-files', action='store', default=True, help="Create user configuration files")
    #    make_option('-F', '--create-family-file', action='store', default=True, help="Create family file")
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

        if U.id:
            bot_path = settings.BASEDIR+'/bots-config/'+U.nick+'/'
            mkdir(bot_path)
            symlink(settings.WIKI['path']+'/families', bot_path+'families')
            symlink(settings.WIKI['path']+'/userinterfaces', bot_path+'userinterfaces')
            
            f = open(bot_path+'user-config.py', 'wr')
            f.write("""
            family = '{0}'
            mylang = '{1}'
            usernames['{0}']['{1}'] = u'{2}'
            """.format(U.family,U.language,U.nick))
            f.close()

            chdir(settings.WIKI['path'])
            status_code = system('python login.py')

