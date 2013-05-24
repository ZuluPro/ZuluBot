from celery.task import task
from core.handlers import wiki_handler

@task(name='move_pages')
def async_move_pages(*args, **kwargs):
    w = wiki_handler()
    return w.move_pages(*args, **kwargs)

@task(name='add_category')
def async_add_category(*args, **kwargs):
    w = wiki_handler()
    return w.add_category(*args, **kwargs)

@task(name='move_category')
def async_move_category(*args, **kwargs):
    w = wiki_handler()
    return w.move_category(*args, **kwargs)

@task(name='remove_category')
def async_remove_category(*args, **kwargs):
    w = wiki_handler()
    return w.remove_category(*args, **kwargs)

@task(name='add_internal_link')
def async_add_internal_link(*args, **kwargs):
    w = wiki_handler()
    return w.add_internal_link(*args, **kwargs)

@task(name='sub')
def async_sub(*args, **kwargs):
    w = wiki_handler()
    return w.sub(*args, **kwargs)

@task(name='test')
def test(i,j=1):
    return i+j
