import settings
from sys import exit, argv


if not settings.WIKI.get('path', None):
    print 'Please configure path of pywikipedia directory.'
    exit(1)
else:
    wiki_path = settings.WIKI['path']+'/user-config.py'

try:
    with open(wiki_path): pass
except IOError:
    print "You havn't yet configure your credentials on pywikipedia."
    print "Supposed credential file: '%s'" % wiki_path
    print "Please configure it before launch django environment.\n"

    ALLOWED_CMDS = ('add-wikiuser', 'del-wikiuser', 'syncdb')
    if not argv[1] in ALLOWED_CMDS:
        print "You can create file with './manage.py add-wikiuser'"
        exit(1)
    else:
        raw_input("Press enter to begin to configure it.")
