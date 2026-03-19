# Legacy OpenClaw Import

Source inspected read-only: `~/Desktop/openclawoldbot`
Import date: 2026-03-19

## What was imported into this workspace

### Identity and user context
- Assistant identity from old `workspace/IDENTITY.md`
- User name and preference notes from old `workspace/USER.md`
- Relevant memory notes from old `workspace/memory/*.md`

### Legacy recurring jobs discovered
From old `cron/jobs.json`:
1. `healthcheck:skill-scan`
   - Weekly Monday 09:00 UTC
   - Run skills check, deep security audit, update status, produce risk report
2. `discord:professional-events-weekly`
   - Weekly Sunday 10:00 UTC
   - Research Tokyo professional events for students and post to Discord
3. `internships:tokyo-english-weekly-sheet-update`
   - Weekly Monday 10:00 UTC
   - Update a Google Sheet with English-friendly Tokyo internships
4. `discord:tokyo-student-topic-weekly`
   - Weekly Wednesday 09:00 Asia/Tokyo
   - Post one student discussion question to Discord
5. `discord:social-events-weekend`
   - Weekly Thursday 17:00 Asia/Tokyo
   - Post Tokyo social events for the upcoming weekend to Discord

## What was intentionally NOT imported automatically
- Linux-specific paths like `/home/squire/.openclaw/workspace`
- Secrets/tokens/API keys
- Device identity/auth files
- Machine-specific pairing/device state
- Direct config replacement from the old `openclaw.json`
- Service account JSON contents
- Browser profiles, venvs, node_modules, delivery queue, media caches

## Candidate follow-up actions
- Recreate selected cron jobs on this Mac only after confirming which ones still matter
- Reconnect Discord if those announcement jobs are still wanted
- Rebuild any safe local notes in `TOOLS.md` if needed
- Optionally review old session transcripts for more durable memory worth importing
