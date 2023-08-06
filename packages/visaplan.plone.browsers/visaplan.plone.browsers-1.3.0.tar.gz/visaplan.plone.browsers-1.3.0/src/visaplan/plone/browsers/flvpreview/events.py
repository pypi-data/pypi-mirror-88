# Python compatibility:
from __future__ import absolute_import

# Standard library:
import glob
import os
from os import unlink


def delete(self,event):
    """ """
    context=event.object
    storagepath=context.getBrowser('flvpreview')._storage_path()

    if hasattr(context,'UID'):
        for path in glob.glob(storagepath+context.UID()+'_flash_file_*'):
            if os.path.exists(path):
                unlink(path)