## Pre-requisites
- Raspberry Pi GPIO libraries (if not yet installed)
- MySQL

Please contact me if there are any more pre-requisites that I missed here

## Installation
1. Boot up "mysql" in the command line with your credentials (e.g. user == root)
    ```
    mysql --user="root" -p
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 41
    Server version: 5.5.57-0+deb8u1 (Raspbian)

    Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    mysql>
    ```
    
2. Create the 'sjcmpc' database and confirm that it exists
    ```
    mysql> CREATE DATABASE sjcmpc;
    Query OK, 1 row affected (0.00 sec)
    mysql> USE sjcmpc;
    Database changed
    ```
3. Clone this repository to a directory on your Raspberry Pi
    ```
    git clone https://github.com/Francis-T/sjcmpc_app.git
    Cloning into 'sjcmpc_app'...
    remote: Counting objects: 25, done.
    remote: Compressing objects: 100% (20/20), done.
    remote: Total 25 (delta 3), reused 25 (delta 3), pack-reused 0
    Unpacking objects: 100% (25/25), done.
    Checking connectivity... done.
    ```
4. Enter the newly-created directory and run setup.sh
    ```
    cd sjcmpc_app
    ./setup.sh
    ```
5. Test the program by running main.py
    ```
    python3 main.py
    =====================================
    Test Program w/ Database Connectivity
    -------------------------------------
      (1) Admin Mode
      (2) Normal Mode
      (3) Quit
    > 

    ```
  

