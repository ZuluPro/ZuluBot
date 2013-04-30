from celery import task
from zulubot.handlers import wiki_handler
w = wiki_handler()

@task()
def async_move_pages(*args, **kwargs):
    return w.move_pages(*args, **kwargs)

@task()
def async_add_category(*args, **kwargs):
    return w.add_category(*args, **kwargs)

@task()
def async_move_category(*args, **kwargs):
    return w.move_category(*args, **kwargs)

@task()
def async_remove_category_from(*args, **kwargs):
    return w.remove_category_from(*args, **kwargs)

@task()
def test(i,j=1):
    return i+j
