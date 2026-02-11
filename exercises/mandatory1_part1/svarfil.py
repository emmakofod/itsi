#!/usr/bin/python3

"""
Challenge answers for IT-Security Mandatory Part 1
Student: emma673r

How to use:
1. Start python3 interactive mode
2. import challenge
3. game = challenge.client(ip_address="cybergame.dk", port=29594)
4. game.login("emma673r", "ITSI-F26")
5. import svarfil as answer
6. game.answer(0, answers.answer0(game.data(0)))
"""

def answer0(data):
    """Question 0: Resend the text that is submitted in data as the answer"""
    return data

def answer1(data):
    """Question 1: The answer is the data multiplied with 2"""
    return data * 2

def answer2(data):
    """Question 2: The answer is the data in uppercase"""
    return data.upper()

def answer3(data):
    """Question 3: Return the text in data in the reverse order"""
    return data[::-1]

def answer4(data):
    """Question 4: Return the sorted list"""
    return sorted(data)

def answer5(data):
    """Question 5: Return a list containing only the first 3 elements"""
    return data[:3]

def answer6(data):
    """Question 6: Return a list where each number is multiplied with 5"""
    return [ item*5 for item in data]

def answer7(data):
    """Question 7: Return the value of the 6th element"""
    return data[5]

def answer8(data):
    """Question 8: Return a sorted list, where the duplicates are removed"""
    return sorted(set(data))

def answer9(data):
    """Question 9: Replace 'be' in the data with 'python'"""
    return data.replace("be", "python")

def answer10(data):
    """Question 10: The answer is the whole sentence with the word 'star' spelled backwards"""
    words = data.split()
    return " ".join(["rats" if word == "star" else word for word in words])

def answer11(data):
    """Question 11: Return a list containing 20 values starting with the number in data and incrementing with 5"""
    return [data + i*5 for i in range(20)]

def answer12(data):
    """Question 12: The data is a list of tuples containing ip-addresses and number of connections. return the number of connections for ip-address 192.168.1.212"""
    for addr, cons in data:
        if addr == "192.168.1.212":
            return cons

def answer13(data):
    """Question 13: The answer is the total sum of all the numbers in the list"""
    return sum(data)

def answer14(data):
    """Question 14: Return a list containing tuples with names and phonenumbers [(\"name1\",\"phone1\"),(\"name2\",\"phone2\")...]"""
    result = []
    for pair in data.split(","):
        (name, number) = pair.split(":")
        result.append((name, number))
    return result

def answer15(data):
    """Question 15: Return the dictionary with the entry for \"192.168.1.243\" removed"""
    data.pop("192.168.1.243")
    return data

def answer16(data):
    """Question 16: The answer is the sentence where each word is in reverese (the words keep their place in the sentence)"""
    return ' '.join([word[::-1] for word in data.split()])

def answer17(data):
    """Question 17: return a list containing 10 tuples of the ones found in data"""
    return [data] * 10

def answer18(data):
    """Question 18: Add a new item to the dictionary with the key \"yellow\" and the value 22"""
    data["yellow"] = 22
    return data

def answer19(data):
    """Question 19: return a set containing all unique ip addresses in data"""
    return {line.split()[0] for line in data.split("\n") if line.strip()}

def answer20(data):
    """Question 20: return a dictionary containing all status codes (in string)  as key, and how many times their occured (in int) as value"""
    status_counts = {}
    for line in data.split("\n"):
        parts = line.split()
        if len(parts) > 8:
            status = parts[8]
            status_counts[status] = status_counts.get(status, 0) + 1
    return status_counts

def answer21(data):
    """Question 21: return the average size (in int) of all responses with status 200 """
    sizes = []
    for line in data.split("\n"):
        if line.strip():
            parts = line.split()
            if len(parts) > 9 and parts(8) == "200":
                size = parts[9]
                if size == "-":
                    break
                else:
                    sizes.append(int(size))

    return sum(sizes) // len(sizes)  # // for integer division

def answer22(data):
    """Question 22: return the number of times (in int) an images of the type png is in the response"""
    count = 0
    for line in data.split("\n"):
        if line.strip():
            parts = line.split()
            for part in parts:
                if ".png" in part.casefold():
                    count += 1
    return count

## can also just be .. if you stop overthinking everything
def answer22_v2(data):
    return data.lower().count(".png")

def answer23(data):
    """Question 23: convert this list to a dictionary where the episode number is the key (ie: \"Episode I\") and the name is the value (ie: \"The Phantom Menace\")"""
    episodes = {}
    for name, number in data:
        episodes[number] = name
    return episodes

def answer24(data):
    """Question 24: return a sorted list (in int) containing the numbers 1-100, but without the numbers divideble with the number in data (ie. the numbers 3,6,9,12... should not be there)"""
    return [num for num in range(1, 101) if num % data != 0]


def answer25(data):

    import hashlib
    import itertools

    """Question 25: this sha1 hash was found. the system it comes from normally uses 4 character kodes, consisting of a-z in lowercase"""
    vic_hash = data
    
    # Generate all 4-character combinations of a-z (could prob do a loop instead of using this library)
    for combo in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=4):
        word = ''.join(combo)
        # Hash it (need the hashlib library - can't see how i could do without)
        hash_obj = hashlib.sha1(word.encode())
        current_hash = hash_obj.hexdigest()
        
        # Check if it matches
        if current_hash == vic_hash:
            return word
        
# word = funi

def answer26(data, test=None):
    """Question 26: the data provided contains a tuple,
    where first element is a
    sha256. The second element contains a dictionary
    (created by scrapping the victims facebook)
    of words an values that the password could be generated from.
    Assume that the password length is 8 characters,
    and that the system requires lowercase,
    uppercase letters and numbers."""
    
    import hashlib
    import itertools
    import ast

    # STEP 1 — Parse the provided string safely into Python data

    # The game gives us data:
    # '(("hash"),[(tuple1),(tuple2),...])' - NO DICT though..
    #
    # Use ast.literal_eval to safely convert string → Python object
    # (literal_eval is safe because it only parses literals, not code) - have seen other methods that also
    # parse executables and runs them - don't want to risk anything.

    parsed = ast.literal_eval(data)

    vic_hash = parsed[0]        # SHA256 to match (som many billions possiilities - no brute force - use human thinking and engineering)
    scraped_data = parsed[1]         # The list of tuples with vics facebook inmportant info scraped


    # STEP 2 — Flatten + put tokens in boxes

    # Extract all words + numbers -> separate lists ( != dta types, everytiong into its own box)

    words = []
    numbers = []

    for group in scraped_data:
        for token in group:
            if token.isdigit():
                numbers.append(token)
            else:
                words.append(token)

    # Normalize capitalization for consistency
    # Humans usually capitalize names - as a fellow human i would know, its a guessing and patience game
    words = [w.capitalize() for w in words]


    # STEP 3 — Validation

    # Enforce CONSTRAINTS BEFORE hashing
    # so 8 chars, upper + lower case + ints
    # that way no "bad" guesses taken into accoutn

    def make_valid_pwd(pwd):
        return (
            len(pwd) == 8 and
            any(c.islower() for c in pwd) and
            any(c.isupper() for c in pwd) and
            any(c.isdigit() for c in pwd)
        )


    # STEP 4 — Hash comparison

    # SHA256 is one-way, no reversible etc etc etc 
    # We hash each candidate and compare to target. so we need "good" guesses, educated guesses, human like guesses
    # so i have to try and be Lars and how i would make my pwd as someone who .. maybe? dont kno about it idk

    def matches_hash(pwd):
        return hashlib.sha256(pwd.encode()).hexdigest() == vic_hash



    # STEP 5 — Structured Combination Strategy

    #
    # Rule! no brute force, so it has to be something that we student can work through and "guess" - a pettern
    # patterns are good, they are guessable
    #
    # so:  generate:
    #
    #   word_slice + word_slice + number_slice
    # like ive tried a lot before this function so ive tried other patterns, this one won, so this one i keep obvs.
    #
    # This models real human password behavior:
    #   - name fragment
    #   - surname fragment
    #   - important year - my guy had a child i suppose "JAN" and the year is the most important date
    #
    # THE ONE that worked:
    #   LaHa2014 - i feel ike i couldve guessed it, but nvm its still cool 
    #
    # This is:
    #   Lars[:2] + Hansen[:2] + 2014


    tested = 0  # Debugging, i love data

    for w1, w2 in itertools.permutations(words, 2):

        for n in numbers:

            # Try different slice lengths of both words and number
            for i in range(1, len(w1) + 1):
                for j in range(1, len(w2) + 1):
                    for k in range(1, len(n) + 1):

                        candidate = w1[:i] + w2[:j] + n[:k]
                        tested += 1

                        # Check constraints BEFORE hashing - dont need to use extra memory or wathever on passwords not valid
                        if make_valid_pwd(candidate):

                            if matches_hash(candidate):
                                print(f"[+] Password found after {tested} attempts")
                                return candidate

    # If nothing found - but like i found it hehe
    print(f"[-] No password found after {tested} attempts")
    return None

# LaHa2014 - hahahah


def answer27(data):
    """Question 27: return the missing layer"""
    return "network"

def answer28(data):
    """Question 28: return the mac address"""
    return "a4:67:06:8d:83:a1"

def answer29(data):
    """Question 29: Use cap.pcapng from the network challenge. Analyse the paket(data is the packet no). What is the length of the data transmitted in this paket (in bytes)."""
    return 39

def answer30(data):
    """Question 30: Use cap.pcapng from the network challenge. Data is a path for a HTTP request. What is Ack (raw) in the packet that acknowledges this file?"""
    return 3775708311
# http -> look for style.css request, packet 1611 req, 1626 response and
# packet 1627 acknowledges getting http \style.css data/response

def answer31(data):
    """Question 31: Use cap.pcapng from the network challenge. What domain name is here?"""
    return "0.client-channel.google.com"
# dns.a == 74.125.143.189 - and look at dns response

def answer32(data):
    """Question 32: KEA has been infiltrated by thieves.
    Luckily, they were chased away, and dropped what they stole. 
    Your task is to use the recorded log data to figure out what
    floor and room number the thieves ended up.
    ServiceDesk gave you the following legend:
    ^ = +1 floor, v = -1 floor, < = -1 room number, > = +1 room number.
    Answer with a tuple containing the floor and room number,
    considering you start on floor 0 and room 0."""
    floor = 0
    room = 0
    
    for char in data:
        if char == "^":
            floor += 1
        elif char == "v":
            floor -= 1
        elif char == "<":
            room -= 1
        elif char == ">":
            room += 1
    
    return (floor, room)

"""
Also thouhgt of count ...
so here is extra:

def answer32(data):
    floor = data.count("^") - data.count("v")
    room = data.count(">") - data.count("<")
    return (floor, room)

could also probably store what the character mean in a dict with the value.. and use those
anyways i like for loops
"""

def answer33(data):
    """Question 33: ServiceDesk calls you and tells you they gave you an outdated legend for the log data.
It was from before KEA realised that having negative room numbers doesn't make sense.
That means the room numbers wrap back around. For example if you are by room 0 and you move left (<), you will be by room 100 and vice versa.
Furthermore the legend states that if log entries are repeated, they increment in value. 
For example if you see >>>, the first ">" is 1, the next ">" is 2, and the last ">" is 3, totalling 6 rooms moved. 
This incremenation resets if the current log entry differs from the previous entry."""
    floor = 0
    room = 0
    incr = 1
    prev_char = None
    
    for char in data:
        if char == prev_char:
            incr += 1
        else:
            incr = 1
        
        if char == "^":
            floor += incr  # Floors DON'T wrap
        elif char == "v":
            floor -= incr  # Floors can go negative
        elif char == "<":
            room = (room - incr) % 101  # ONLY rooms wrap
        elif char == ">":
            room = (room + incr) % 101  # ONLY rooms wrap
        
        prev_char = char
    
    return (floor, room)

# had ifs 100 -> 0 and reverse, but knew there was a cleaner way
# and modulo is nice -so i adopted it


## svar til 32 er >>> answer32(game.data(32)) = (-6, 7)
# så er forvirret over hvorfor det er rooms der ikke kan være negative (real ligfe i get it),
# men i det tilfæld, så var det floors der var negative