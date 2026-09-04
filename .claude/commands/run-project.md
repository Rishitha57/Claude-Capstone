# Command: /run-project

Run the complete local AI Expense Advisor verification workflow from the
repository root.

```powershell
python scripts/verify_workflow.py
```

The command runs the test suite, core financial coverage, dependency audit,
secret scan, and offline Confluence publication check. It does not contact
Confluence. To publish the verified documents to the configured Confluence
space, run:

```powershell
python scripts/publish_all_confluence.py
```

Credentials are loaded from the untracked `.env` file and are never included
in prompts, logs, or reports.