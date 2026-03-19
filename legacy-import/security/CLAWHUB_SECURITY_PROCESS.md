# ClawHub Security Process

Rules enforced:
1. Skills may only come from ClawHub registry.
2. Skills may only come from trusted sources in `.clawhub-policy.json`.
3. All files are inspected and scanned before install.

## Install command (legacy reference)

```bash
./scripts/clawhub-safe-install.sh <slug> [version]
```

## Policy file

Current trusted sources from legacy setup:
- @steipete
- @RhysSullivan
- @lamelas

Legacy scan patterns included:
- shell pipe-to-bash style patterns
- eval / child_process / subprocess / os.system
- sudo / dangerous rm patterns
- possible secret assignments
- plain http://

Imported as documentation only. Not wired into current automation.
