# btassessment
Because GitHub API isn't too shabby.

## What is this for?
This project utilizes the GitHub API via Python to analyze top level details for a public facing organization. From the top level object, URLs which contain further information (such as repos and events) are gathered and analyzed with respect to their status codes. If the status code returns 200, the repository ids and names are listed, as well as detailed event information for those repositories. After this information has been displayed in the user's console (my apologies in advance), some verification is performed:

1. The top level detail object is analyzed to ensure the updated date is equal to or greater than the created date, and a PASS/FAIL is generated
2. The top level detail object is analyzed for the reported number of public repos and compared to the length of the repository list, and a PASS/FAIL is generated

## Why are you doing this?
In short, I really like programming. I stayed up until 5 AM doing this because it was challenging and fun. I recognize I have a long way to go in terms of my usage of object oriented principles; however, with the constraints of current knowledge and time, I attempted to adhere as closely as possible to an important OOP principle - DRY. I've already started working on version two which codifies the project into definitive classes.

## How do I use this thing?
This was developed for python version 3.7.3. You should be good pulling the project down and running the project in your IDE. However, here's the output of `pip freeze` for my virtual environment:

```
certifi==2019.6.16
chardet==3.0.4
Deprecated==1.2.6
idna==2.8
PyJWT==1.7.1
requests==2.22.0
urllib3==1.25.3
wrapt==1.11.2
```

Any and all comments or suggestions are greatly appreciated!
