*This project has been created as part of the 42 curriculum by oshtohri*

# Born2beroot

## Description

Born2beroot is a system administration project designed to introduce students to Linux server administration, virtualization, and security hardening.

The goal of the project is to build a minimal virtual machine from scratch, configure it according to strict subject requirements, and understand every major component of the setup. This includes:
- choosing and installing a stable Linux distribution;
- configuring encrypted storage with LVM;
- managing users and groups;
- securing remote access with SSH;
- configuring a firewall;
- enforcing strong password policies;
- configuring `sudo` with strict rules;
- creating a monitoring script that runs automatically every 10 minutes.

The project is not only about creating a working machine, but also about being able to explain every configuration choice during the defense.

---

## Instructions

### Required files
At the root of the repository, you must have:
- `README.md`
- `signature.txt`

### Required environment
- VirtualBox or UTM
- Debian stable or Rocky Linux stable
- a properly configured virtual machine
- a valid disk signature in `signature.txt`

### What must be done
1. Install a minimal Linux server in a virtual machine.
2. Configure encrypted partitions using LVM.
3. Create the required user and groups.
4. Configure the hostname correctly.
5. Install and configure SSH on port `4242`.
6. Configure firewall rules:
   - `ufw` for Debian
   - `firewalld` for Rocky Linux
7. Configure strong password policy.
8. Configure `sudo` with the required restrictions.
9. Set up the `monitoring.sh` script and run it every 10 minutes with `cron`.
10. Ensure the system matches the subject requirements at evaluation time.

---

## My setup choices

### Operating system choice: Debian
I chose Debian because it is stable, lightweight, and easier to understand for a first server administration project. It provides a clean base, which makes it easier to focus on security and system setup instead of spending time on unnecessary complexity.

#### Advantages of Debian
- Stable and predictable release cycle
- Large community and extensive documentation
- Simple and efficient package management with `apt`
- Easier for beginners to learn system administration
- Good fit for a minimal and secure server

#### Disadvantages of Debian
- Packages may be older than in less stable distributions
- Less enterprise-oriented than Rocky Linux
- Some advanced security tools may feel simpler, but less granular than enterprise alternatives

### Why not Rocky Linux?
Rocky Linux is a strong choice for enterprise-style environments, but for this project I preferred Debian because of its simplicity and documentation quality. Rocky usually brings more complexity with SELinux and firewalld, which is useful for learning later, but not necessary for a first project.

---

## Main design choices

### 1. Partitioning and encryption
I used LVM with encryption to organize the disk efficiently and securely.

The system is split into logical volumes such as:
- `/`
- `/home`
- `swap`

This design provides:
- better control over disk usage;
- easier resizing in the future;
- improved isolation between system areas;
- protection of data at rest through encryption.

### 2. Security policies
The system is hardened according to the subject requirements:
- SSH is moved to port `4242`
- root login via SSH is disabled
- UFW allows only the required port
- password policy is enforced through system configuration
- `sudo` is restricted, logged, and configured with a custom security setup
- AppArmor is enabled at startup

### 3. User management
The system contains:
- the root user
- a user with my login
- the required groups such as `sudo` and `user42`

During the evaluation, a new user can be created and added to the `evaluating` group.

### 4. Installed services
Only the services needed by the subject are installed:
- `ssh`
- `sudo`
- `ufw`
- `cron`
- `apparmor`

This keeps the machine minimal and easier to secure.

---

## Comparisons

### Debian vs Rocky Linux

| Topic | Debian | Rocky Linux |
|---|---|---|
| Family | Debian-based | RHEL-compatible |
| Package manager | `apt` | `dnf` |
| Mandatory access control | AppArmor | SELinux |
| Firewall tool | UFW | firewalld |
| Beginner friendliness | High | Medium |
| Enterprise focus | Medium | High |
| Main advantage | Simplicity and stability | Enterprise-like environment |

#### Short conclusion
Debian is a great choice for a first secure server because it is stable, well documented, and easier to configure. Rocky Linux is stronger for enterprise environments, but also more complex.

### AppArmor vs SELinux

| Topic | AppArmor | SELinux |
|---|---|---|
| Policy model | Path-based | Label-based |
| Complexity | Simpler | More complex |
| Typical usage | Easier to configure | More powerful and granular |
| Default on | Debian/Ubuntu | Rocky/RHEL |
| Best for | Beginners and quick hardening | Advanced security environments |

#### Short conclusion
AppArmor is easier to understand and manage, which is why it fits this project well. SELinux is more advanced and very powerful, but harder to configure correctly.

### UFW vs firewalld

| Topic | UFW | firewalld |
|---|---|---|
| Usability | Very simple | More advanced |
| Rule model | Direct rules | Zones and services |
| Typical distro | Debian/Ubuntu | Rocky/RHEL |
| Best for | Small, minimal servers | More dynamic server setups |

#### Short conclusion
UFW is enough for this project because only one port needs to be open. firewalld is excellent for more complex setups, but it is less straightforward.

### VirtualBox vs UTM

| Topic | VirtualBox | UTM |
|---|---|---|
| Platform support | Windows, Linux, macOS | Best on Apple Silicon |
| Use case | Standard virtualization tool | Great alternative on Mac M1/M2 |
| Ease of use | Common and well known | Simple and convenient |
| Typical choice for project | Very common | Used when VirtualBox is unavailable |

#### Short conclusion
VirtualBox is the most standard option for Born2beroot. UTM is a good alternative on Apple Silicon where VirtualBox support may be limited.

---

## Monitoring script

The file `monitoring.sh` is a Bash script that displays system information on all terminals every 10 minutes. It is launched at startup and then repeated by `cron`. The output is broadcast with `wall`.

The script shows:
- operating system architecture and kernel version
- number of physical CPUs
- number of virtual CPUs
- RAM usage and percentage
- disk usage and percentage
- CPU load
- last reboot date and time
- whether LVM is active
- number of active TCP connections
- number of logged-in users
- IPv4 address and MAC address
- number of commands executed with `sudo`

### Why this script matters
This script demonstrates:
- basic shell scripting;
- system monitoring;
- dynamic value calculation;
- scheduled execution with `cron`;
- output broadcasting with `wall`.

---

## Useful commands

These commands are useful during setup, verification, and evaluation:

hostnamectl
- Displays the current hostname and system identity.

cat /etc/os-release
- Shows the Linux distribution name and version.

### Disk and partition checks

lsblk
- Shows block devices, LVM volumes, and mount points.

fdisk -l
- Displays disk partition tables and partition layout.

blkid
- Shows UUIDs and filesystem types for block devices.

mount
- Shows which filesystems are currently mounted.

### User and group checks

whoami
- Prints the currently logged-in user.

id
- Shows the user ID, group ID, and all groups for the current user.

groups
- Shows the groups of the current user.

groups <username>
- Shows the groups of a specific user.

getent group sudo
- Displays the members of the sudo group.

getent passwd <username>
- Shows account information for a specific user.

### Password policy checks

chage -l <username>
- Displays password expiration settings such as max age, warning days, and minimum days.

sudo passwd <username>
- Changes a user password and helps test whether the password policy is enforced.

### SSH checks

sudo systemctl status ssh
- Checks whether the SSH service is running.

ss -tunlp
- Shows listening ports and the processes using them.

ssh <username>@<ip_address> -p 4242
- Connects to the VM through SSH on port 4242.

### Firewall checks

sudo ufw status
- Shows whether UFW is active and which rules are enabled.

sudo ufw status verbose
- Shows detailed UFW status and rules.

### AppArmor checks

sudo aa-status
- Displays the AppArmor status and loaded profiles.

sudo systemctl status apparmor
- Checks whether AppArmor is running.

### Sudo checks

sudo -l
- Shows what commands the current user can run through sudo.

sudo ls /var/log/sudo/
- Checks whether the sudo log directory exists.

sudo cat /var/log/sudo/*
- Displays the sudo logs and command history.

### Cron and monitoring script

sudo systemctl status cron
- Checks whether cron is running.

crontab -l
- Lists the current user's cron jobs.

sudo crontab -l
- Lists root's cron jobs.

bash monitoring.sh
- Runs the monitoring script manually.

### Network and resource checks

who
- Shows logged-in users.

w
- Shows who is logged in and what they are doing.

free -m
- Displays memory usage in megabytes.

df -h
- Displays disk usage in a human-readable format.

uptime
- Shows system uptime and load average.

ip a
- Displays network interfaces, IP addresses, and MAC addresses.

### Restart and persistence checks

sudo reboot
- Reboots the machine to verify that the configuration persists after restart.

### System information

uname -a
- Shows the kernel version, architecture, and general operating system information.

---

## How to verify the project during defense

During the evaluation, the reviewer may ask to:
- change the hostname and reboot;
- create a new user;
- assign the user to a group;
- show password policy settings;
- show active firewall rules;
- add and remove a temporary firewall rule;
- verify SSH access;
- prove that root login via SSH is disabled;
- explain the monitoring script;
- stop the monitoring script without editing it;
- show that `signature.txt` matches the disk signature.

---

## Resources

### Documentation
- Debian documentation: https://www.debian.org/doc/
- AppArmor documentation: https://apparmor.net/
- UFW documentation: https://help.ubuntu.com/community/UFW
- Linux manual pages:
  - `man apt`
  - `man sudoers`
  - `man ufw`
  - `man crontab`
  - `man hostnamectl`
  - `man lsblk`
  - `man chage`
  - `man passwd`
  - `man ssh`

### Learning references
- 42 Born2beroot subject
- 42 correction sheet
- Linux administration tutorials
- Debian administration guides
- Bash scripting references

### AI usage
AI was used to:
- help structure and improve this README;
- compare Debian, Rocky Linux, AppArmor, SELinux, UFW, firewalld, VirtualBox, and UTM;
- prepare defense questions and answers;
- write concise explanations for commands and evaluation steps.

AI was not used to perform the actual VM installation or configuration.

---

## Signature

The virtual machine disk signature is stored in `signature.txt` at the root of the repository.


