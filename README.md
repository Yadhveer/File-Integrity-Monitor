# File-Integrity-Monitor

This is a basic python based application in the field of information security. This is based on hashing a text file using SHA-256 and storing the same in a mysql database. The stored hash is then cross checked with a new hash that is generated on running the program and then gives an alert if the hash changes, as that means that its file has changed.

I have created a local MySQL server and have connected it to my python code such that the user can insert, update or delete files and their hashes if they wish to change their files.
