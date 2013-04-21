from django.contrib import messages

def make_messages(request, results):
    """
    Create messages from wiki_handler's result.
    """
    # Format results arg
    if not isinstance(results, (tuple,list)) :
        results = (results,)

    # Match resutlt type with messages.TAG
    TAGS = dict([ (j,i) for i,j in messages.DEFAULT_TAGS.items() ])

    grouped_results = {'success':'','warning':'','error':''}
    for task_r in results:
        for s in ('success','warning','error'):
            for p,r in task_r[s]:
                if r :
                    grouped_results[s] += ('<li>%s</li>' % r )
            messages.add_message(request, TAGS[s], grouped_results[s])
    return messages.get_messages(request)
