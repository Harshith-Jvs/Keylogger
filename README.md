# Keyboard Hook & Persistence Analysis

> ⚠️ **Ethical Use Notice**  
> This repository is intended **strictly for cybersecurity education, malware analysis training, and defensive research**.  
> Do **not** deploy monitoring software on systems without **explicit user consent**.

---

## Project Overview

This project documents the **technical analysis of a Windows keyboard hook–based monitoring program** and the **startup persistence mechanisms** commonly studied in malware analysis.

The purpose is to help cybersecurity students understand:

- How Windows keyboard hooks work internally
- How programs attempt to achieve persistence
- How defenders can **detect and mitigate such behavior**

---
## Architecture Overview

The analyzed architecture follows a typical **dropper–payload structure** often observed in malicious software samples.

| Component | Role |
|---|---|
| Startup Script | Launch mechanism triggered at system startup |
| Payload Binary | Program interacting with Windows APIs |
| Log File | Captured output written to disk |

### Execution Flow
System Startup
│
Startup Launcher
│
Executable Payload
│
Windows API Interaction
│
Event Processing / Logging


---

## Windows API Concepts Demonstrated

This project examines several Windows API mechanisms frequently studied in **malware analysis and endpoint detection research**.

## Keyboard Hooking

The Windows API allows programs to monitor input events using hooks.

Relevant API:

- `SetWindowsHookEx`
- `CallNextHookEx`
- `UnhookWindowsHookEx`

Hook types include:

- Low-level keyboard hooks
- Message hooks
- Event hooks

These mechanisms are used in legitimate software such as:

- Accessibility tools  
- Input method editors  
- Assistive technologies  

However, they are also commonly abused by malicious software.

---

## Window Context Identification

To determine which application receives input, programs may query the active window.

Relevant API:

- `GetForegroundWindow`
- `GetWindowText`

This allows correlation between **user input events and active applications**.

---

## Keyboard Translation

Keyboard input arrives as **Virtual Key Codes (VK codes)**.

To convert these into readable characters:

- `GetKeyboardState`
- `MapVirtualKey`
- `ToAscii` or `ToUnicode`

These functions account for:

- Shift key
- Caps Lock
- Keyboard layout

---

## Persistence Mechanisms in Windows

Malware often attempts to remain active after reboot.

Common persistence locations include:

| Mechanism | Description |
|---|---|
| Startup Folder | Automatically launches programs when the user logs in |
| Registry Run Keys | Executes programs on startup |
| Scheduled Tasks | Periodic or startup execution |
| Windows Services | Long-running background services |

Security teams routinely monitor these locations.

---

## Detection & Defensive Techniques

Security professionals detect suspicious behavior using multiple strategies.

## File System Monitoring

Watch for unexpected executables in directories such as:
C:\Users\Public

C:\ProgramData

Startup folders

---

## Behavioral Detection

Endpoint security tools can detect suspicious activity such as:

- Processes calling keyboard hook APIs
- Programs writing continuous input logs
- Unknown binaries executing on startup

---

# Security Tools for Investigation

Common tools used by analysts include:

- Autoruns – inspect startup entries
- Process Explorer – analyze running processes
- Wireshark – monitor network activity
- Windows Defender – built-in endpoint protection

---

## Learning Objectives

After studying this project, you should understand:

- How keyboard input flows through the Windows operating system
- How malware attempts to establish persistence
- How defenders detect suspicious API usage
- How to analyze suspicious binaries safely

---

## Safe Testing Environment

All experiments should be conducted inside an **isolated lab environment** such as:

- Virtual machines
- Sandboxed operating systems
- Dedicated malware analysis labs

Never test unknown binaries on your primary system.

---

## Disclaimer

This repository is provided **solely for defensive cybersecurity education and malware analysis research**.

The author and contributors **do not condone misuse** of these techniques.

Unauthorized monitoring of user activity may violate **privacy laws and computer misuse regulations**.
