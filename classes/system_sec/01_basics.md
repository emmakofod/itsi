# Basics

system security: 
- Company data : data is either at rest or in transit
- trying to protect data at rest:
    - on a company server
    - if system is compromised, data is compromised
    - we need to protect the system to protect the data
- network is data in transit (another course)


Class obj: 
- protect and prevent (main)
    -protect data and assets
    - prevent unauthorized access, changes and misuse
- detect & respond (minor)
    - detect breach (see "the bank job" movie)
    - respond to incident
- recovery (very small part)
    - disaster recovery plan
    - restore data and services

Content of class:
Not system attack class - defense class
Method:
Highly practical class, do exercises etc 
Importance levels:
**What** is this, **how** does this work, **why** is it important (explain this)


## Sec policy

### Structure

Policy is essential - otherwise its just random. Randomness is worse than an enemy, you can't expect anything from randomness.

How to manage, protect and distribute data.
    - business driven, != for every company, depending og their needs and priorities
Set of rules and practices. A least:
    - accesss rules to sys and data
    - software installation rights on sys
    - data permissions
    - recovery from failure 
    - anything nor permitted should be restricted
**Policy that both users and admins must follow**

**General policy**
    - Physical protection, rooms, doors, power outage etc,
    - Admin of servers -> limited team only
    - Any compliance to external rules must e added into the security policy
    - Each server must be registered with at least : location, os version, HW config, services + apps being run
    - All info in management sys mus be up to date

**Configuration policy**
    - any service not used should be removed
    - all access should be logged 
    etc

**Monitoring policy**

etc...


### Examples

**pwd policy**
can be divided in sub-policies
Paswword creation is a sub policy:
    - is user allowed to create own pwd
    - a user should no use same pwd for dif level of account
    - an adm must not use same pwd at work as in private acc on internet
    - min complexity of pwd - not easy to guess
    - changes all default pwd

**pwd protection policy**
    - pwd are confidential info - not shared with anyone
    - pwd not be setn per email or similiar
    - never tell pw on phone or in questionnaires
    - pw hints should not give any hints - bad
    - do not keep pwd written in office
    - do not use remember pwd ft. in apps
    - when in doubt, report incident and change pwd

and so many others

### Why do we have policies
- **Creating a repeatable and consistent process for managing information**
- Educating workforce members around best practices and corporate security protocols
- **Documenting controls to ensure people adhere to security measures**
- Meeting mission-critical **compliance** requirements
- Establishing guidelines for detecting new threats and mitigating new risks
- Giving customers confidence over your org's security posture
- Ensuring appropriate access to IT and data resources on a "as needed" basis 

=> That your process is consistent and repeatable, to ensure quality



## Linux


## Media integrity

Whenever doing an install:
- new software or new version : 
    - integrity check the media, or dl file BEFORE use : checksum, avoiod installing "additional" free features - could be malware 
- new sw with new media
    - maybe also test i sandbox before approval for use in systems
- known sw
    - use the one you have tested before

### How to check for integrity

Hash / Checksum check

## Disk Encryption
Data is "parked" on hard drive.
    - protected by OS controles:
        - spec users are allowed spec access
        - others users no access granted

What is the easiest way to bypass the OS controls if attacker has local access?
- Human engineering, i can pretend to be an "invisible" worker, install own OS, use it for access to disk.

How do you defend against that?
Encrypt your disk, ex LUKS to encrypt partition.
Dont loose the encryption key, so keep a safe record of the key in a safe location.

## Sudo access

## Privilege separation
role based access control 