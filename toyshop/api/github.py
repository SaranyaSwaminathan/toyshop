import frappe
from frappe import _


# GitHub - Task integration
@frappe.whitelist(allow_guest=True)
def github_issue_webhook():
    data = frappe.request.get_json()

    # Only act when issue is opened
    if data.get("action") != "opened":
        return {"status": "ignored"}

    issue = data.get("issue")

    task = frappe.get_doc({
        "doctype": "Task",
        "subject": f"[GitHub] {issue.get('title')}",
        "description": issue.get("body") or "",
        "status": "Open",
        "priority": "Medium"
    })

    task.insert(ignore_permissions=True)
    frappe.db.commit()

    return {"status": "task created", "task": task.name}
