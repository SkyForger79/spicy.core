from threading import local

SITE_THREAD_INFO = local()

class SiteIDHook:
    def __init__(self):
        # default value
        SITE_THREAD_INFO.SITE_ID = 1

    def __int__(self):        
        return SITE_THREAD_INFO.SITE_ID

    def __hash__(self):        
        return SITE_THREAD_INFO.SITE_ID


class SiteTemplateHook:
    def __init__(self, default_tmpl_dir, *args):
        self.default = default_tmpl_dir
        self.dirs = args

        #lobal SITE_THREAD_INFO
        SITE_THREAD_INFO.TEMPLATE_DIRS = (self.default,) + self.dirs

    def __getitem__(self, index):
        #print '@@', dir(SITE_THREAD_INFO.SITE_ID)
        return SITE_THREAD_INFO.TEMPLATE_DIRS[index]

    def __tuple__(self):
        return SITE_THREAD_INFO.TEMPLATE_DIRS

