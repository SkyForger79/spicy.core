from optparse import make_option
try:
    from django.core.management.base import BaseCommand, CommandError
except ImportError:
    BaseCommand = object
    class CommandError(Exception):
        pass

#from django.core.exceptions import ImproperlyConfigured

from django.conf import settings

import sys, os
from datetime import datetime


TRUNK_URL = 'https://svn.local.lh/django-projects/trunk/django-example/'
TAG_URL = 'https://svn.local.lh/django-projects/tags/django-example/'

class CommandFailed(OSError):
    pass

class Command(BaseCommand):
    version = None
    app = ''

    option_list = (
        make_option(
            '--init', '-i', default=False, action="store_true",
            help='Init application release management additional scrips.'),
        make_option(
            '--commit', '-c', dest='commit', default=False, action="store",
            help='Commit latests changes, update CHANGELOG and VERSION files.'),
        make_option('--tag', '-t', default=False, action="store_true", help='Make revision tag.'),
        make_option('--release', '-r', default=False, action="store_true", help='Make tag and tallbar release.'),
        make_option('--info', '-I', default=False, action="store_true", help='Show version info.')
        ) + BaseCommand.option_list

    if '--verbosity' not in [opt.get_opt_string() for opt in BaseCommand.option_list]:
        option_list += (
            make_option('--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
        )

    help = 'Release management automatization tools. Use it for multi apps project or define specified  application name instead.'
    args = '[appname] [[--init] [--commit changeset-comment|zero] | [--tag] | [--release] | [--info]]'
    def handle(self, app='', *args, **options):
        self.app = app
        self.verbosity = int(options['verbosity'])

        if len(args) > 0:
            raise CommandError('Please read usage help.')
        
        if app:
            if not app in settings.INSTALLED_APPS:
                raise CommandError(
                    'App. "%s" is not installed, check your settings.py'%self.app)

        self.app_path = './' + settings.APP_SOURCE_PATH + (self.app and (self.app + '/'))
        self.app_mod = self.app + str(self.app and '.')
        try:
            self.version = self._import_version()
        except ImportError, exc:
            if not options.get('init', True):
                raise CommandError(
                    '%s is not under release manager control, init it first.'%(self.app or 'Project'))

        if options.get('init', True):
            if self.version is None:
                self._touch_version(
                    ["version = Version(__name__[:__name__.rfind('.')], 0, 0, 0)\n",
                     'CHANGES = []\n'])
            else:
                raise CommandError(
                    '%s is already under release manager control.'%(self.app or 'Project'))
        if options.get('commit', True):
            return self.commit(options['commit'])
        if options.get('tag', True):
            return self.tag()
        if options.get('release', True):
            return self.release()
        if options.get('info', True):
            print self.version.version.short()
            return
        
        if not options.get('init', True):
            raise CommandError('Define command line correctly, please.')

    def commit(self, comment):
        if not comment in self.version.CHANGES:
            self.version.CHANGES.append(comment)
            self._update_version()
            self.sh("%s ci -m '%s'"%(settings.REPOSITORY_TYPE, comment))
        else:
            raise CommandError(
                'Nothing to change, "%s" is already in the %s CHANGELOG file'
                %(comment, self.app or 'project'))

    def _import_version(self):
        return __import__(self.app_mod + '_version', {}, {}, [''])

    def _touch_version(self, code_lines):
        fd = open(self.app_path + '_version.py', 'a')
        fd.writelines(
            ['# This is auto-generated file.\n',
             'from rmanager.versions import Version\n',] + code_lines)
        fd.close()
        self.version = self._import_version()

    def _update_version(self):
        self.sh('rm %s_version.py*'%self.app_path)
        version = self.version.version
        self._touch_version(
            ["version = Version(__name__[:__name__.rfind('.')], %s, %s, %s)\n"
             %(version.major, version.minor, version.micro),
             'CHANGES = [%s]\n'%',\n'.join(
                    ["'%s'"%msg for msg in self.version.CHANGES])])

    def sh(self, command):
        if self.verbosity == 0:
            command = "%s > /dev/null" % command
        else:
            print "--$", command
            if self.verbosity == 2:
                if raw_input("run ?? ").startswith('n'):
                    return
        
        if os.system(command) != 0:
            raise CommandFailed(command)

    def release(self):
        raise NotImplemented

    def tag(self):
        raise NotImplemented
         
def tag():
    version = _get_version_check_point()
    version.version.increase()
    
    date = datetime.now().isoformat().split('T')[0]
    try:
        fd = open('topfiles/CHANGELOG')
        old_changes = fd.readlines()
    except:
        old_changes = []
    
    is_duplicated = False
    for text in old_changes:
        if text.startswith(version.version.short()):
            is_duplicated = True
            start = old_changes.index(text) + 2
            stop = len(old_changes)
            count = 0
            for txt in old_changes[start:]:
                if txt == '\n':
                    break
                count += 1
            if count:
                stop = start + count
            for change in version.CHANGES:
                ch_pattern = '    - %s\n'%change
                if not ch_pattern in old_changes[start:stop]:
                    old_changes.insert(start, ch_pattern)
            old_changes[start-2] = '%s (%s)\n'%(version.version.short(), date)

    if is_duplicated:
        new_changes = old_changes
    else:
        new_changes = ['%s (%s)\n'%(version.version.short(), date),
                       '==============================\n']
        for change in version.CHANGES:
            new_changes.append('    - %s\n'%change)
        new_changes = new_changes + ['\n'] + old_changes
        
    sh('rm topfiles/CHANGELOG')
    fd = open('topfiles/CHANGELOG', 'a')
    fd.writelines(new_changes)
    fd.close()

    if os.path.exists('topfiles/VERSION'):
        sh('rm topfiles/VERSION')
    fd = open('topfiles/VERSION', 'a')
    fd.write(version.version.short()+'\n')
    fd.close()
    
    _update_version(version.version, [])
    to_url = TAG_URL + version.version.base()
    sh("svn ci -m 'Make TAG %s'"%version.version.short())
    sh("svn cp %s %s -m 'Make TAG %s'"%(TRUNK_URL, to_url, version.version.short()),
       prompt=True)
    
