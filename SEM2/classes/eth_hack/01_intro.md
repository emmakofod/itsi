 virksomheden kan blive nedlagt = ekonomi, alle secrets kan leaked, GDPR brud 


Retroforum:
>$RETRO=127.17.0.3

>nikto $RETRO

> curl $RETRO

$RETRO | grep -E "flag{.*}"

gobuster (directory buster)

> gobuster dir --url $RETRO --wordlist /usr/share/wordlist/dirb/common.txt --extensions-file /usr/share/wordlist/dirb/extensions_common.txt --output gobuster.txt

cat gobuster.txt | grep -E ": 200" | uniq

curl $RETRO/backup.sql | grep -E "flag{.*}"


