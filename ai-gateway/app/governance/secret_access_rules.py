from copy import deepcopy


class SecretAccessRules:
    """
    Enterprise Secret Access Rules

    Controls access to secrets such as API keys,
    passwords, tokens and certificates.

    Features

    ✓ Register Secrets
    ✓ Role-Based Access
    ✓ User-Based Access
    ✓ Read / Write Permissions
    ✓ Secret Validation
    ✓ Statistics
    ✓ Export

    Used by

    - Governance Manager
    - Policy Engine
    - RBAC
    - Secret Manager
    - Vault Integration
    """

    READ = "read"
    WRITE = "write"

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Register Secret
    # -------------------------------------------------

    def register(
        self,
        secret,
        roles=None,
        users=None,
        permissions=None,
    ):

        self._secrets[secret] = {

            "roles": set(roles or []),

            "users": set(users or []),

            "permissions": set(
                permissions or [self.READ]
            ),

        }

        return True

    # -------------------------------------------------
    # Remove Secret
    # -------------------------------------------------

    def remove(
        self,
        secret,
    ):

        return self._secrets.pop(
            secret,
            None,
        ) is not None

    # -------------------------------------------------
    # Allow Role
    # -------------------------------------------------

    def allow_role(
        self,
        secret,
        role,
    ):

        if secret not in self._secrets:

            self.register(secret)

        self._secrets[secret]["roles"].add(role)

        return True

    # -------------------------------------------------
    # Deny Role
    # -------------------------------------------------

    def deny_role(
        self,
        secret,
        role,
    ):

        if secret not in self._secrets:
            return False

        self._secrets[secret]["roles"].discard(role)

        return True

    # -------------------------------------------------
    # Allow User
    # -------------------------------------------------

    def allow_user(
        self,
        secret,
        user,
    ):

        if secret not in self._secrets:

            self.register(secret)

        self._secrets[secret]["users"].add(user)

        return True

    # -------------------------------------------------
    # Deny User
    # -------------------------------------------------

    def deny_user(
        self,
        secret,
        user,
    ):

        if secret not in self._secrets:
            return False

        self._secrets[secret]["users"].discard(user)

        return True

    # -------------------------------------------------
    # Grant Permission
    # -------------------------------------------------

    def grant(
        self,
        secret,
        permission,
    ):

        if secret not in self._secrets:

            self.register(secret)

        self._secrets[secret]["permissions"].add(
            permission
        )

        return True

    # -------------------------------------------------
    # Revoke Permission
    # -------------------------------------------------

    def revoke(
        self,
        secret,
        permission,
    ):

        if secret not in self._secrets:
            return False

        self._secrets[secret]["permissions"].discard(
            permission
        )

        return True

    # -------------------------------------------------
    # Check Access
    # -------------------------------------------------

    def allowed(
        self,
        secret,
        *,
        permission=READ,
        role=None,
        user=None,
    ):

        if secret not in self._secrets:
            return False

        rule = self._secrets[secret]

        #
        # Permission
        #

        if permission not in rule["permissions"]:
            return False

        #
        # Explicit User
        #

        if user is not None:

            if user in rule["users"]:
                return True

        #
        # Role
        #

        if role is not None:

            if role in rule["roles"]:
                return True

        return False

    # -------------------------------------------------
    # Exists
    # -------------------------------------------------

    def exists(
        self,
        secret,
    ):

        return secret in self._secrets

    # -------------------------------------------------
    # Roles
    # -------------------------------------------------

    def roles(
        self,
        secret,
    ):

        if secret not in self._secrets:
            return []

        return sorted(

            self._secrets[secret]["roles"]

        )

    # -------------------------------------------------
    # Users
    # -------------------------------------------------

    def users(
        self,
        secret,
    ):

        if secret not in self._secrets:
            return []

        return sorted(

            self._secrets[secret]["users"]

        )

    # -------------------------------------------------
    # Permissions
    # -------------------------------------------------

    def permissions(
        self,
        secret,
    ):

        if secret not in self._secrets:
            return []

        return sorted(

            self._secrets[secret]["permissions"]

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "secrets": len(
                self._secrets
            ),

            "role_rules": sum(
                len(item["roles"])
                for item in self._secrets.values()
            ),

            "user_rules": sum(
                len(item["users"])
                for item in self._secrets.values()
            ),

            "permission_rules": sum(
                len(item["permissions"])
                for item in self._secrets.values()
            ),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            secret: {

                "roles": sorted(
                    values["roles"]
                ),

                "users": sorted(
                    values["users"]
                ),

                "permissions": sorted(
                    values["permissions"]
                ),

            }

            for secret, values

            in self._secrets.items()

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._secrets = {}

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return SecretAccessRules()