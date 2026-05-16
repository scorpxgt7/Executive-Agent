"""
Role-Based Access Control (RBAC) and Permission Management

Defines roles, permissions, and enforcement policies for the platform.
"""

from enum import Enum
from typing import Dict, List, Set
import structlog

logger = structlog.get_logger()


class Role(str, Enum):
    """System roles"""
    ADMIN = "admin"  # Full system access
    OPERATOR = "operator"  # Execute and manage goals/tasks
    VIEWER = "viewer"  # Read-only access
    SYSTEM = "system"  # Internal system operations


class Permission(str, Enum):
    """System permissions"""
    # Goal management
    GOALS_CREATE = "goals:create"
    GOALS_READ = "goals:read"
    GOALS_UPDATE = "goals:update"
    GOALS_DELETE = "goals:delete"

    # Task management
    TASKS_CREATE = "tasks:create"
    TASKS_READ = "tasks:read"
    TASKS_UPDATE = "tasks:update"
    TASKS_EXECUTE = "tasks:execute"

    # Approval management
    APPROVALS_READ = "approvals:read"
    APPROVALS_APPROVE = "approvals:approve"
    APPROVALS_REJECT = "approvals:reject"

    # Agent management
    AGENTS_READ = "agents:read"
    AGENTS_MANAGE = "agents:manage"

    # Monitoring
    MONITORING_READ = "monitoring:read"
    MONITORING_EXPORT = "monitoring:export"

    # System administration
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_CONFIG = "system:config"
    SYSTEM_AUDIT = "system:audit"


# Role to permissions mapping
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        # All permissions
        Permission.GOALS_CREATE,
        Permission.GOALS_READ,
        Permission.GOALS_UPDATE,
        Permission.GOALS_DELETE,
        Permission.TASKS_CREATE,
        Permission.TASKS_READ,
        Permission.TASKS_UPDATE,
        Permission.TASKS_EXECUTE,
        Permission.APPROVALS_READ,
        Permission.APPROVALS_APPROVE,
        Permission.APPROVALS_REJECT,
        Permission.AGENTS_READ,
        Permission.AGENTS_MANAGE,
        Permission.MONITORING_READ,
        Permission.MONITORING_EXPORT,
        Permission.SYSTEM_ADMIN,
        Permission.SYSTEM_CONFIG,
        Permission.SYSTEM_AUDIT,
    },
    Role.OPERATOR: {
        # Execute workflows and manage tasks
        Permission.GOALS_CREATE,
        Permission.GOALS_READ,
        Permission.GOALS_UPDATE,
        Permission.TASKS_CREATE,
        Permission.TASKS_READ,
        Permission.TASKS_UPDATE,
        Permission.TASKS_EXECUTE,
        Permission.APPROVALS_READ,
        Permission.APPROVALS_APPROVE,
        Permission.APPROVALS_REJECT,
        Permission.AGENTS_READ,
        Permission.MONITORING_READ,
    },
    Role.VIEWER: {
        # Read-only access
        Permission.GOALS_READ,
        Permission.TASKS_READ,
        Permission.APPROVALS_READ,
        Permission.AGENTS_READ,
        Permission.MONITORING_READ,
    },
    Role.SYSTEM: {
        # Internal operations
        Permission.GOALS_CREATE,
        Permission.GOALS_READ,
        Permission.GOALS_UPDATE,
        Permission.TASKS_CREATE,
        Permission.TASKS_READ,
        Permission.TASKS_UPDATE,
        Permission.TASKS_EXECUTE,
        Permission.MONITORING_READ,
        Permission.SYSTEM_AUDIT,
    }
}


class RBAC:
    """Role-Based Access Control manager"""

    @staticmethod
    def get_permissions_for_role(role: Role) -> Set[Permission]:
        """Get all permissions for a role"""
        return ROLE_PERMISSIONS.get(role, set())

    @staticmethod
    def get_permissions_for_roles(roles: List[str]) -> Set[str]:
        """
        Get all permissions for a list of roles

        Args:
            roles: List of role names

        Returns:
            Set of permission strings
        """
        permissions: Set[str] = set()
        for role_name in roles:
            try:
                role = Role(role_name)
                permissions.update(RBAC.get_permissions_for_role(role))
            except ValueError:
                logger.warning("rbac_unknown_role", role=role_name)

        return permissions

    @staticmethod
    def has_permission(roles: List[str], required_permission: str) -> bool:
        """
        Check if roles have required permission

        Args:
            roles: List of role names
            required_permission: Permission to check

        Returns:
            True if any role has permission, False otherwise
        """
        permissions = RBAC.get_permissions_for_roles(roles)
        return required_permission in permissions

    @staticmethod
    def can_access_goal(roles: List[str], action: str) -> bool:
        """Check if user can perform action on goals"""
        permission_map = {
            "create": Permission.GOALS_CREATE.value,
            "read": Permission.GOALS_READ.value,
            "update": Permission.GOALS_UPDATE.value,
            "delete": Permission.GOALS_DELETE.value,
        }
        required = permission_map.get(action)
        return required and RBAC.has_permission(roles, required)

    @staticmethod
    def can_execute_task(roles: List[str]) -> bool:
        """Check if user can execute tasks"""
        return RBAC.has_permission(roles, Permission.TASKS_EXECUTE.value)

    @staticmethod
    def can_approve(roles: List[str]) -> bool:
        """Check if user can approve requests"""
        return RBAC.has_permission(roles, Permission.APPROVALS_APPROVE.value)

    @staticmethod
    def can_administer_system(roles: List[str]) -> bool:
        """Check if user can administer system"""
        return RBAC.has_permission(roles, Permission.SYSTEM_ADMIN.value)


# Audit action types
class AuditAction(str, Enum):
    """Types of actions to audit"""
    GOAL_CREATED = "goal_created"
    GOAL_UPDATED = "goal_updated"
    GOAL_DELETED = "goal_deleted"
    TASK_EXECUTED = "task_executed"
    TASK_FAILED = "task_failed"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_APPROVED = "approval_approved"
    APPROVAL_REJECTED = "approval_rejected"
    SYSTEM_CONFIG_CHANGED = "system_config_changed"
    AUTH_LOGIN = "auth_login"
    AUTH_FAILURE = "auth_failure"
    PERMISSION_DENIED = "permission_denied"


class AuditEntry:
    """Audit log entry structure"""

    def __init__(
        self,
        action: AuditAction,
        user_id: str,
        resource_type: str,
        resource_id: str,
        details: Dict = None,
        status: str = "success",
        ip_address: str = None,
    ):
        self.action = action.value
        self.user_id = user_id
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.details = details or {}
        self.status = status
        self.ip_address = ip_address
        self.timestamp = None

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "action": self.action,
            "user_id": self.user_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "details": self.details,
            "status": self.status,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp,
        }
