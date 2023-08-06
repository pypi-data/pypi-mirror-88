from asencis.client import AsencisAPIClient

from asencis.mixins import ListAPIMixin

class Quantity(
    AsencisAPIClient,
    ListAPIMixin
):

    OBJECT_NAME = "Quantity"

    def __init__(self):
        """
        Initialise the Quantity API Object
        """
        super(Quantity, self).__init__(
            realm='measurements',
            resource='quantities'
        )
