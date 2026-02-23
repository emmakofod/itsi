# The Game - Question 26 - Cracking a Password from a Hash

## My Journey Through This Nightmare, this gave me the best coding high i've ever had!!!

### What I Had to Work With

I got a SHA-256 hash and some "scraped Facebook data":

```
Hash: 0ba128bd856006948e7c57b714586bf43199aa898cc2bcd25141d951a34664a8

Data:
("Lars","Hansen","05","09","1984")
("fido")
("jan","08","08","2014")
("barcelona","fodbold")
```

The password had to be:

- Exactly 8 characters
- Have uppercase letters
- Have lowercase letters
- Have numbers

### How I Started (And Failed... A LOT)

At first, I thought: "Okay, this is probably just Lars + his birth year, right?"

So I tried the obvious stuff:

- Lars1984
- Fido2014
- Hansen84

**None of them worked.**

Then I got creative and tried:

- Name + pet: FidoLars, LarsFido
- Dates: Lars0509, Fido0808
- Shortened words: Barca084, Fodbold1

**Still nothing.**

I literally tested THOUSANDS of combinations. I tried:

- Different capitalizations (lArs1984, LaRs1984)
- Numbers in the middle (La19rs84)
- Leet speak (L4rs1984, H4nsen84)
- Meta passwords (Passw0rd, Facebook)
- Even completely random common passwords

At one point I had tested over 50,000 combinations and had used chat and claude, and they told me to give up. But maybe i needed sleep.
I sent messages to the 2 team mates that solved it, but i dont think they saw it, it was on fronter... and then i sent a last dicth effort message to my teacher, even though he had said he didnt want to give the solution out. Just hoping for the best. And goddamn, was it a night to sleep on it, the tip i got from the teacher or just pure luck.. i am happy i didn't give up. I am happy i wanted to solve it and went for it.
It makes me feel accomplished. I am not the best, and I will surely never be the best, but i feel like i prove myself that i can follow through and make something "impossible" happen. I am proud of myself. Even though its "just" a challenge from the intro course.

### The Clues That Changed Everything

**Clue 1: Question 25**

The answer to question 25 was "funi" - which sounds like "funny" when you say it out loud. That made me realize maybe this wasn't straightforward. Maybe it was a pun or something fun or unexpected.

**Clue 2: The "Dictionary" That Wasn't**

The question said the data was a "dictionary" but it was actually a list of tuples. I thought this might be a hint that something wasn't what it seemed.

**Clue 3: The Teacher's Hint**

My teacher finally gave me a hint:

> "You need to tokenize the keywords and make combinations."

That word - **tokenize** - completely changed how I was thinking.

I wasn't supposed to just use whole words. I was supposed to break them into PIECES and recombine them!

### What "Tokenize" Actually Meant

Instead of thinking:

- "Lars" + "1984"

I should think:

- "La" + "Ha" + "2014"

Breaking words into smaller chunks:

- Lars → La, Lar, Lars, ar, ars, rs
- Hansen → Ha, Han, Hans, Hansen, an, ans, nsen
- 1984 → 19, 84, 198, 984

Then combining these chunks in different ways to make 8-character passwords.

### My Strategy After the Hint

I wrote code to:

1. Extract all possible "tokens" (chunks) from the data
2. Try combining 2-4 tokens to make exactly 8 characters
3. Test different capitalization patterns
4. Hash each combination and compare to the target

For example, from "Lars" and "Hansen" and "2014", I could make:

- La + Ha + 2014 = LaHa2014 ✓ (8 chars!)
- Lar + sen + 84 = Larsen84 ✓ (8 chars!)
- Han + fi + do + 14 = Hanfido14 ✓ (8 chars!)

### The Breakthrough

After testing tokens systematically, I found it:

**LaHa2014**

Breaking it down:

- **La** = first 2 letters of Lars
- **Ha** = first 2 letters of Hansen
- **2014** = the year his child was born

It's:

- 8 characters exactly
- Has uppercase (L, H)
- Has lowercase (a, a)
- Has numbers (2014)

**It worked!**

### Why This Password Makes Sense

If you're Lars Hansen and you need to make a password:

- You want something memorable
- You can't use "LarsHansen2014" (too long - 14 characters)
- So you shorten it: La + Ha + 2014
- It's meaningful to you but looks random to others

People do this ALL THE TIME. They think they're being clever by truncating their personal info, but it's actually super predictable once you know the pattern.

### What I Learned

**About Password Cracking:**

- The hash itself (SHA-256) is completely secure - I didn't "break" the encryption
- The weakness was human behavior - people reuse personal information
- When you know someone's context (name, birthday, kids, pets), the number of realistic passwords drops from trillions to hundreds

**About Problem Solving:**

- Sometimes you need to completely change your approach (I went from "try obvious combinations" to "tokenize and recombine")
- Asking for help/hints is smart, not cheating
- Persistence matters - I was ready to quit multiple times but kept going

**About Security:**

- Never use personal info in passwords!
- Don't truncate predictably (first 2 letters of each word is common)
- Use a password manager with random passwords
- Make passwords LONG (12+ characters minimum)
- Birthday years are especially bad because they're public info

### My Actual Process (The Real Numbers)

Total attempts before finding the answer: **Way too many to count**

I tried:

- ~100+ manual guesses first
- ~50,000+ programmatic attempts with different patterns
- Then finally focused tokenization after the hint
- Found the answer after implementing smart token combinations

The key was reducing the search space from "all possible 8-character combinations" (trillions) to "realistic human password patterns based on available data" (hundreds).

### Final Thoughts

This challenge reinforced that cybersecurity isn't just about knowing technical stuff. It's about understanding how humans think and behave.

The most secure encryption in the world doesn't help if your password is based on predictable personal information.

Also: You should never using personal info in passwords again. This was "way too easy" once I knew the pattern!

### Technical Details

**Hash Algorithm:** SHA-256  
**Password Found:** LaHa2014  
**Method:** Tokenization + Behavioral Modeling  
**Search Space Reduction:** From ~218 trillion to ~500 realistic candidates  
**Time Spent:** Around 5 hours
**Final Score:** 34/34 🎉

---

_Emma - ITSI-F26_  
_February 2026_
