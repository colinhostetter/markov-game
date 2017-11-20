from collections import namedtuple
from unittest import TestCase
from unittest.mock import MagicMock

from app import game_manager


Emission = namedtuple(
    typename='Emission',
    field_names=['name', 'data', 'room']
)


class BaseTestCase(TestCase):
    def setUp(self):
        self.mock_socketio = MagicMock()
        game_manager.init_game_manager(self.mock_socketio)

    def tearDown(self):
        game_manager._game_registry = {}

    @property
    def emissions(self):
        return [
            Emission(name=i[0][0], data=i[0][1], room=i[1].get('room'))
            for i in self.mock_socketio.emit.call_args_list
        ]
