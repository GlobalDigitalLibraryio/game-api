import unittest
from unittest.mock import Mock, patch

from gdl.jwt_validate import JWTValidator, MissingRoleError


class JWTValidatorTestCase(unittest.TestCase):

    def setUp(self):
        self.jwt_validator = JWTValidator('environment')

    def test_that_empty_auth_header_returns_none_for_extract_token(self):
        request = Mock()
        request.headers = {}
        token = JWTValidator.extract_token(request)
        self.assertEqual('', token)
        self.assertFalse(token)

    def test_that_token_is_extracted_for_valid_bearer_token(self):
        request = Mock()
        request.headers = {'Authorization': 'Bearer this-is-the-token-string'}
        self.assertEqual('this-is-the-token-string', JWTValidator.extract_token(request))

    def test_that_empty_list_is_returned_for_empty_token(self):
        self.assertListEqual([], self.jwt_validator.get_roles(''))

    @patch('gdl.jwt_validate.jwt')
    def test_that_empty_list_is_returned_for_valid_token_without_scope(self, jwt_mock):
        jwt_mock.decode.return_value = {}
        self.assertListEqual([], self.jwt_validator.get_roles('this-is-a-token'))

    @patch('gdl.jwt_validate.jwt')
    def test_that_roles_for_different_environment_are_not_returned(self, jwt_mock):
        jwt_mock.decode.return_value = {'scope': 'games-environment:write games-environment:write'}
        self.assertListEqual([], JWTValidator(environment='other').get_roles('this-is-a-token'))

    @patch('gdl.jwt_validate.jwt')
    def test_that_roles_for_correct_environment_are_returned(self, jwt_mock):
        jwt_mock.decode.return_value = {'scope': 'games-environment:something games-other:dostuff games-prod:some-role'}
        self.assertListEqual(['games:some-role'], JWTValidator(environment='prod').get_roles('this-is-a-token'))

    @patch('gdl.jwt_validate.JWTValidator.get_roles')
    def test_that_MissingRoleError_is_raised_for_missing_role(self, get_roles_mock):
        def f(): pass
        get_roles_mock.return_value = ['games:actual-role']
        self.assertRaises(MissingRoleError, JWTValidator('prod').require_role(Mock(), role='games:required-role')(f))

    @patch('gdl.jwt_validate.JWTValidator.get_roles')
    def test_that_MissingRoleError_is_not_raised_when_role_valid(self, get_roles_mock):
        def f(): pass
        get_roles_mock.return_value = ['games:actual-role']
        JWTValidator('prod').require_role(Mock(), role='games:actual-role')(f)()
