import unittest

from mockito import when, unstub

import util


class TestUtil(unittest.TestCase):
    def test_consul_all_variables_set(self):
        try:
            when(util).get_docker_host().thenReturn("some_host")
            when(util).in_docker().thenReturn(True)

            consul_host = util.get_consul_host()

            self.assertEqual({'host': 'some_host', 'port': 8500}, consul_host)
        finally:
            unstub()

    def test_consul_no_variables_set(self):
        try:
            when(util).get_docker_host().thenReturn("some_host")
            when(util).in_docker().thenReturn(False)

            consul_host = util.get_consul_host()

            self.assertEqual({'host': 'some_host', 'port': 8501}, consul_host)
        finally:
            unstub()


if __name__ == '__main__':
    unittest.main()
