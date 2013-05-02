from django.core.management.base import BaseCommand, CommandError
from core.models import Wiki_User
from optparse import make_option
import logging


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-n', '--nick', action='store', default=False, help="Find user's nick"),
        make_option('-f', '--family', action='store', default=False, help="Find user's family"),
        make_option('-l', '--language', action='store', default=False, help="Find user's language"),
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
        if user.active():
            logging.info("'%s' is already active." % U.name)
            return

        if raw_input("Do you really want to active '%s' ? [Y/n] " % Us.get()) == 'n':
            logging.info('Aborted !')
            return

        U.set_active()
        logging.info(u"Set user '%s' active" % U.nick)
