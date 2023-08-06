from asencis.client import AsencisAPIClient

from asencis.mixins import ListAPIMixin

class Domain(
    AsencisAPIClient,
    ListAPIMixin
):

    OBJECT_NAME = "Domain"

    def __init__(self):
        """
        Initialise the Domain API Object
        """
        super(Domain, self).__init__(
            realm='domains',
        )
