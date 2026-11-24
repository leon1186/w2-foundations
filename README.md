# w2-foundations

Week 2 Day 1 homework. I set up the AI agent in Antigravity with a skill, a hook and permissions. All of it lives in files in this repo, so anyone who clones it gets the same setup.

## What is a skill?

A skill is a set of steps written in plain English that the agent follows when I call it by name. It's like a checklist I give the agent so I don't have to type the same instructions every time.

My skill is `check-local-stack`. I run it with `/check-local-stack` and it checks that Python, the `psql` client and the PostgreSQL server are ready before I start Flask and Postgres work. It tells me what's ready and what's missing, and it doesn't install anything.

The skill is only instructions. The agent reads them and tries to follow them, but it could still forget or do something else.

## What is a hook?

A hook is a small program that Antigravity runs automatically at a certain moment, like right before the agent runs a terminal command. The agent can't skip it.

My hook is `deny-rm`. Before every terminal command, Antigravity sends the command to `scripts/deny_rm.py` as JSON. The script answers `deny` if the command uses `rm`, and `allow` for everything else. So the agent can't delete files, even if it tries.

The difference: a skill asks the agent to behave. A hook stops it.

## How do permissions work when rules conflict?

Permissions are Allow / Ask / Deny rules I set in Antigravity Settings > Tool Permissions.

- **Allow**: runs without asking me
- **Ask**: stops and waits for me to approve
- **Deny**: blocked

When two rules match the same thing, **Deny wins first, then Ask, then Allow.** So a big Allow can never cancel a specific Deny. For example, I allow the agent to read my whole project folder, but I deny `.env` inside it. The agent still can't read `.env`, because Deny is checked first.

My exact rules are in `NOTES.md`.

## Files

```text
w2-foundations/
├── .agents/
│   ├── hooks.json                     # tells Antigravity to run the hook before terminal commands
│   └── skills/
│       └── check-local-stack/
│           └── SKILL.md               # the skill
├── scripts/
│   └── deny_rm.py                     # the hook program that blocks rm
├── NOTES.md                           # what I tested, my permission rules, detection pass
└── README.md                          # this file
```

Note: hooks run from inside `.agents/`, so `hooks.json` points to `../scripts/deny_rm.py`.

## Test the hook without Antigravity

```bash
printf '%s' '{"toolCall":{"name":"run_command","args":{"CommandLine":"rm NOTES.md"}}}' | python3 ./scripts/deny_rm.py
# {"decision": "deny", ...}

printf '%s' '{"toolCall":{"name":"run_command","args":{"CommandLine":"ls NOTES.md"}}}' | python3 ./scripts/deny_rm.py
# {"decision": "allow"}
```
