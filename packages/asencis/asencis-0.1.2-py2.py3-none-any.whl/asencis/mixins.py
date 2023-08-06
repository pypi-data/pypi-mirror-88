from asencis.exceptions import (
    UUIDValidationException,
    RealmResourceSpecificationException
)

from asencis.utils import (
    validate_uuid4
)

class ListAPIMixin(object):
    def list(self, *args, **kwargs):
        # We first need to check if either of the realm or resource have been specified:
        if not hasattr(self, 'realm') and not hasattr(self, 'resource'):
            # If neither have been specified, raise a RealmResourceSpecification error:
            raise RealmResourceSpecificationException("The realm and/or resource lookup needs to be specified")

        # Else, we can construct the resource "path" for listing:
        if self.resource is not None:
            path='{}/{}'.format(self.realm, self.resource)
        else:
            path='{}'.format(self.realm)

        # Perform call to the _perform_request method:
        return self._perform_request(action="GET", path=path, data=None, query=None, headers=None)

class RetrieveAPIMixin(object):
    def retrieve(self, uuid=None, **kwargs):
        # First we need to check if the uuid has been specified and passes validation:
        if uuid is None or not validate_uuid4(uuid):
            raise UUIDValidationException("Please provide a valid UUID4 value")

        # We first need to check if either of the realm or resource have been specified:
        if not hasattr(self, 'realm') and not hasattr(self, 'resource'):
            # If neither have been specified, raise a RealmResourceSpecification error:
            raise RealmResourceSpecificationException("The realm and/or resource lookup needs to be specified")

        # Else, we can construct the resource "path" for retrieval:
        if self.resource is not None:
            path='{}/{}/{}'.format(self.realm, self.resource, uuid)
        else:
            path='{}/{}'.format(self.realm, uuid)

        return self._perform_request(action="GET", path=path, data=None, query=None, headers=None)

class SearchAPIMixin(object):
    def search(self, query, **kwargs):
        print("Searching the API for Results")
        return None
