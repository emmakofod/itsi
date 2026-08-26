Session 14 – Monitoring & Logging

📌 Why Logging Matters
Logging serves two purposes:

Real-time — see and alert on ongoing events as they happen
Post-incident (forensics) — discover what happened and how after the fact


Rule: Enable logging for ALL services. Never disable logging to save disk space.
Also always configure logging to a remote machine — very valuable for forensics (see Session 15).


🔍 Tool Overview
ToolPurposeLogcheckScans log files and alerts on suspicious entriesMultiTailView multiple log files simultaneously in one terminal windowGlancesReal-time system performance monitoring (CPU, RAM, disk, network)WhowatchMonitor who is logged in and what they are doingstatDetailed file/directory/filesystem metadatalsofList open files and network connections

📋 Logcheck
The problem: log files have thousands of entries — impossible to read manually.
Logcheck scans and filters log files, highlighting only interesting/suspicious lines and sending them by email (or stdout).
Configuration files

/etc/logcheck/logcheck.conf — main config (report level, email, timestamp format)
/etc/logcheck/logcheck.logfiles — which log files to scan
/etc/logcheck/violations.d/ — rules for things that are always flagged (security violations)
/etc/logcheck/ignore.d.server/ — rules for things to ignore (reduce noise)

Report levels
LevelUse caseworkstationLess strict, good if you don't have time to read muchserverDefault for serversparanoidVery strict — only for dedicated single-service servers
Key commands
bash# Run manually and print to terminal (not email)
sudo -u logcheck logcheck -o -t

# Check the config
sudo nano /etc/logcheck/logcheck.conf

# See which logs it scans
cat /etc/logcheck/logcheck.logfiles

# Change cron schedule (default: every hour + on reboot)
sudo nano /etc/cron.d/logcheck

📺 MultiTail
Lets you view multiple log files at once in a split terminal — useful when correlating events across logs.
bash# Two logs side by side
multitail /var/log/syslog /var/log/auth.log

# Three logs in two columns
multitail -s 2 /var/log/syslog /var/log/bootstrap.log /var/log/auth.log

# Colour coded logs
multitail -ci yellow /var/log/auth.log -ci blue -I /var/log/bootstrap.log

-I merges the second log into the same window as the previous one (interleaved, not split)


📊 Glances
Real-time system performance monitor — shows maximum info in a compact display.
Colour coding:

🟢 Green = OK
🔵 Blue = check it
🟣 Violet = warning
🔴 Red = critical

bash# Install
sudo apt install glances

# Run locally
glances

# Change refresh rate (default 3 seconds)
glances -t 5

# Run as server (so another machine can connect)
glances -s
glances -s -B 172.16.121.131     # bind to specific IP

# Connect from another machine
glances -c 172.16.121.131
Config file: /etc/glances/glances.conf (tweak colour thresholds here)

👥 Whowatch
Monitors who is logged in and what they are doing — like who and top combined.
bashsudo apt install whowatch
whowatch

Shows all logged-in users (terminal, SSH, etc.)
Press Enter on a user to see their processes
Bottom menu: sysinfo, details, kill process


📁 stat
Shows detailed metadata about a file, directory or filesystem — much more than ls -l.
bashstat /etc/passwd          # file metadata
stat /etc                 # directory metadata (note: Links count)
stat -f /dev/sda1         # filesystem info
Shows: access time, modify time, change time, inode number, device, number of links.

Useful in forensics — Modify = file contents changed, Change = permissions/ownership changed


🔌 lsof (List Open Files)
In Linux, everything is a file — including network connections. lsof shows what files/sockets are currently open.
bashsudo lsof | wc -l                    # how many files are open total?
sudo lsof -i                         # all network connections
sudo lsof -i tcp                     # only TCP connections
sudo lsof -i -u ekko                 # files + network by user
sudo lsof -p 1234                    # all files opened by process ID 1234
