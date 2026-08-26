## Wireshark Lab HTTP (1)

Enter the url http://kallas.dk in your web browser and capture the corresponding HTTP
packets.
Then, answer the following questions:

1. Which version of HTTP is your browser running? What about the server?
   my browser (aka the client) is running http v1.1 and the server is also running 1.1.
   ![http versions](image-2.png)

2. What languages (if any) does your browser indicate that it can accept to the server?
   Accept-Language: en-US,en;q=0.5\r\n
   so english us and english as default.
   ![language header request](image-3.png)

3. What is the status code returned from the server to your browser?
   200 OK, means everything went well. You can see it at different emplacements
   ![status code response](image-4.png)

4. When was the HTML file that you’re retrieving last modified at the server?
   Last-Modified: Wed, 26 Aug 2020 19:57:36 GMT\r\n
   ![last modified date](image-5.png)

5. How many bytes of content are being returned to your browser?
   We get a 18 bytes response.
   ![size of returned content](image-6.png)

![whole wireshark screen](image-7.png)

## Wireshark Lab HTTP (2)

The url http://www.kallas.dk/basic.php is password protected.

- Username: guest
- Password: guest

Capture the corresponding HTTP packets and examine the Wireshark output.

Then answer the following questions:

1. How many requests/responses where generated?
   We have 3 pairs. one for the /basic.php but it needs auth, so i got a 403 - unauthorized error, then i logge din, whihc prompted the second pair, i had teh right credentials so i got me a response 200 OK to see the content. The last pair is a little bit irrelevant i guess, its to get th favicon file, which we btw dont get 404 not found.

2. What is the server’s response (status code and phrase) in response to the initial HTTP GET message from your browser?
   403, not authorized (i didnt have the credentials input yet.)

3. When your browser’s sends the HTTP GET message for the second time, what new field is included in the HTTP GET message?
   "Credentials: guest:guest"
   the credentials that i used to give me auhtorization to access that page.

4. You may see somewhere a string that looks like Basic Z3Vlc3Q6Z3Vlc3Q=. What is this?
   I would guess that it is the credentials, that got encoded in Base64.
   guest:guest encoded in Base64, is indeed this string : Z3Vlc3Q6Z3Vlc3Q= .

![wireshark screenshot](image-1.png)

## Wireshark exercise ek.dk

https://www.ek.dk/english/knowledge-and-inspiration/wireshark-1

![test results](image.png)
