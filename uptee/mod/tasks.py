import os
from celery import task
from datetime import datetime
from django.contrib.auth.models import User
from settings import MEDIA_ROOT, SERVER_EXEC
from subprocess import Popen


@task()
def run_server(path, server):
    log_path = os.path.join(MEDIA_ROOT, 'logs', server.owner.username, server.mod.title)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    with open(os.path.join(log_path, '{0}_{1}_{2}.txt'.format(server.id, datetime.now().strftime("%y%m%d%H%M%S"), User.objects.make_random_password())), 'w') as f:
        p = Popen((os.path.join(path, SERVER_EXEC), '-f', 'generated.cfg'), cwd=path, stdout=f, stderr=f)
        server.pid = p.pid
        server.save()
