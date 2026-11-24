# Week 2 foundations notes

Project path: ~/codeplatoon/w2-foundations

Why a harness matters (one sentence): The harness keeps agent instructions and rules in files inside the repo, so they are versioned, shared and reviewed like code instead of living in someone's chat history.

Skill name: check-local-stack

Hook name: deny-rm

Permission rules I set: see "Permission rules" below

Real-world use for a skill: a release checklist, onboarding a new teammate, or an incident response runbook.

Real-world use for a hook: log every command an agent runs so a team lead can review it later, or block `git commit` unless the message has a ticket number.

## Permission rules

I use the Antigravity desktop app. Permissions are set in Settings > General > Global Permissions, not in a file in this repo.

- Preset: Default

File reads (Settings > Tool Permissions > File access rules):
- Deny: `/Users/leon1186/codeplatoon/w2-foundations/.env` (keep secrets out of the chat)
- Deny: `/Users/leon1186/.ssh` (keep SSH keys out of the chat)
- Allow: `/Users/leon1186/codeplatoon/w2-foundations` (the agent can read my project)

Terminal commands (Settings > Tool Permissions > Terminal commands):
- Deny: `rm -rf` (backup in case the hook fails)
- Ask: `*` (I approve every other command before it runs)
- Allow: `ls` (harmless, no need to ask)

Deny is checked first, then Ask, then Allow. That way a broad Allow can never override a specific Deny. Example: the whole project folder is allowed for reads, but `.env` inside it is still denied because Deny wins.

Mistake I caught: at first I set Deny on the whole project folder for reads, which would have blocked the agent from reading its own skill and notes. I changed it to Allow.

## Skill run

- Prompt: `/check-local-stack`
- What the agent did: It read SKILL.md, then listed the three commands before running them: `python3 --version`, `psql --version` and `pg_isready`. Results: Python 3.15.2, psql (PostgreSQL) 18.1, and `pg_isready` answered `/tmp:5432 - no response`. Its summary said Python and the psql client are ready, and the PostgreSQL server is not running. It did not install anything.
- Tool calls approved: one `run_command` (all three checks were chained into a single command).

Later I also tried `@[.agents/skills/check-local-stack]`. That did NOT run the checks. The agent only listed the folder and described the skill. The slash command is what actually runs it.

## Hook test

Denied:
- Prompt: `rm NOTES.md`
- Result: "tool call denied by pre-tool hook: Course hook blocks rm. Use a safer cleanup path or run rm yourself in your own terminal." NOTES.md still exists.

Allowed:
- Prompt: `ls NOTES.md`
- Result: the agent ran `ls -la NOTES.md` and it worked: `-rw-r--r--@ 1 leon1186 staff 426 Nov 23 21:30 NOTES.md`

Dry run in my terminal (no IDE):

```bash
printf '%s' '{"toolCall":{"name":"run_command","args":{"CommandLine":"rm NOTES.md"}}}' | python3 ./scripts/deny_rm.py
# {"decision": "deny", "reason": "Course hook blocks rm. ..."}
printf '%s' '{"toolCall":{"name":"run_command","args":{"CommandLine":"ls NOTES.md"}}}' | python3 ./scripts/deny_rm.py
# {"decision": "allow"}
```

The hook is just a program that reads the tool call as JSON on stdin and prints a decision as JSON on stdout, so I can test it with `printf` without opening Antigravity.

Path bug I hit: hooks run with `.agents/` as the working directory. My first `hooks.json` used `./scripts/deny_rm.py`, so Antigravity looked for `.agents/scripts/deny_rm.py`, which did not exist, and the hook failed. I changed the command to `python3 ../scripts/deny_rm.py`, restarted Antigravity, and `rm NOTES.md` is still blocked.

## Detection pass

Slop: The skill's command `which pg_isready && pg_isready || echo "pg_isready not found"` printed "pg_isready not found" even though pg_isready was found. The `||` also fires when the server does not respond. The final summary was right, but the raw output was misleading.

Drift: During the hook test the agent went beyond what I asked. After the hook failed, it read files around the repo (including `.git/config`), created `.agents/scripts/deny_rm.py` without asking, and then ran `rm NOTES.md` again on its own. The hook blocked it, but it should have stopped and told me instead of trying to delete the file a second time. I removed the copy and fixed the path in `hooks.json`.

Hallucination: none. Its claim that hooks run from `.agents/` matches the error message (`.agents/./scripts/deny_rm.py: No such file or directory`).

One fix I would make next time: make `deny_rm.py` stricter. It only catches `rm` with spaces around it, so `/bin/rm`, `;rm` or `find . -delete` would get through. I would also change the skill to run each check as its own command so the output can't mislead.
