import argparse
import json
import sys
from typing import Dict, Any, List

# --- Fictitious App Database / State ---
MOCK_DB = {
    "users": [
        {"id": 1, "name": "Alice Smith", "email": "alice@example.com", "status": "active"},
        {"id": 2, "name": "Bob Jones", "email": "bob@example.com", "status": "pending"},
    ],
    "system_health": "healthy",
    "background_jobs": []
}

# --- Core Business Logic Functions (The Application) ---
def get_users(status: str = None) -> List[Dict[str, Any]]:
    """Inspect tool for agents to read data."""
    if status:
        return [u for u in MOCK_DB["users"] if u["status"] == status]
    return MOCK_DB["users"]

def update_user_status(user_id: int, status: str) -> Dict[str, Any]:
    """Command tool for agents to execute mutation actions."""
    for user in MOCK_DB["users"]:
        if user["id"] == user_id:
            user["status"] = status
            return {"success": True, "message": f"User {user_id} updated to {status}", "user": user}
    return {"success": False, "message": f"User {user_id} not found"}

def run_sync_workflow() -> Dict[str, Any]:
    """Workflow tool for running compound background automations."""
    # Simulate a multi-step routine an AI agent might trigger after updating code
    MOCK_DB["background_jobs"].append("sync_external_apis")
    return {
        "status": "completed",
        "steps_executed": ["fetch_remote", "reconcile_db", "clear_cache"],
        "records_affected": len(MOCK_DB["users"]),
        "system_health": MOCK_DB["system_health"]
    }

# --- CLI Framework Architecture ---
def main():
    parser = argparse.ArgumentParser(
        description="Agent-Accessible CLI Gateway for App Integration.",
        epilog="Designed for optimal scraping and parsing by LLM/AI Coding Agents."
    )

    # Global flag forcing JSON output so agents can programmatically consume standard out
    parser.add_argument("--json", action="store_true", help="Format all stdout as parsable JSON")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available agent operations")

    # 1. INSPECT DATA Command
    inspect_parser = subparsers.add_parser("inspect", help="Read-only data extraction hooks for the AI agent")
    inspect_parser.add_argument("--status", choices=["active", "pending"], help="Filter users by system status")

    # 2. EXECUTE COMMAND Command
    execute_parser = subparsers.add_parser("execute", help="Action mutations to change database state")
    execute_parser.add_argument("--update-user", type=int, metavar="USER_ID", help="The specific user ID to modify")
    execute_parser.add_argument("--set-status", choices=["active", "pending"], help="The new status to apply")

    # 3. RUN WORKFLOW Command
    workflow_parser = subparsers.add_parser("workflow", help="Trigger high-level multi-step application routines")
    workflow_parser.add_argument("--action", choices=["sync"], required=True, help="The macro pipeline to kick off")

    # Parse arguments passed by the terminal/agent
    args = parser.parse_args()
    output: Dict[str, Any] = {}

    try:
        # Route logic based on commands
        if args.command == "inspect":
            data = get_users(status=args.status)
            output = {"status": "success", "data": data}

        elif args.command == "execute":
            if args.update_user and args.set_status:
                result = update_user_status(args.update_user, args.set_status)
                output = result
            else:
                parser.error("Executing user mutations requires BOTH --update-user and --set-status.")

        elif args.command == "workflow":
            if args.action == "sync":
                result = run_sync_workflow()
                output = {"status": "success", "workflow_results": result}

        # Print layout based on agent preference (--json)
        if args.json:
            print(json.dumps(output, indent=2))
        else:
            # Human readable fallback
            print(f"[{args.command.upper()} RESULT]:")
            print(json.dumps(output, indent=2)) # Defaulting to structured formats makes AI processing safer

    except Exception as e:
        error_payload = {"status": "error", "message": str(e)}
        if args.json:
            print(json.dumps(error_payload), file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
