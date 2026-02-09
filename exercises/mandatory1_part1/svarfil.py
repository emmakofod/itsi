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
                size = parts(9)
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

