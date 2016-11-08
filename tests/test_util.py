# -*- coding: utf-8 -*-
import os
import unittest

from mockito import *

from typeahead import util


class TestUtil(unittest.TestCase):
    def test_consul_all_variables_set(self):
        try:
            when(util)._get_environment().thenReturn(
                {'CONSUL_HOST', "some_host:1234"},
                {'CONSUL_HOST_2', "second_host:1234"},
                {'CONSUL_HOST_3', "third_host:3214"})

            consul_hosts = util.get_consul_hosts()

            self.assertEqual([{'host': 'some_host', 'port': '1234'},
                              {'host': 'second_host', 'port': '1234'},
                              {'host': 'third_host', 'port': '3214'}],
                             consul_hosts)
        finally:
            unstub()

    def test_consul_no_variables_set(self):
        try:
            when(os).getenv('CONSUL_HOST',
                            '127.0.0.1:8500').thenReturn("default_host:1234")
            when(os).getenv('CONSUL_HOST_2', None).thenReturn(None)
            when(os).getenv('CONSUL_HOST_3', None).thenReturn(None)

            consul_hosts = util.get_consul_hosts()

            self.assertEqual([
                {'host': 'default_host', 'port': '1234'}], consul_hosts)
        finally:
            unstub()


if __name__ == '__main__':
    unittest.main()
