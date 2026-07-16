from copy import deepcopy


class RBAC:
    """
    Enterprise Role-Based Access Control (RBAC)

    Controls access based on assigned user roles.

    Features

    ✓ User Role Assignment
    ✓ Role Permissions
    ✓ Permission Checks
    ✓ Role Management
    ✓ Statistics
    ✓ Export

    Used by

    - Policy Engine
    - Governance Manager
    - Tool Permissions
    - Secret Access Rules
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Create Role
    # -------------------------------------------------

    def add_role(
        self,
        role,
        permissions=None,
    ):

        self._roles[role] = set(
            permissions or []
        )

        return True

    # -------------------------------------------------
    # Remove Role
    # -------------------------------------------------

    def remove_role(
        self,
        role,
    ):

        if role not in self._roles:
            return False

        del self._roles[role]

        for user in list(self._users):

            if self._users[user] == role:

                del self._users[user]

        return True

    # -------------------------------------------------
    # Assign User
    # -------------------------------------------------

    def assign(
        self,
        user,
        role,
    ):

        if role not in self._roles:
            return False

        self._users[user] = role

        return True

    # -------------------------------------------------
    # Revoke User
    # -------------------------------------------------

    def revoke(
        self,
        user,
    ):

        return self._users.pop(
            user,
            None,
        ) is not None

    # -------------------------------------------------
    # Grant Permission
    # -------------------------------------------------

    def grant(
        self,
        role,
        permission,
    ):

        if role not in self._roles:
            return False

        self._roles[role].add(
            permission
        )

        return True

    # -------------------------------------------------
    # Revoke Permission
    # -------------------------------------------------

    def revoke_permission(
        self,
        role,
        permission,
    ):

        if role not in self._roles:
            return False

        self._roles[role].discard(
            permission
        )

        return True

    # -------------------------------------------------
    # Check Permission
    # -------------------------------------------------

    def allowed(
        self,
        user,
        permission,
    ):

        role = self._users.get(
            user
        )

        if role is None:
            return False

        return permission in self._roles.get(
            role,
            set(),
        )

    # -------------------------------------------------
    # User Role
    # -------------------------------------------------

    def role(
        self,
        user,
    ):

        return self._users.get(
            user
        )

    # -------------------------------------------------
    # User Permissions
    # -------------------------------------------------

    def permissions(
        self,
        user,
    ):

        role = self.role(user)

        if role is None:
            return []

        return sorted(

            self._roles.get(
                role,
                set(),
            )

        )

    # -------------------------------------------------
    # Roles
    # -------------------------------------------------

    def roles(
        self,
    ):

        return sorted(

            self._roles.keys()

        )

    # -------------------------------------------------
    # Users
    # -------------------------------------------------

    def users(
        self,
    ):

        return deepcopy(
            self._users
        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "roles": len(
                self._roles
            ),

            "users": len(
                self._users
            ),

            "permissions": sum(

                len(p)

                for p in self._roles.values()

            ),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            "roles": {

                role: sorted(
                    permissions
                )

                for role, permissions

                in self._roles.items()

            },

            "users": deepcopy(
                self._users
            ),

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._roles = {}

        self._users = {}

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return RBAC()