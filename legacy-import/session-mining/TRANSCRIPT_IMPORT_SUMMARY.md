# Legacy Transcript Import Summary

Reviewed old session transcripts in `~/Desktop/openclawoldbot/agents/main/sessions/` for durable preferences, workflows, and failure patterns.

## Durable findings imported
- n8n was part of the active Linux automation stack.
- Google Sheets automation for internships depended on Google auth / `gog` tooling.
- Discord delivery sometimes failed because channel targets were referenced by names instead of stable IDs.
- Browser-control timeouts affected the internship sheet-update workflow.
- Healthcheck/skill-scan automation was an intentional recurring maintenance habit.

## Not imported as memory
- transient one-off troubleshooting chatter
- raw cron outputs
- machine-specific paths and environment details
- tokens, keys, or secret-bearing command output

## Recommended follow-up
- If Discord automation matters, replace name-based targets with stable channel IDs where possible.
- If internship sheet automation matters, rebuild Google auth/tooling on this Mac before trusting the job.
- If n8n matters, re-establish it explicitly on this Mac rather than copying old runtime state.
