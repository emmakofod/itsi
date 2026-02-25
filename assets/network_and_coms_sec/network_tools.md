# Linux 101 — Command Line Tools

## File Inspection

### `man` — Manual / help pages
Almost every tool has built-in documentation. Always check this first.
```bash
man ls
man unzip
```

### `file` — Identify file type by header (not extension)
```bash
file access.zip
```

---

## Viewing & Paginating Files

### `more` — Basic viewer (forward only, one page at a time)
```bash
more access.log
```

### `less` — Advanced viewer (navigate back and forth) ⭐ preferred
```bash
less access.log
less -N access.log              # show line numbers
less +5000 access.log           # start at line 5000
less +F /var/log/messages       # auto-refresh (like tail -f) — or press Shift+F inside
less +/POST access.log          # open and highlight pattern
```

### `head` — Show beginning of file (default: 10 lines)
```bash
head access.log
head -n 35 access.log           # show first 35 lines
head -c 50 access.log           # show first 50 bytes/characters
head -n 35 access.log | less -N # pipe to less with line numbers
```

### `tail` — Show end of file (default: 10 lines)
```bash
tail access.log
tail -n 35 access.log
tail -f /var/log/messages       # follow/live-update as file grows
```

### `cat` — Display and concatenate files
```bash
cat /var/log/messages           # display file
cat > my_file.txt               # create new file (Ctrl+D to finish writing)
cat file1.txt file2.txt file3.txt > new_file.txt   # merge files
```

---

## Streams, Pipes & Redirection

### Pipe `|` — Chain commands (output of one → input of next)
```bash
ls -la /etc/ | less
grep POST access.log | head
```

### Redirect `>` / `>>` / `<`

| Symbol | Stream | Description |
|--------|--------|-------------|
| `<` or `0<` | stdin (0) | Read input from file |
| `>` or `1>` | stdout (1) | Write output to file **(overwrites)** |
| `>>` | stdout | Append output to file |
| `2>` | stderr (2) | Write errors to file |
| `2>>` | stderr | Append errors to file |

```bash
ls -la /etc/ > ls_file.txt                    # save stdout
rm missing_file 2> rm_error.log               # save stderr only
rm missing_file 2>> rm_error.log              # append stderr
./program.py < program_input.txt              # feed file as input
echo -e "Dany\n40\n" | ./program.py > out.txt # pipe + save stdout
./program.py > output.txt 2> errors.txt       # stdout and stderr to separate files
```

### `echo` — Print text / feed input to programs
```bash
echo "Hi how are you?"
echo -e "Dany\n40\n" | ./program.py    # -e enables escape sequences (\n = newline)
                                        # -E disables escape sequences (default)
```

### `tee` — Write to stdout AND a file simultaneously
```bash
ls -l | wc -l | tee test.txt           # prints result to screen AND saves to test.txt
```

---

## Searching & Filtering

### `grep` — Search for patterns in text
```bash
grep POST access.log                    # lines containing "POST"
grep POST access.log | head             # first 10 matches
grep -A 2 eth0                          # show 2 lines AFTER match
grep -B 2 eth0                          # show 2 lines BEFORE match
grep -v POST access.log                 # INVERT — lines NOT matching
grep -n POST access.log                 # show line numbers
grep -vn POST access.log | head         # combine flags
grep -f patterns.txt access.log         # load patterns from file

# Practical examples:
sudo ifconfig | grep eth0
sudo ifconfig | grep -A 2 eth0
head -n 500 access.log | grep -f patterns.txt
```

---

## Data Processing & Analysis

### `cut` — Extract columns from delimited data (simple, fast)
```bash
cut -d ' ' -f1 access.log | head       # first column (IP address), space delimiter
cut -d ' ' -f1,4-5 access.log | head   # columns 1, 4, and 5 (IP + date)
```
> `-d` = delimiter, `-f` = field number(s)

### `awk` — More powerful column extraction / scripting
```bash
awk '{print $1" "$4" "$5}' access.log | head    # same as cut example above
```
> `$1`, `$4`, `$5` = column numbers (space-delimited by default)

### `sort` — Sort data
```bash
ls -la | sort                   # alphabetical sort
ls -la | sort -k5               # sort by column 5
ls -la | sort -nk5              # numeric sort by column 5
ls -la | sort -rnk5             # reverse numeric sort by column 5 (desc)
head access.log | sort -rnk10   # sort first 10 lines by column 10 desc
```
> `-k` = column key, `-n` = numeric, `-r` = reverse/desc

### `uniq` — Remove or count duplicate lines
```bash
uniq testfile.txt               # remove consecutive duplicates
uniq -c testfile.txt            # count occurrences
```
> **Important:** `uniq` only removes **consecutive** duplicates — always `sort` first!
```bash
sort testfile.txt | uniq -c     # correct way to count all duplicates
```

### `wc` — Word/line/byte count
```bash
wc access.log                   # lines, words, bytes
wc -l access.log                # lines only (fastest)
ls /etc/ | grep net | wc -l     # count files/dirs containing "net" in /etc/
```

### `split` — Split large files into smaller ones
```bash
split -l 100000 access.log      # split into chunks of 100,000 lines (default: 1000)
split -b 50m access.log         # split by bytes (50MB chunks)
```
> Output files will be named `xaa`, `xab`, `xac`, etc.

---

## Process Management

### Background & foreground jobs
```bash
gedit test.py &     # launch in background immediately
# Ctrl + Z          # suspend running process
jobs                # list all background/suspended processes
fg %1               # bring job 1 to foreground
bg %1               # resume job 1 in background
```

---

## Practical Combinations (Log Analysis)

```bash
# 5 biggest HTTP responses in whole file
sort -rnk10 access.log | head -n 5

# IP addresses of the 5 biggest responses
sort -rnk10 access.log | head -n 5 | awk '{print $1}'

# Count unique IP addresses
cut -d ' ' -f1 access.log | sort | uniq | wc -l

# Count 404 errors
grep ' 404 ' access.log | wc -l
```