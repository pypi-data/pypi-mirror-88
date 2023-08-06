import os

from PyQt5.QtWidgets import QApplication

from .. import layout
from ..scope import NDScope


if __name__ == '__main__':
    os.environ['NDSSERVER'] = 'fake'

    channels = ['FOOBAR']

    template, ltype = layout.template_from_chans(channels)

    app = QApplication([])
    scope = NDScope(template['plots'])
    scope.show()
    scope.fetch(t0=1234, window=(-1, 1))

    scope.export('testtest.png')
    
    # import IPython
    # IPython.embed()
