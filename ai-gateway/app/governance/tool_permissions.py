from copy import deepcopy


class ToolPermissions:
    """
    Enterprise Tool Permissions

    Controls which users or roles may execute
    specific MCP tools.

    Features

    ✓ Register Tool Permissions
    ✓ Allow / Deny Roles
    ✓ Allow / Deny Users
    ✓ Permission Validation
    ✓ Runtime Statistics
    ✓ Export

    Used by

    - Policy Engine
    - RBAC
    - Governance Manager
    - Agent Service
    """

    def __init__(self):

        self.clear()

    # -------------------------------------------------
    # Register Tool
    # -------------------------------------------------

    def register(
        self,
        tool,
        roles=None,
        users=None,
    ):

        self._tools[tool] = {

            "roles": set(roles or []),

            "users": set(users or []),

        }

        return True

    # -------------------------------------------------
    # Remove Tool
    # -------------------------------------------------

    def remove(
        self,
        tool,
    ):

        return self._tools.pop(
            tool,
            None,
        ) is not None

    # -------------------------------------------------
    # Allow Role
    # -------------------------------------------------

    def allow_role(
        self,
        tool,
        role,
    ):

        if tool not in self._tools:

            self.register(tool)

        self._tools[tool]["roles"].add(role)

        return True

    # -------------------------------------------------
    # Deny Role
    # -------------------------------------------------

    def deny_role(
        self,
        tool,
        role,
    ):

        if tool not in self._tools:
            return False

        self._tools[tool]["roles"].discard(role)

        return True

    # -------------------------------------------------
    # Allow User
    # -------------------------------------------------

    def allow_user(
        self,
        tool,
        user,
    ):

        if tool not in self._tools:

            self.register(tool)

        self._tools[tool]["users"].add(user)

        return True

    # -------------------------------------------------
    # Deny User
    # -------------------------------------------------

    def deny_user(
        self,
        tool,
        user,
    ):

        if tool not in self._tools:
            return False

        self._tools[tool]["users"].discard(user)

        return True

    # -------------------------------------------------
    # Check Permission
    # -------------------------------------------------

    def allowed(
        self,
        tool,
        *,
        role=None,
        user=None,
    ):

        if tool not in self._tools:
            return False

        permissions = self._tools[tool]

        #
        # Explicit user permission
        #

        if user is not None:

            if user in permissions["users"]:

                return True

        #
        # Role permission
        #

        if role is not None:

            if role in permissions["roles"]:

                return True

        return False

    # -------------------------------------------------
    # Tool Exists
    # -------------------------------------------------

    def exists(
        self,
        tool,
    ):

        return tool in self._tools

    # -------------------------------------------------
    # Roles
    # -------------------------------------------------

    def roles(
        self,
        tool,
    ):

        if tool not in self._tools:
            return []

        return sorted(

            self._tools[tool]["roles"]

        )

    # -------------------------------------------------
    # Users
    # -------------------------------------------------

    def users(
        self,
        tool,
    ):

        if tool not in self._tools:
            return []

        return sorted(

            self._tools[tool]["users"]

        )

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    def statistics(
        self,
    ):

        return {

            "tools": len(
                self._tools
            ),

            "role_permissions": sum(

                len(v["roles"])

                for v in self._tools.values()

            ),

            "user_permissions": sum(

                len(v["users"])

                for v in self._tools.values()

            ),

        }

    # -------------------------------------------------
    # Export
    # -------------------------------------------------

    def export(
        self,
    ):

        return {

            tool: {

                "roles": sorted(

                    values["roles"]

                ),

                "users": sorted(

                    values["users"]

                ),

            }

            for tool, values

            in self._tools.items()

        }

    # -------------------------------------------------
    # Clear
    # -------------------------------------------------

    def clear(
        self,
    ):

        self._tools = {}

    # -------------------------------------------------
    # Empty
    # -------------------------------------------------

    @staticmethod
    def empty():

        return ToolPermissions()