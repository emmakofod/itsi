Exercise 8.1a
• Check/install SSH Server on your server machine.
• Check/install SSH Client on your client machine.
• Make sure you have user1, user2 and user3 as accounts
on both machines.
• Login a user to the server over SSH.
• Check/Disable SSH root login.
• Configure SSH server to port 22123.
– Test login over that port.
– Test standard scan with nmap. Do you see the SSH service?
• Configure SSH to only accept group13.
– Test login.
• Can you do the above steps for any central service like a
CRM system, Billing system, HR system,…?


Exercise 8.1b
• Create an SSH public/private key pair for user2.
– Add a passphrase to the private key.
– Check and view the keys.
• Upload the public key to the SSH server.
• Test logging in over SSH.
– Verify that the key pair is used.
– Verify the passphase is used.
– Check and view the public key on the server.
• Disallow password login. Must use key.
• Why is this login more secure than a password?
• Is crypto-key based login a second factor, 2FA?
• Can you add 2FA to any central service?