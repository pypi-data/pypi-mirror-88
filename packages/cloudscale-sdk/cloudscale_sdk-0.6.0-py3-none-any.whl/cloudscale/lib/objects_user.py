from . import CloudscaleMutable

class ObjectsUser(CloudscaleMutable):

    def __init__(self):
        """Ojbects User
        """
        super().__init__()
        self.resource = 'objects-users'

    def create(self, display_name: str, tags: dict = None) -> dict:
        """Creates an objects user.

        Args:
            display_name (str): The display name of the objects user.
            tags (dict, optional): The tags assigned to the objects user. Defaults to None.

        Returns:
            dict: API data response.
        """
        payload = {
            'display_name': display_name,
            'tags': tags,
        }
        return super().create(payload=payload)

    def update(self, uuid: str, display_name: str = None, tags: dict = None) -> dict:
        """Updates an objects user.

        Args:
            uuid (str): The UUID of the objects user.
            display_name (str, optional):  The display name of the objects user. Defaults to None.
            tags (dict, optional): The tags assigned to the objects user. Defaults to None.

        Returns:
            dict: API data response.
        """
        payload = {
            'display_name': display_name,
            'tags': tags,
        }
        return super().update(uuid=uuid, payload=payload)
