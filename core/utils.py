from django.contrib import messages

def make_messages(request, results):
    """
    Create messages from wiki_handler's result.
    """
    TAGS = dict([ (j,i) for i,j in messages.DEFAULT_TAGS.items() ])
    for s in ('success','warning','error'):
        for r in results[s]:
            messages.add_message(request, TAGS[s], r[1])
    return messages.get_messages(request)
