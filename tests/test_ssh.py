import unittest
from os import environ

from sshmux import ssh, errors


class TestSSH(unittest.TestCase):

    def test_ssh_output(self):
        output = ssh.ssh(environ['sshmux_test_host'], 'echo "hello"', environ[
                         'sshmux_test_user'], environ['sshmux_test_key'])
        self.assertEqual(output, 'hello\n')

    def test_wrong_cmd(self):
        host = environ['sshmux_test_host']
        user = environ['sshmux_test_user']
        key = environ['sshmux_test_key']
        self.assertRaises(errors.MuxError, ssh.ssh, host,
                          'does_not_exist', user, key)

    def test_background_run(self):
        output = ssh.ssh(environ['sshmux_test_host'], 'echo "hello"&', environ['sshmux_test_user'], environ['sshmux_test_key'], bg_run=True) # NOQA
        self.assertEqual(output, 'hello\n')


if __name__ == '__main__':
    unittest.main()
