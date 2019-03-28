import jwt
from functools import wraps


class MissingRoleError(Exception):
    def __init__(self, message):
        self.message = message


class JWTValidator:
    def __init__(self, environment):
        self.environment = environment

    @staticmethod
    def extract_token(http_request):
        return http_request.headers.get('Authorization', '').replace('Bearer', '').strip()

    def get_roles(self, token):
        if not token:
            return []

        # Roles are encode like '<category>-<environment>:<action>' in jwt-token. Remove environment, to get '<category>:<action>'
        env_suffix = "-{}:".format(self.environment)

        role_list = jwt.decode(token, verify=False).get('scope', '').split(' ')
        filtered = list(filter(lambda x: env_suffix in x, role_list))
        mapped = list(map(lambda x: x.replace(env_suffix, ':'), filtered))
        return mapped

    def verify_role(self, request, role, api):
        roles = self.get_roles(self.extract_token(request))
        if role not in roles:
            api.abort(403, "Missing required role")
            # raise MissingRoleError("Access denied. Missing required role.")

    def require_role(self, request, role):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                roles = self.get_roles(self.extract_token(request))
                if role not in roles:
                    raise MissingRoleError("Access denied. Missing required role.")
                return f(*args, **kwargs)

            return decorated_function

        return decorator
