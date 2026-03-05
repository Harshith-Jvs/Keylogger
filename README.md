# Keylogger

# Architecture Overview

The analyzed architecture follows a typical **dropper–payload structure** often observed in malicious software samples.

| Component | Role |
|---|---|
| Startup Script | Launch mechanism triggered at system startup |
| Payload Binary | Program interacting with Windows APIs |
| Log File | Captured output written to disk |
