from django.conf import settings
from core.utils import Task_Result
import wikipedia, catlib, userlib, pagegenerators
from datetime import datetime
import re

class wiki_handler(object):
    """
    Wiki handling, for make simply complex operations.
    """
    REDIRECT = '#REDIRECTION [[%s]]'

    def __init__(self):
        self.nick = settings.WIKI['nick']
        self.language = settings.WIKI['language']
        self.family = settings.WIKI['family']
        self.site = wikipedia.getSite(self.language,self.family)
        self.user = userlib.User(self.site,self.nick)

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

        results = Task_Result()
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
                    results.add_result('success',msg)
                else:
                    msg = WARNING % old_page.title()
                    results.add_result('warning',msg)

            except:
                msg = ERROR % (old_page.title(), new_page.title())
                results.add_result('error',msg)

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

        results = Task_Result()
        SUCCESS = u'"%s" ajout\xe9e \xe0 "%s".'
        WARNING = u'"%s" d\xe9j\xe0 pr\xe9sente dans "%s".'
        for p in pages :
            p = self.get_page(p)
            try :
                old_text = p.get()
            # Do not touch redirect pages
            except wikipedia.IsRedirectPage as e:
                results.add_result('error', e.message)
            else :
                # Cat is already present
                if re.search((u'\[\[%s\]\]' % category.title()) , old_text) :
                    msg = WARNING % (category.title(), p.title())
                    results.add_result('warning', msg)
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
                    results.add_result('success',msg)
        return results 

    def delete_category(self, category):
        """
        Delete a category.
        """
        # TODO
        # Exception : Page already deleted
        results = Task_Result()
        self.get_category(category).delete(
            reason='-Suppression',
            prompt=False,
            mark=True
        )
        msg = u'Cat\xe9gorie "%s" supprim\xe9e.' % (category.title(), p.title())
        results.add_result('success',msg)
        return results 

    def remove_category(self, pages, category):
        """
        Remove a category to a list of page's name.
        Work if pages list is a single pagename.
        """
        # TODO
        # Compile regex
        # Format pages arg
        if not isinstance(pages, (tuple,list)) :
            pages = (pages,)
        else:
            pages = list(set(pages))
        # Format category arg
        category = self.get_category(category)

        results = Task_Result()
        SUCCESS = u'"%s" supprim\xe9e de "%s".'
        WARNING = u'"%s" non trouv\xe9e dans "%s".'
        for p in pages :
            p = self.get_page(p)
            old_text = p.get()
            if re.search((r"\[\[%s(\|[^\]]*)?]\]" % category.title()), old_text):
                new_text = re.sub((r"\[\[%s(\|[^\]]*)?]\]" % category.title()), '', old_text)
                p.put(new_text, comment=(u'-[[%s]]' % category.title()))
                msg = SUCCESS % (category.title(), p.title())
                results.add_result('success',msg)
            else:
                msg = WARNING % (category.title(), p.title())
                results.add_result('warning',msg)
        return results 

    def move_category(self, old, new):
        """
        Move all category's Pages to an another one.
        Delete the old category.
        If new doesn't exits put the text of old one.
        """
        # TODO
        # Add lire cases
        old_cat = self.get_category(old)
        new_cat = self.get_category(new)
        pages = old_cat.articlesList()
        self.remove_category_from([ p.title() for p in pages ], old_cat.title()) 
        self.add_category([ p.title() for p in pages ], new_cat.title) 

        results = Task_Result()
        if not new_cat.exists() and old_cat.exists() :
            new_cat.put(
                newtext=old_cat.get(),
                comment=u'D\xe9placement de %s vers %s' % (old_cat.title(),new_cat.title()),
                minorEdit=False,
            )
            msg = u'D\xe9placement de %s vers %s termin\xe9.' % (old_cat.title(),new_cat.title())
            results.add_result('success',msg)
            self.delete_category(old_cat.title())
        return results

    def get_user(self, user):
        """
        Get a user by its short or long name.
        """
        if isinstance(user, userlib.User):
            pass
        elif isinstance(user, basestring):
            user = userlib.User(self.site, user)
        elif issubclass(type(user), wikipedia.Page):
            user = userlib.User(self.site, user.name())
        return user

    def sub(self, pages, pat, repl):
        """
        Make a simple string replacement on list of page.
        """
        # Format pages arg
        if not isinstance(pages, (tuple,list)) :
            pages = (pages,)
        else:
            pages = list(set(pages))

        results = Task_Result()
        for page in pages:
            page = self.get_page(page)
            old_text = page.get()
            new_text = old_text.replace(pat,repl)
            if new_text != old_text :
                page.put(
                    newtext=new_text,
                    comment=u"Subsitution de '%s' vers '%s'" % (pat,repl),
                )
                msg = u"Subsitution de '%s' vers '%s' dans '%s' avec succ\xe8s" % (pat, repl, page.title())
                results.add_result('success',msg)
            else:
                msg = u"Aucune occurence de '%s' dans '%s'" % (pat, page.title())
                results.add_result('warning',msg)
        return results

    def add_internal_link(self, pages, link, link_text=''):
        """
        Add internal link to the list of page.
        """
        # Format pages arg
        if not isinstance(pages, (tuple,list)) :
            pages = (pages,)
        else:
            pages = list(set(pages))

        link_reg = re.compile(link)
        TO_NOT_LINK = (
            re.compile(r"\[\[(?!.*\]\].*).*$"),
            re.compile(r"\{\{(?!.*\}\}.*).*$", re.S),
            re.compile(r"<nowiki>(?!.*</nowiki>.*).*$", re.S),
            re.compile(r"<pre>(?!.*</pre>.*).*$", re.S),
            re.compile(r"http://\S*$"),
        )

        results = Task_Result()
        SUCCESS = u'Hyperlien(s) "%s" ajout\xe9(s) sur "%s".'
        WARNING = u'Aucun hyperlien "%s" ajout\xe9(s) sur "%s".'
        for page in pages:
            page = self.get_page(page)
            old_text = page.get()
            # Walk in text with the key ofr step
            # Append text and add link or not
            # Words are linked only each 5 step
            new_text = ''
            count = 0
            for text in link_reg.split(old_text):
                new_text += text
                # Do not apply to last and empty split
                if text.endswith(old_text[-10:]) or not text:
                    continue
                # if text unallow links
                if False in [ False for r in TO_NOT_LINK if r.search(new_text) ]:
                    new_text += link
                else:
                    # if step counter is finished
                    if not count:
                        # Add link text or not
                        if not link_text:
                            new_text += ('[[%s]]' % link)
                        else:
                            new_text += ('[[%s|%s]]' % (link,link_test))
                        count = 5
                    # Decrement count
                    else:
                        new_text += link
                        count -= 1

            # Put page only if modified
            if new_text != old_text :
                page.put(
                    newtext=new_text,
                    comment=u"Ajout d'hyperliens pour '%s'" % link,
                )
                msg = SUCCESS % (link, page.title())
                results.add_result('success',msg)
            else:
                msg = WARNING % (link, page.title())
                results.add_result('warning',msg)
            return results

    def get_contrib(self,number=50,page=1,namespace=[]):
        """
        A generator of user contributions.
        Usable with pages and limit number.
        """
        # Check args before
        if not page:
            raise ValueError('Bad page number.')
        elif not number:
            raise ValueError('Bad limit number.')
        else:
            # Set range
            start,end = number*page-number,number*page

        # Yield only contribs in range
        precontribs = self.user.contributions(limit=end, namespace=namespace)
        for (i,(wpage,id,date,comment)) in enumerate(precontribs) :
            if i < start or i > end :
                continue
            yield (wpage,id,datetime.strptime(str(date),'%Y%m%d%H%M%S'),comment)
