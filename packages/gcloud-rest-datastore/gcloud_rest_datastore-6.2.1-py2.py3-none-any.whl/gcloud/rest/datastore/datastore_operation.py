from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
from builtins import object
from typing import Any
from typing import Dict
from typing import Optional


class DatastoreOperation(object):
    def __init__(self, name     , done      ,
                 metadata                           = None,
                 error                           = None,
                 response                           = None)        :
        self.name = name
        self.done = done

        self.metadata = metadata
        self.error = error
        self.response = response

    def __repr__(self)       :
        return str(self.to_repr())

    @classmethod
    def from_repr(cls, data                )                        :
        return cls(data['name'], data.get('done', False), data.get('metadata'),
                   data.get('error'), data.get('response'))

    def to_repr(self)                  :
        return {
            'done': self.done,
            'error': self.error,
            'metadata': self.metadata,
            'name': self.name,
            'response': self.response,
        }
