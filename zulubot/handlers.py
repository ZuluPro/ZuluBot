from django.conf import settings
from celery import task
import wikipedia, catlib, pagegenerators
import re

class wiki_handler(object):
    REDIRECT = '#REDIRECTION [[%s]]'

    def __init__(self):
        self.language = settings.WIKI['language']
        self.family = settings.WIKI['family']
        self.site = wikipedia.getSite(self.language,self.family)

    def get_all(self, namespace=None):
        """
        Return all Pages objects as iterator.
        """
        return pagegenerators.AllpagesPageGenerator(namespace=namespace)

    def search_words(self, key, namespaces=None):
        """
        Get all Pages containing the given words.
        A namespace filter is available.
        """
        return pagegenerators.SearchPageGenerator(key, number=0, namespaces=namespaces)

    def search_in_title(self, key, namespaces=None):
        """
        Get pages which title matching with given key.
        This key is a case insensitive regex.
        """
        regex = re.compile(key, re.I)

        pages = self.get_all(namespaces)
        for page in pages :
            if regex.search(page.titleWithoutNamespace()):
                yield page

    def get_page(self, page):
        """
        Get a Page object by his name.
        """
        if isinstance(page, wikipedia.Page):
            pass
        elif isinstance(page, basestring):
            page = wikipedia.Page(self.site, page)
        return page 

    def delete_page(self, page):
        """
        Delete a category.
        """
        self.get_page(page).delete(
            reason='-Suppression',
            prompt=False,
            mark=True
        )

    def move_page(self, old, new, redirect=False):
        """
        Move content of page to another one and delete it.
        """
        old_page = self.get_page(old)
        new_page = self.get_page(new)
        try:
            new_page.put(
                newtext=old_page.get(),
                comment=u'D\xe9placement de %s vers %s' % (old_page.title(),new_page.title()),
                minorEdit=False,
            )
        except wikipedia.IsRedirectPage :
            pass
        except wikipedia.NoPage :
            pass
        else:
            if redirect :
                old_page.put(
                    newtext=self.REDIRECT % new_page.title(),
                    comment=u'D\xe9placement de %s vers %s' % (old_page.title(),new_page.title()),
                    minorEdit=False,
                )
            else :
                self.delete_page(old_page)

    def move_pages(self, pages, pat, rep, redirect=False):
        """
        Rename a list of pages with pattern replacement.
        """
        # Format pages arg
        if not isinstance(pages, (tuple,list)) :
            pages = (pages,)
        else:
            pages = list(set(pages))

        results = {'error':[],'success':[],'warning':[]}
        ERROR = u'D\xe9placement de "%s" vers "%s" \xe9chou\xe9'
        SUCCESS = u'"%s" d\xe9plac\xe9 vers "%s"'
        WARNING = u'Pas de modification sur "%s"'
        for p in pages:
            try:
                old_page = self.get_page(p)
                new_page = self.get_page(re.sub(pat,rep,p.title()))
                if old_page != new_page :
                    self.move_page(old_page, new_page, redirect)
                    msg = SUCCESS % (old_page.title(), new_page.title())
                    results['success'].append([p,msg])
                else:
                    msg = WARNING % old_page.title()
                    results['warning'].append([p,msg])

            except:
                msg = ERROR % (old_page.title(), new_page.title())
                results['error'].append([p,msg])

        return results

    def get_category(self, category):
        """
        Get a category by its short or long name.
        """
        if isinstance(category, catlib.Category):
            pass
        elif isinstance(category, basestring):
            category = catlib.Category(self.site, category)
        elif issubclass(type(category), wikipedia.Page):
            category = catlib.Category(self.site, category.title())

        return category

    def add_category(self, pages, category):
        """
        Add a category to a list of page's name.
        Work if pages list is a single pagename.
        """
        # Format pages arg
        if not isinstance(pages, (tuple,list)) :
            pages = (pages,)
        else:
            pages = list(set(pages))
        # Format category arg
        category = self.get_category(category)

        results = {'error':[],'success':[],'warning':[]}
        SUCCESS = u'"%s" ajout\xe9e \xe0 "%s".'
        WARNING = u'"%s" d\xe9j\xe0 pr\xe9sente dans "%s".'
        for p in pages :
            p = self.get_page(p)
            try :
                old_text = p.get()

            # Do not touch redirect pages
            except wikipedia.IsRedirectPage as e:
                results['error'].append([p,e])
            else :
                # Cat is already present
                if re.search((u'\[\[%s\]\]' % category.title()) , old_text) :
                    msg = WARNING % (category.title(), p.title())
                    results['warning'].append([p,msg])
                else:
                    # Search if a category zone is present
                    s = re.search('\[\[Cat.gorie:[^\]]*\]\]', old_text)
                    if s :
                        new_text = old_text[:s.end()]+ (u'\n[[%s]]' % \
                                category.title()) +old_text[s.end():]
                    else :
                        new_text = old_text+(u'\n[[%s]]' % category.title())
                    p.put(new_text, comment=(u'+[[%s]]' % category.title()))
                    msg = SUCCESS % (category.title(), p.title())
                    results['success'].append([p,msg])
        return results 

    def delete_category(self, category):
        """
        Delete a category.
        """
        results = {'error':[],'success':[],'warning':[]}
        self.get_category(category).delete(
            reason='-Suppression',
            prompt=False,
            mark=True
        )
        msg = u'Cat\xe9gorie "%s" supprim\xe9e.' % (category.title(), p.title())
        results['success'].append([p,msg])
        return results 

    def remove_category_from(self, pages, category):
        """
        Remove a category to a list of page's name.
        Work if pages list is a single pagename.
        """
        # Format pages arg
        if not isinstance(pages, (tuple,list)) :
            pages = (pages,)
        else:
            pages = list(set(pages))
        # Format category arg
        category = self.get_category(category)

        SUCCESS = u'Cat\xe9gorie "%s" supprim\xe9e.'
        results = {'error':[],'success':[],'warning':[]}
        for p in pages :
            p = self.get_page(p)
            new_text = p.get().replace((u'[[%s]]' % category.title()), '')
            p.put(new_text, comment=(u'-[[%s]]' % category.title()))
            msg = SUCCESS % (category.title(), p.title())
            results['success'].append([p,msg])
        return results 

    def move_category(self, old, new):
        """
        Move all category's Pages to an another one.
        Delete the old category.
        If new doesn't exits put the text of old one.
        """
        old_cat = self.get_category(old)
        new_cat = self.get_category(new)
        pages = old_cat.articlesList()
        self.remove_category_from([ p.title() for p in pages ], old_cat.title()) 
        self.add_category([ p.title() for p in pages ], new_cat.title) 

        results = {'error':[],'success':[],'warning':[]} 
        if not new_cat.exists() and old_cat.exists() :
            new_cat.put(
                newtext=old_cat.get(),
                comment=u'D\xe9placement de %s vers %s' % (old_cat.title(),new_cat.title()),
                minorEdit=False,
            )
        self.delete_category(old_cat.title())

