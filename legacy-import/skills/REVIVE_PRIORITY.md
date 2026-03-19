# Legacy Skill Revival Priority

Goal: identify which legacy skills are most worth reviving on this Mac first.

## Revive first (highest leverage)

### 1. gog
Why:
- directly supports the internship Google Sheet workflow
- supports Gmail, Calendar, Drive, Sheets, Docs, Contacts
- old bot clearly depended on Google auth/tooling for automation
Status:
- worth re-establishing once Google auth is ready on this Mac

### 2. github
Why:
- low-risk, broadly useful, no unusual hardware dependency
- helpful for repo/CI/PR work
Status:
- easy win if `gh` is installed/authenticated

### 3. oracle
Why:
- useful for second-model review, debugging, architecture checks
- complements coding/troubleshooting work well
Status:
- good value if you still want that workflow

### 4. summarize
Why:
- broadly useful for URLs, PDFs, files, and videos
- strong day-to-day utility
Status:
- useful once desired API key/provider path is confirmed

### 5. nano-pdf / video-frames
Why:
- practical utility tools with bounded scope
- minimal account complexity compared with other legacy skills
Status:
- easy selective reactivation candidates

## Revive if needed (medium priority)
- gemini — useful if you explicitly want Gemini CLI access
- gifgrep — nice utility, but not core infrastructure
- blogwatcher — useful only if blog/RSS monitoring matters again
- himalaya — only if terminal email workflow is desired
- sag — useful if ElevenLabs voice/TTS is wanted again
- goplaces — useful if place search becomes a recurring workflow

## Leave disabled unless there is a concrete need (lower priority)
- blucli
- sonoscli
- openhue
- eightctl
- camsnap
- wacli
- ordercli
- songsee

Reason:
These depend on local devices, home-network hardware, third-party auth, or a very specific use case.

## Important caution
Do not bulk-reactivate legacy skills all at once.
Best path is selective recovery:
1. confirm the workflow still matters
2. install the required CLI/tooling
3. authenticate/configure it on this Mac
4. test a single happy path
5. only then consider using it in real automations
