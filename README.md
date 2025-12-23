# 🛠️ AutomationZ Admin Control Panel [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R6R51QD7BU)

AutomationZ Admin Control Panel is the **central command hub** for all AutomationZ automation tools.
It allows you to control, schedule, monitor, and maintain multiple game servers and services
from **one unified desktop interface**.

# AutomationZ_Admin_Control_Center

[![Automation_Z_Admin_Control_Center.png](https://i.postimg.cc/d0ymHhY8/Automation_Z_Admin_Control_Center.png)](https://postimg.cc/hJKdhPhj)

## Overview
Main AutomationZ Control Center dashboard launching and supervising all AutomationZ tools.

## Purpose
This screen demonstrates how **AutomationZ Admin Control Center** integrates into the AutomationZ ecosystem.

## Key Features
- Unified AutomationZ dark UI
- Profile-based server targeting
- Safe automation workflows
- Visual status & logging feedback

## Notes
This interface is part of the **AutomationZ Admin Control Center** suite.

This is a **server-side automation control panel** for real administrators.

---

## 👑 What This Tool Is ( Tool_List ) 

AutomationZ Admin Control Center acts as the **master controller** for:

- AutomationZ Admin Orchestrator [Go to AutomationZ AutomationZ Admin Orchestrator](#AutomationZ_Admin_Orchestrator)
- AutomationZ Log Cleanup Scheduler [Go to AutomationZ AutomationZ Log Cleanup Scheduler](#AutomationZ_Log_Cleanup_Scheduler)
- AutomationZ Scheduler [Go to AutomationZ Scheduler](#AutomationZ_Scheduler)
- AutomationZ Server Backup Scheduler [Go to AutomationZ Server Backup Scheduler](#AutomationZ_Server_Backup_Scheduler) 
- AutomationZ Server Health Monitor [Go to AutomationZ Server Health Monitor](#AutomationZ_Server_Health)
- AutomationZ Uploader [Go to AutomationZ Uploader](#AutomationZ_Uploader)
- Future AutomationZ tools

## 🧰 AutomationZ Tools Overview

- **AutomationZ Admin Orchestrator**
  Plans + mappings + profiles, push presets to targets, optional restart + verify.

- **AutomationZ Log Cleanup Scheduler**  
  Automatically clean and rotate server logs to prevent disk bloat and maintain long-term stability.  

- **AutomationZ Scheduler**  
  Execute time-based automation tasks such as preset uploads or configuration changes without manual intervention.

- **AutomationZ Server Backup Scheduler**  
  Create scheduled server backups and snapshots with profile-based targets and restore-ready archives.

- **AutomationZ Server Health Monitor**  
  Monitor live server logs, detect crashes and errors, and send real-time alerts via Discord.

- **AutomationZ Uploader**  
  Safely deploy configuration presets to servers using FTP/FTPS with preview, validation, and automatic backups.

- **Future AutomationZ Tools**  
  The AutomationZ platform is designed for expansion, allowing new automation modules to integrate seamlessly into the control panel.  

 
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


All future tools inherit:
- Same UI
- Same logic
- Same philosophy

---

# Included Tools:
# AutomationZ_Admin_Orchestrator
[Go to Original Projects Repo for detailed description](https://github.com/DayZ-AutomationZ/AutomationZ_Admin_Orchestrator) 
Nothing new under the hood here — this version only changes the UI.
The logic and functionality are exactly the same as the original tool.
If you already use AutomationZ, you can just drop the `main.py` in the AutomationZ_Admin_Orchestrator folder from this repo into the original repository to switch to the new design.
[![Automation_Z_Admin_Orchestrator.png](https://i.postimg.cc/FKLgWY43/Automation_Z_Admin_Orchestrator.png)](https://postimg.cc/rdqrzFzw)
## Overview 
Central orchestration engine combining plans, mappings, profiles, and scheduling into one control flow.

## Purpose
This screen demonstrates how **AutomationZ Admin Orchestrator** integrates into the AutomationZ ecosystem.

## Key Features
- Unified AutomationZ dark UI
- Profile-based server targeting
- Safe automation workflows
- Visual status & logging feedback

# AutomationZ_Log_Cleanup_Scheduler
[Go to Original Projects Repo for detailed description](https://github.com/DayZ-AutomationZ/AutomationZ_Log_Cleanup_Scheduler) 
Nothing new under the hood here — this version only changes the UI.
The logic and functionality are exactly the same as the original tool.
If you already use AutomationZ, you can just drop the `main.py` in the AutomationZ_Admin_Orchestrator folder from this repo into the original repository to switch to the new design.
[![Automation_Z_Log_Cleanup_Scheduler.png](https://i.postimg.cc/DzXdjSTJ/Automation_Z_Log_Cleanup_Scheduler.png)](https://postimg.cc/wt9m3T3g)
## Overview
Automated log retention and cleanup scheduler to prevent disk bloat and keep servers clean.

## Purpose
This screen demonstrates how **AutomationZ Log Cleanup Scheduler** integrates into the AutomationZ ecosystem.

## Key Features
- Unified AutomationZ dark UI
- Profile-based server targeting
- Safe automation workflows
- Visual status & logging feedback

# AutomationZ_Scheduler

[![Automation_Z_Scheduler.png](https://i.postimg.cc/HLy4Zrgb/Automation_Z_Scheduler.png)](https://postimg.cc/WDsktbt4)
## Overview
Time-based automation engine for executing preset uploads and tasks without server restarts.

## Purpose
This screen demonstrates how **AutomationZ Scheduler** integrates into the AutomationZ ecosystem.

## Key Features
- Unified AutomationZ dark UI
- Profile-based server targeting
- Safe automation workflows
- Visual status & logging feedback

# AutomationZ_Server_Backup_Scheduler

[![Automation_Z_Server_Backup_Scheduler.png](https://i.postimg.cc/zfgStyrg/Automation_Z_Server_Backup_Scheduler.png)](https://postimg.cc/3y3vWJW8)
## Overview
Scheduled snapshot and backup automation with profile-based targets and restore-ready archives.

## Purpose
This screen demonstrates how **AutomationZ Server Backup Scheduler** integrates into the AutomationZ ecosystem.

## Key Features
- Unified AutomationZ dark UI
- Profile-based server targeting
- Safe automation workflows
- Visual status & logging feedback

# AutomationZ_Server_Health

[![Automation_Z_Server_Health.png](https://i.postimg.cc/5tCq7XVF/Automation_Z_Server_Health.png)](https://postimg.cc/1gyq4549)
## Overview
Live server log monitoring tool with crash detection, error scanning, and Discord notifications.

## Purpose
This screen demonstrates how **AutomationZ Server Health** integrates into the AutomationZ ecosystem.

## Key Features
- Unified AutomationZ dark UI
- Profile-based server targeting
- Safe automation workflows
- Visual status & logging feedback

# AutomationZ_Uploader

[![Automation_Z_Uploader.png](https://i.postimg.cc/DzXdjST4/Automation_Z_Uploader.png)](https://postimg.cc/MczQXKXz)
## Overview
Preset-based FTP/FTPS uploader for pushing server configuration files safely with preview, backups, and exact path mapping.

## Purpose
This screen demonstrates how **AutomationZ Uploader** integrates into the AutomationZ ecosystem.

## Key Features
- Unified AutomationZ dark UI
- Profile-based server targeting
- Safe automation workflows
- Visual status & logging feedback

## Notes
These interfaces are part of the **AutomationZ Admin Control Center** suite.

Created by **Danny van den Brande**
