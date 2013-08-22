import copy
from zope.interface import implements
from plone.memoize import ram
from plone.supermodel.model import finalizeSchemas, SchemaClass

from .schemaeditor import SCHEMATA_KEY, get_ttw_edited_schema, model_key
from .userdataschema import (IUserDataSchemaProvider, IUserDataZ3CSchema,
                             IRegisterSchemaProvider)
from plone.app.users.browser.z3cregister import IZ3CRegisterSchema


class BaseMemberScheamProvider(object):
    """Base mixin class for members schema providers
    """

    @ram.cache(lambda *args, **kw: "%s-%s" % (model_key(), args))
    def getSchema(self):
        """
        """
        def copySchemaAttrs(schema):
            return dict([(a, copy.deepcopy(schema[a])) for a in schema])

        attrs = copySchemaAttrs(self.baseSchema)
        ttwschema = get_ttw_edited_schema()
        if ttwschema:
            attrs.update(copySchemaAttrs(ttwschema))
        schema = SchemaClass(SCHEMATA_KEY,
                             bases=(self.baseSchema,),
                             attrs=attrs)
        finalizeSchemas(schema)
        return schema


class UserDataSchemaProvider(BaseMemberScheamProvider):
    implements(IUserDataSchemaProvider)
    baseSchema = IUserDataZ3CSchema


class RegisterSchemaProvider(BaseMemberScheamProvider):
    implements(IRegisterSchemaProvider)
    baseSchema = IZ3CRegisterSchema

