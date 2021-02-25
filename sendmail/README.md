Gmail	smtp.gmail.com	587
Outlook / Hotmail	smtp-mail.outlook.com	587
YAHOO Mail	smtp.mail.yahoo.com	587
Verizon	smtp.verizon.net	465
Comcast	smtp.comcast.net	587


>>> msg = 'Hello Wørld'
>>> from_ = 'a@example.com'
>>> to_ = 'b@example.com'
>>> subject = 'Hello'

>>> fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'

>>> server.sendmail(to_, from_, fmt.format(to_, from_, subject, msg).encode('utf-8'))
This will send this message*:

b'From: b@example.com'
b'To: a@example.com'
b'Subject: Hello'
b'Hello W\xc3\xb8rld'
However this workaround will not work if you want to send non-text binary data with your message.

A better solution is to use the EmailMessage class from the email package.

>>> from email.message import EmailMessage
>>> em = EmailMessage()
>>> em.set_content(fmt.format(to_, from_, subject, msg))
>>> em['To'] = to_
>>> em['From'] = from_
>>> em['Subject'] = subject

>>> # NB call the server's *send_message* method
>>> server.send_message(em)
{}
This sends this message; note the extra headers telling the recipient the encoding used:

b'Content-Type: text/plain; charset="utf-8"'
b'Content-Transfer-Encoding: 8bit'
b'MIME-Version: 1.0'
b'To: b@example.com'
b'From: a@example.com'
b'Subject: Hello'
b'X-Peer: ::1'
b''
b'From: b@example.com'
b'To: a@example.com'
b'Subject: Hello'
b'Hello W\xc3\xb8rld'
* Run the command python -m smtpd -n -c DebuggingServer localhost:1025 in a separate terminal to capture the message data.