---
name: check-local-stack
description: Checks whether Python and PostgreSQL look available on this machine before local app work. Use when verifying the local stack, preparing to run Flask with PostgreSQL, or confirming installfest tools still work.
---

# Check local stack

When this skill is active:

1. State the commands you will run before you run them.
2. Check Python with `python3 --version`.
3. Check PostgreSQL client access with `psql --version`.
4. If `pg_isready` exists, run `pg_isready` and report the result.
5. Summarize what is ready and what is missing.
6. Do not install packages unless the user explicitly asks for installs.
