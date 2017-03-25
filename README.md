# PythonDownloader


command line download manager.
The manager, called autodownloader, is composed of two components:
    1. Background service (**autodl-service**)
    2. Command line utility to handle the application (**autodl**).

**autodl-service** is executed as a different process, by running the command *./autodl-service.py [max-tasks-number]*
**autodl** is executed by 'user' with the command *./autodl.py <command>*
*add <url> [path]*      Add the URL to the service to download.
                        If path is not given, the current user’s home directory is used instead.
*clear*                 The service will finish its ongoing tasks and not start new ones.
                        All the previously added URLs should be forgotten.