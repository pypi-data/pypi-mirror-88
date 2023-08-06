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

from gcloud.rest.datastore.key import Key
from gcloud.rest.datastore.value import Value


class Entity(object):
    key_kind = Key
    value_kind = Value

    def __init__(
            self, key               ,
            properties                                      = None)        :
        self.key = key
        self.properties = {k: self.value_kind.from_repr(v).value
                           for k, v in (properties or {}).items()}

    def __eq__(self, other     )        :
        if not isinstance(other, Entity):
            return False

        return bool(self.key == other.key
                    and self.properties == other.properties)

    def __repr__(self)       :
        return str(self.to_repr())

    @classmethod
    def from_repr(cls, data                )            :
        # https://cloud.google.com/datastore/docs/reference/data/rest/v1/Entity
        # "for example, an entity in Value.entity_value may have no key"
        if 'key' in data:
            key                = cls.key_kind.from_repr(data['key'])
        else:
            key = None
        return cls(key, data.get('properties'))

    def to_repr(self)                  :
        return {
            'key': self.key.to_repr() if self.key else None,
            'properties': {k: self.value_kind(v).to_repr()
                           for k, v in self.properties.items()},
        }


class EntityResult(object):
    entity_kind = Entity

    def __init__(self, entity        , version      = '',
                 cursor      = '')        :
        self.entity = entity
        self.version = version
        self.cursor = cursor

    def __eq__(self, other     )        :
        if not isinstance(other, EntityResult):
            return False

        return bool(self.entity == other.entity
                    and self.version == other.version
                    and self.cursor == self.cursor)

    def __repr__(self)       :
        return str(self.to_repr())

    @classmethod
    def from_repr(cls, data                )                  :
        return cls(cls.entity_kind.from_repr(data['entity']),
                   data.get('version', ''),
                   data.get('cursor', ''))

    def to_repr(self)                  :
        data                 = {
            'entity': self.entity.to_repr(),
        }
        if self.version:
            data['version'] = self.version
        if self.cursor:
            data['cursor'] = self.cursor

        return data
