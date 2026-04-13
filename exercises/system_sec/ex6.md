## Exercise 6.1 Overview

1. Install Ubuntu Server VM
2. Install + configure LDAP server (`slapd`)
3. Install LDAP Account Manager (web UI)
4. Add groups: `sales`, `economy`, `support`
5. Add users: `John Doe`, `Peter Jensen`, `Alice Sorensen` (use high UIDs!)
6. Install + configure LDAP client on Ubuntu Desktop VM
7. Test: log in to client using LDAP user credentials


![etup](image-19.png)
![slapcat](image-20.png)
![lam login page](image-21.png)



![groups](image-23.png)
![users](image-22.png)

> getent passwd
![getent passwd on ubuntu desktop](image-24.png)

![login as jdoe](image-25.png)
![whoami + id on jdoe](image-26.png)