from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTests(TestCase):
    """
    Management command: helper command that allows us to wait for de db to be
    available before continuing and running other commands.
    """

    def test_wait_for_db_ready(self):
        """
        Tests What happens when we call our command and the db is already available.
        Test waiting for db when db is available
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts):
        """
        Cheks that the wait_for_db command will try the db 5 and on the 6th
        it will be succesfull and we will contintue
        Test waiting for db
        """

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
