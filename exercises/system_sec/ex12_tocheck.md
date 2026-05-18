Opgaver 12:

12.a sXID

![sxid setup shows that it works - if i add a file in the testdir, it detects the changes](image-37.png)


_____


12.b Tripwire (ligner meget sXID — detekterer ændringer i filer):
bashsudo apt install tripwire
sudo tripwire --init
# opret/ændr en fil i protected dir
sudo tripwire --check


![successfully generated](image-38.png)
![report done](image-39.png)
![check ændringer i rapport ](image-40.png)




12.c PortSentry (detekterer og reagerer på nmap-scans):
bashsudo apt install portsentry
# edit /etc/portsentry/portsentry.conf
# scan fra Kali med nmap, se hvad PortSentry opdager

![kali scan before config](image-41.png)
![kali nmap efter conf](image-43.png)
![portsntry viser 1 nmap scan fra mon kali ip](image-42.png)
![kali blocked](image-44.png)


12.d — SquidProxy (proxy-filter på indhold og domæner).
![added regler](image-48.png)
![firefox procy sw](image-46.png)

![virker kun pga https limitiation](image-50.png)

squid dstdomain ACL virker kun på HTTP
Når en side redirecter til HTTPS, går forbindelsen via CONNECT tunnel som Squid ikke kan inspicere