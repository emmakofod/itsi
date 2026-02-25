## [LINUX.01] Exercises — Command Answers

```bash
# Task 1: Number of unique IP addresses
cut -d ' ' -f1 access.log | sort | uniq | wc -l > task1.txt

# Task 2: Unique IPs that did NOT make GET requests
grep -v '"GET' access.log | cut -d ' ' -f1 | sort | uniq | wc -l > task2.txt

# Task 3: Hits in December 2019
grep '/Dec/2019' access.log | wc -l > task3.txt

# Task 4: IPs of 20 biggest downloads (bytes desc)
sort -rnk10 access.log | head -n 20 | awk '{print $1}' > task4.txt

# Task 5: Total 404 and 401 responses
grep -E ' (404|401) ' access.log | wc -l > task5.txt
```
