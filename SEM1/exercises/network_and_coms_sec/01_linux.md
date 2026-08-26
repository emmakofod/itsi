## [LINUX.01] Exercises — Command Answers

Look in kali vm for the file.

```bash
# Task 1: Number of unique IP addresses
cut -d ' ' -f1 access.log | sort | uniq | wc -l > task1.txt

# Task 2: Unique IPs that did NOT make GET requests
cut -d ' ' -f1,6 access.log | grep -v GET | cut -d ' ' -f1 | sort | uniq | wc -l > task2.txt

# Task 3: Hits in December 2019
cut -d ' ' -f4 access.logh | grep 'Dec/2019' | wc -l > task3.txt

# Task 4: IPs of 20 biggest downloads (bytes desc)
cut -d ' ' -f1,10 access.log | sort -rnk 2 | head -n 20 | cut -d ' ' -f1 > task4.txt

# Task 5: Total 404 and 401 responses
cut -d ' ' -f9 access.log | grep '404\|401' | wc -l > task5.txt
```
