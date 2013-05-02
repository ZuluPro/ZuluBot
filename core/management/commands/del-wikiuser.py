from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.models import Wiki_User

from optparse import make_option
from os import remove, rmdir
import logging


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-n', '--nick', action='store', default=False, help="Find user's nick"),
        make_option('-f', '--family', action='store', default=False, help="Find user's family"),
        make_option('-l', '--language', action='store', default=False, help="Find user's language"),
        make_option('-D', '--delete-user-config', action='store', default=False, help="Delete user configuration files")
    )

    def handle(self, *args, **options):
        Us = Wiki_User.objects.all()
        # Stop if there's no user in Db
        if Us.count() == 0:
            print "There's no user in database."
            return

        # If there's only 1 user, choose it
        if Us.count() == 1:
            pass

        # Search user by args or asking
        else:
            if not options['nick']:
                nick_list = [ U.nick for U in Us ]
                if len(nick_list) > 1:
                    print '\n'.join([ ('%s: %s' % (i, n)) for i, n in enumerate(nick_list) ])
                    num = int(raw_input('Which nick do you choose ? : '))
                    options['nick'] = nick_list[num]
                else:
                    options['nick'] = nick_list[0]
            Us = Us.filter(nick=options['nick'])
            print(u"Nick : %s" % options['nick'])

            if not options['family']:
                family_list = [ U.family for U in Us ]
                if len(family_list) > 1:
                    print '\n'.join([ ('%s: %s' % (i, f)) for i, f in enumerate(family_list) ])
                    num = int(raw_input('Which family do you choose ? : '))
                    options['family'] = family_list[num]
                else:
                    options['family'] = family_list[0]
            Us = Us.filter(family=options['family'])
            print(u"Family : %s" % options['family'])

            if not options['language']:
                lang_list = [ U.language for U in Us ]
                if len(lang_list) > 1:
                    print '\n'.join([ ('%s: %s' % (i, l)) for i, n in enumerate(lang_list) ])
                    num = int(raw_input('Which language do you choose ? : '))
                    options['language'] = lang_list[num]
                else:
                    options['language'] = lang_list[0]
            Us = Us.filter(language=options['language'])
            print(u"Language : %s" % options['language'])

        U = Us.get()

        if raw_input("Do you really want to delete '%s' ? [N/y] " % Us.get()) != 'y':
            logging.info('Aborted !')
            return

        bot_path = settings.BASEDIR+'/bots-config/'+U.nick+'/'
        try:
            # Delete families symlink from pwikipedia dir
            families_symlink = settings.WIKI['path']+'/families'
            remove(bot_path+'families')
            logging.info(u"Remove file '%s'" % families_symlink)
        except (OSError, IOError):
            logging.warning(u"No file to delete : '%s'" % families_symlink)

        try:
            # Delete families symlink from pwikipedia dir
            userinterfaces_symlink = settings.WIKI['path']+'/userinterfaces'
            remove(bot_path+'userinterfaces')
            logging.info(u"Remove file '%s'" % userinterfaces_symlink)
        except (OSError, IOError):
            logging.warning(u"No file to delete : '%s'" % userinterfaces_symlink)

        # TODO
        # Don't delete folder if there another files
        try:
            # Delete bot dir
            rmdir(bot_path)
            logging.info(u"Delete folder '%s'" % bot_path)
        except (OSError, IOError):
            logging.warning(u"No folder to delete : '%s'" % bot_path)

        U.delete()
        logging.info(u"Delete user '%s' in Db" % U.nick)
        logging.info(u"You can delete manually your credentials in '%s'." % settings.WIKI['path'])
