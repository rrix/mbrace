from celery import task

@task
def update_friends(user):
    import pdb
    pdb.set_trace()
