This is a CLI chat client for the game hackmud based around the ability to chat via JSON.

How to use:
```
  /user <user> -> switch to user, invalid user will crash
  /channel <channel> -> switch channel, invalid channel will make the program very confused
  /baud <int> -> client will poll for changes every <int> seconds - deafult is 3
  /quit -> quit the program
  {coming soon} /help -> display this
```

THIS PROJECT REQUIRES THE 'requests' LIBRARY
To install this library, run:
```
  pip3 install requests
```
```
  pip install requests
```
depending on your installation of pip.
