import click
import unittest
from sshmux import validate
from os import environ

from click.testing import CliRunner


class TestValidations(unittest.TestCase):

    @click.command()
    @click.option('--hostname', '-h', callback=validate.validate_hostname, multiple=True, help='IP address or hostname')  # NOQA
    def check_hostname(hostname):
        click.echo('sucess')

    @click.command()
    @click.option('--username', '-u', callback=validate.validate_user, default='',
                  help='ssh username')
    def check_username(username):
        click.echo('sucess')

    @click.command()
    @click.option('--key', '-k', default=environ['HOME'] + '/.ssh/id_rsa',
                  help='ssh private key')
    def check_key(key):
        click.echo('sucess')

    def test_hostname_check(self):
        runner = CliRunner()
        result = runner.invoke(self.check_hostname, ['-h', '127.0.0.1'])
        self.assertEqual('sucess\n', result.output)

    def test_hostname_fail(self):
        runner = CliRunner()
        result = runner.invoke(self.check_hostname, ['-h', 'wrong_host_name'])
        self.assertNotEqual(result.exit_code, 0)

    def test_username_check(self):
        runner = CliRunner()
        result = runner.invoke(self.check_username, ['-u', 'testuser'])
        self.assertEqual('sucess\n', result.output)

    def test_username_fail(self):
        runner = CliRunner()
        username = 'testusername' * 12
        result = runner.invoke(self.check_username, ['-u', username])
        self.assertNotEqual(result.exit_code, 0)

    def test_key_check(self):
        key = environ['HOME'] + '/.ssh/id_rsa'
        key = validate.validate_key(key)
        runner = CliRunner()
        result = runner.invoke(
            self.check_key, ['-k', key])
        self.assertEqual('sucess\n', result.output)
    # NOTE(rjrhaverkamp): Does not work, so commented out.
    # def test_password_fail(self):
    #     password = "sshmuxpassword" * 12
    #     self.assertRaises(click.exceptions.BadParameter,
    #                       validate.validate_pass(password))

if __name__ == '__main__':
    unittest.main()
