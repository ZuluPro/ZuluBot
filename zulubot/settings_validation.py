import settings
from sys import exit, argv


if not settings.WIKI.get('path',None):
    print 'Please configure path of pywikipedia directory.'
    exit(1)

try:
    with open(settings.WIKI['path']+'/user-config.py'): pass
except IOError:
    print "You havn't yet configure your credentials on pywikipedia."
    print "Supposed credential file: '%s'" % (settings.WIKI['path']+'/user-config.py')
    print "Please configure it before launch django environment.\n"

    if not 'addwikiuser' in argv or not 'deletewikiuser' in argv:
        print "You can create file with './manage.py addwikiuser'"
        exit(1)
    else:
        raw_input("Press enter to begin to configure it.")
