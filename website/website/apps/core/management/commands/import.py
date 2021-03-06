# -*- coding: utf-8 -*-
import os
import sys
import reversion
from optparse import make_option
from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<filename ../path/to/file>'
    help = 'Imports the given data file'
    output_transaction = True
    option_list = BaseCommand.option_list + (
        make_option('--run',
            action='store_true',
            dest='run',
            default=False,
            help='Run'),
    )
    
    DATA_ROOT = os.path.join(os.path.split(settings.SITE_ROOT)[0], 'data')
    
    def list_datafiles(self):
        files = sorted([_ for _ in os.listdir(self.DATA_ROOT)
                                if os.path.splitext(_)[1] == '.py'
                                and _.startswith("0")])
        for filename in files:
            print(" - {0}".format(os.path.join('data', filename)))
        
    def load(self, filename, dryrun=True):
        directory, module_name = os.path.split(filename)
        module_name = os.path.splitext(module_name)[0]
        sys.path.insert(0, directory)
        
        try:
            ac = transaction.get_autocommit()
            transaction.set_autocommit(False)
            with reversion.create_revision():
                try:
                    __import__(module_name)
                except Exception as e:
                    raise ImportError(u"Failed to Import - Exception: %s" % e)
        except ImportError, e:
            raise
        finally:
            if dryrun:
                print("\n>>> ROLLBACK\n")
                transaction.rollback()
            else:
                print("\n<<< COMMIT\n")
                transaction.commit()
            transaction.set_autocommit(ac)
    
    def handle(self, *args, **options):
        # set some environment variables;
        os.environ['IMPORTER_SITEROOT'] = settings.SITE_ROOT
        os.environ['IMPORTER_DATAROOT'] = self.DATA_ROOT
        
        # handle no args
        if len(args) == 0:
            print("Listing files in {0}:".format(self.DATA_ROOT))
            self.list_datafiles()
            return
        elif len(args) > 1:
            raise ValueError("Expecting one argument only!")
        
        filename = args[0]
        # set some environment variables;
        os.environ['IMPORTER_FILENAME'] = filename
        filename = filename.strip()
        if not os.path.isfile(filename):
            raise IOError('Invalid Filename %s' % filename)
        
        filehead, fileext = os.path.splitext(filename)
        
        if fileext != '.py':
            raise IOError('Unable to import a %s file' % fileext)
        
        self.stdout.write('Importing "%s"\n' % filename)
        
        if 'run' in options and options['run']:
            self.load(filename, dryrun=False)
        else:
            self.load(filename, dryrun=True)
            sys.stdout.write(
                "Dry-run complete. Use --run to save changes. Rolling back."
            )
        self.stdout.flush()
            
