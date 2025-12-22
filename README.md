# 🛠️ AutomationZ Admin Control Panel (Orchestrator) [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R6R51QD7BU)

AutomationZ Admin Control Panel is the **central command hub** for all AutomationZ automation tools.
It allows you to control, schedule, monitor, and maintain multiple game servers and services
from **one unified desktop interface**.

This is **not a game mod**.  
This is a **server-side automation control panel** for real administrators.

---

## 👑 What This Tool Is

AutomationZ Admin Orchestrator acts as the **master controller** for:

- AutomationZ Uploader
- AutomationZ Scheduler
- AutomationZ Backup Scheduler
- AutomationZ Server Health Monitor
- AutomationZ Log Cleanup Scheduler
- Future AutomationZ tools

All tools share:
- Identical UI theme
- Identical workflow logic
- Identical profile & mapping structure

---

## 🎨 Unified AutomationZ UI Theme

All AutomationZ tools use the same dark professional UI:

- Background: #333333
- Panels: #363636
- Text: #e6e6e6
- Accent: AutomationZ Green (#4CAF50)
- Primary green action buttons
- Styled text areas and list views

This ensures **zero context switching** and a professional admin experience.

---

## 📁 Folder Structure

```
AutomationZ_Admin_Orchestrator/
│
├── main.py
├── README.md
│
├── config/
│   ├── profiles.json
│   ├── settings.json
│   └── mappings.json
│
├── logs/
│
├── backups/
│   └── <profile>/<job>/<timestamp>/
│
├── presets/
│   ├── dayz/
│   ├── rust/
│   ├── minecraft/
│   └── fivem/
│
└── docs/
    └── screenshots/
```

---

## 🔐 Profiles (Server Connections)

Profiles define how AutomationZ connects to your servers via FTP or FTPS.

### Example: Nitrado DayZ

```json
{
  "name": "Nitrado_DayZ",
  "host": "ftp.nitrado.net",
  "port": 21,
  "username": "FTP_USER",
  "password": "FTP_PASS",
  "tls": false,
  "root": "/dayzstandalone"
}
```

### Example: Generic VPS (FTPS)

```json
{
  "name": "VPS_Server",
  "host": "yourdomain.com",
  "port": 21,
  "username": "ftpuser",
  "password": "password",
  "tls": true,
  "root": "/home/container"
}
```

Profiles are shared across **all AutomationZ tools**.

---

## 📦 Presets

Presets are local folders containing files you want to deploy.

Example:
```
presets/raid_on/
  ├── cfggameplay.json
  └── BBP_Settings.json
```

Presets are:
- Never uploaded automatically
- Explicitly selected
- Reusable across servers

---

## 🔁 Mappings (Core Automation Logic)

Mappings define **what file goes where**.

### DayZ Example

```json
{
  "name": "DayZ_cfggameplay",
  "enabled": true,
  "local_relpath": "cfggameplay.json",
  "remote_path": "mpmissions/dayzOffline.chernarusplus/cfggameplay.json",
  "backup_before_overwrite": true
}
```

### BaseBuildingPlus Example

```json
{
  "name": "BBP_Settings",
  "enabled": true,
  "local_relpath": "BBP_Settings.json",
  "remote_path": "config/BaseBuildingPlus/BBP_Settings.json",
  "backup_before_overwrite": true
}
```

---

## ⏱️ Scheduling & Automation

The Orchestrator allows you to:
- Run tasks manually
- Schedule tasks
- Chain multiple tools together

Typical automated flows:
- Backup → Upload preset → Restart server
- Nightly cleanup → Health scan → Discord report

---

## 🧹 Log Cleanup Scheduler

Automates:
- Log retention
- Folder cleanup
- Disk space control

---

## ❤️ Server Health Monitor

Detects:
- Errors
- Crashes
- Warnings

Features:
- Offset-based scanning
- Discord alerts
- Weekly crash summary

---

## 💾 Backup Scheduler

Automates:
- Pre-overwrite backups
- Scheduled backups
- Restore points

Backups are stored as:
```
backups/<profile>/<job>/<timestamp>/
```

---

## 🔐 Security Notes

- Credentials are stored locally
- Use limited FTP users
- Prefer FTPS
- Do not expose AutomationZ publicly

---

## 🚀 Typical Use Cases

- DayZ raid window automation
- Multi-server config rollout
- Scheduled maintenance
- Automated backups
- Log hygiene
- Crash detection & alerts

---

## 🧩 Future Expansion

Planned tools:
- Mod update auto-deployer
- Restart orchestrator
- Player/queue watcher
- Config diff viewer
- Multi-server rollout

All future tools inherit:
- Same UI
- Same logic
- Same philosophy

---

## 👑 Author

Created by **Danny van den Brande**  
AutomationZ Project

Control. Automation. Ownership.
