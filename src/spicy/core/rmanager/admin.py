from django.conf import settings 

from spicy.core.service import api

from spicy.core.siteskin.decorators import render_to
from spicy.core.profile.decorators import is_staff

import re
from datetime import datetime, timedelta

@is_staff#(required_perms=('',))
@render_to('rmanager/admin/versions.html')
def versions(request):
    return {'versions': api.register.get_list()}

@is_staff#(required_perms=('',))
@render_to('rmanager/admin/db_logger.html')
def db_logger(request):
    return {'versions': api.register.get_list()}



@is_staff
@render_to('rmanager/admin/memcache.html')
def memcache(request):
    class Stats:
        pass
    
    message = ''
    stats = None
    hit_rate = ''
    
    try:
        import memcache
    except ImportError:
        message = '"memcache" python module is unavailable, install it please. '
    
    # get first memcached URI
    m = re.match(
        "memcached://([.\w]+:\d+)", settings.CACHE_BACKEND
        )
    if not m:
        message = 'Can not locate memcached configuration in the settings.py file.'
    else:
        host = memcache._Host(m.group(1))
        host.connect()
        try:
            host.send_cmd("stats")
        except:
            message = 'Memcached server is unavailable. %s ' % settings.CACHE_BACKEND

    if not message:
        stats = Stats()
        while 1:
            line = host.readline().split(None, 2)
            if line[0] == "END":
                break
            stat, key, value = line
            try:
                # convert to native type, if possible
                value = int(value)
                if key == "uptime":
                    value = timedelta(seconds=value)
                elif key == "time":
                    value = datetime.fromtimestamp(value)
            except ValueError:
                pass
            setattr(stats, key, value)
        hit_rate = 100 * stats.get_hits / stats.cmd_get
        host.close_socket()
            
    return {
        'message': message,
        'stats': stats,
        'hit_rate': hit_rate,
        'time': datetime.now(), # server time
         }
