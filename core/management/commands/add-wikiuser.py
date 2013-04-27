from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.conf import settings
from django.template import Context, loader

from core.models import Wiki_User
from core.validators import validate_family

import wikipedia
from login import LoginManager
import config

from optparse import make_option
from getpass import getpass
from os import symlink, mkdir, chdir, system
import re
import logging

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
	# Set nick
	if not options['nick']:
            options['nick'] = raw_input('Nick > ')
	# Set family
	if not options['family']:
            options['family'] = raw_input('Family (default:wikipedia) > ') or 'wikipedia'
	# Set language
	if not options['language']:
            options['language'] = raw_input('Language (default:en) > ') or 'en'
	# Set index URL
	if not options['url']:
            options['url'] = raw_input('Index URL > ')

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

        # Try to validate family
	try:
	    validate_family(options['family'])
	except ValidationError:
	    family_file = config.datafilepath('families')+('/%s_family') % options['family']
	    logging.error("Your family file '%s' doesn't exist." % family_file)
	    if raw_input('Do you want to create family file ? [Y/n] ') != 'n':
	        with open(family_file, 'w') as outfile:
	           t = loader.get_template('family.py')
		   c = Context({
                     'opts':options,
		     'scriptpath':raw_input("scriptpath (default:'/wiki/') >") or '/wiki/',
                   }) 
		   outfile.write(t.render(context))
	           logging.info("Create family file '%s'." % family_file)

        # Try to validate user in DB
        try:
            U.full_clean() # Test to validate fields
	except ValidationError as e:
	    logging.error('Bad value(s) given for fields.')
        else:
            try:
                # Create bot dir
                bot_path = settings.BASEDIR+'/bots-config/'+U.nick+'/'
                mkdir(bot_path)
	        logging.info(u"Create folder '%s'" % bot_path)
	    except OSError as e:
	        logging.info('Bots config file already exists')
            else:
                # Create families symlink from pwikipedia dir
	        families_symlink = settings.WIKI['path']+'/families'
                symlink(families_symlink, bot_path+'families')
	        logging.info(u"Create file '%s'" % families_symlink)
                # Create families symlink from pwikipedia dir
	        userinterfaces_symlink = settings.WIKI['path']+'/userinterfaces'
                symlink(userinterfaces_symlink, bot_path+'userinterfaces')
	        logging.info(u"Create file '%s'" % userinterfaces_symlink)
            

            # Launch pywikipedia's login.py
            if U.active:
	        L = LoginManager()
	        logging.info(u"User is set as active, trying to login")
		# Find if password file has been configured
		if not config.password_file:
                    logging.warning("Password file has not been configured. \
                      If you want automatic login please set it in '%s/config.py'." % \
                      settings.WIKI['path'])
                else:
                    # Try to see if user is in passwd file
		    user_found = False
		    passwd_file = wikipedia.config.datafilepath(config.password_file)
                    try:
                        with open(passwd_file, 'r') as f:
                            # Search user by syntax: tuple of 2 or 4
                            for line in f.readlines():
                                if not line.strip(): continue
                                entry = eval(line)
                                if len(entry) == 2:
                                    if entry[0] == U.nick: user_found = True
                                elif len(entry) == 4:
                                    if entry[2] == U.nick and \
                                      entry[0] == U.language and \
				      entry[1] == U.family:
                                        user_found = True
		        if not user_found:
		            # Purpose to create it
		            logging.info(u"User '%s' hasn't a passwd row in '%s'." % (U.nick,passwd_file)) 
                            if raw_input('Do you want to appent it ? [Y/n] ') != 'n':
                                with open(passwd_file, 'a') as f:
                                    password = getpass('Password > ')
                                    line = str( (U.language,U.family,U.nick,password) )
                                    f.write(line)
		    except IOError as e:
		        # Except files not exists and purpose to create
		        logging.warning("File '%s' does not exist" % passwd_file)
			if raw_input('Do you want to create it ? [Y/n] ') != 'n':
                            with open(passwd_file, 'w') as f:
                                password = getpass('Password > ')
                                line = str( (U.language,U.family,U.nick,password) )
                                f.write(line)

                    # Try to see if user exists in user-config
                    user_found = False
                    user_file = wikipedia.config.datafilepath('user-config.py')
                    REG_USER_LINE = re.compile("usernames\['(.*)'\]\['(.*)'\] = u?'(.*)'")
                    try:
                        with open(user_file, 'r') as f:
                            for line in f.readlines():
                                if REG_USER_LINE.match(line):
                                     family,lang,nick = REG_USER_LINE.sub(r'\1 \2 \3', line).split()
                                     if family == U.family and lang == U.language and nick == U.nick:
                                         user_found = True
                                         break

		    except IOError as e:
		        # If file doesn't exist create it.
		        logging.warning("File '%s' does not exist" % user_file)
                        with open(user_file, 'w') as f:
                            f.write("# -*- coding: utf-8  -*-")
		            logging.warning("Create file '%s'" % user_file)
		    finally:
		        if user_found:
		            logging.info(u"User '%s' has a row in '%s'." % (U.nick,user_file)) 
                        else:
		            logging.info(u"User '%s' hasn't a row in '%s'." % (U.nick,user_file))
                            # Ask for add line
                            if raw_input('Do you want to append user line ? [Y/n] ') != 'n':
                                with open(user_file, 'a') as f:
                                    user_line = "\nusernames['%s']['%s'] = u'%s'"  % (U.family,U.language,U.nick)
                                    f.write(user_line)
                                    # Ask for add sysops line
                                    if raw_input('Is user sysops ? [N/y] ') == 'y':
                                        sys_line = "sysopnames['%s']['%s'] = u'%s'"  % (U.family,U.language,U.nick)
                                        f.write(user_line)

                # Launch login script
                L.readPassword()
                is_logged = L.login()
			    
            U.save()
	    logging.info(u"Create user '%s' in Db" % U.nick)
