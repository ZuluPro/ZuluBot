from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.conf import settings

from core.models import Wiki_User

from optparse import make_option
from os import symlink, mkdir, chdir, system
from logging import getLogger
logger = getLogger()

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-n', '--nick', action='store', default=False, help="Set user's nick"),
        make_option('-f', '--family', action='store', default=False, help="Set user's family"),
        make_option('-l', '--language', action='store', default=False, help="Set user's language"),
        make_option('-u', '--url', action='store', default=False, help="Set wiki's URL"),
        make_option('-c', '--comment', action='store', default='', help="Set a comment for user"),
        make_option('-a', '--active', action='store', default=None, help="Set user as active"),
        make_option('-C', '--create-user-config', action='store', default=False, help="Create user configuration files")
    #    make_option('-F', '--create-family-file', action='store', default=True, help="Create family file")
    )

    def handle(self, *args, **options):
        # Set Wiki_User attributes
        for opt in 'nick','language','family','url':
            if not options[opt]:
                options[opt] = raw_input(opt.capitalize()+"> ")
	# Set active or not
	if options['active'] is None:
            if raw_input('active [Y/n]') != 'n':
                options['active'] = True
            
        U = Wiki_User(
          nick=options['nick'],
          family=options['family'],
          language=options['language'],
          url=options['url'],
          comment=options['comment'],
	  active=options['active'] or False
        )

        try:
            U.full_clean() # Test to validate fields
            # Create bot dir
            bot_path = settings.BASEDIR+'/bots-config/'+U.nick+'/'
            mkdir(bot_path)
	    logger.info(u"Create folder '%s'" % bot_path)
            # Create families symlink from pwikipedia dir
	    families_symlink = settings.WIKI['path']+'/families'
            symlink(families_symlink, bot_path+'families')
	    logger.info(u"Create file '%s'" % families_symlink)
            # Create families symlink from pwikipedia dir
	    userinterfaces_symlink = settings.WIKI['path']+'/userinterfaces'
            symlink(userinterfaces_symlink, bot_path+'userinterfaces')
	    logger.info(u"Create file '%s'" % userinterfaces_symlink)
            
	    # append to  user-config.py in pywikipedia dir
            if options['create_user_config']:
	        with open(bot_path+'user-config.py', 'a') as f:
                    f.write("""family = '{0}'
                    mylang = '{1}'
                    usernames['{0}']['{1}'] = u'{2}' """.format(U.family,U.language,U.nick))
	        logger.info(u"Append to file '%s'" % bot_path+'user-config.py')

            # Launch pywikipedia's login.py
            if U.active:
	        logger.info(u"User is set as active, trying to login")
                chdir(settings.WIKI['path'])
                status_code = system('python login.py')

            U.save()
	    logger.info(u"Create user '%s'" % U.nick)
	except ValidationError as e:
	    logger.error(e.message)

