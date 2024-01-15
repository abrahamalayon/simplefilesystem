
# SimpleFileSystem with LDAP

A Python script that manipulates the Linux file system and an LDAP Server. (A work in progress...)

## Description

SimpleFileSystem creates, modifies, and deletes files and directories on your Linux file system. You can also navigate through the file system and read files, rename, and copy files. In addition the script allows you to authenticate to, query and download files from an LDAP server using commands such as ldapsearch, ldapdownload, etc. It writes a log in the /var/log directory.  In the current version, traffic to and from LDAP is unencrypted. This script will make changes to your system (i.e delete files, create files) so be careful.

The purpose behind the program is to use a script to execute file system commands on the operating system (as if the user does not know Linux) as well as downloading from servers. The traffic is unencrypted to allow observation of packets with Wireshark. The next phase is to add support for LDAPS, add the find function in Linux, and modify the script so only the log function has to run as superuser. Creating a GUI interface is also in the works.

## Installation

Note:  The file name is simplefilesystemv2.py, which is different from the repository name.

To install and run this program, you need to have Python 3 installed on your system. You can download Python 3 from [here]. You also need to clone this repository to your local machine using the following command:

```bash
git clone https://github.com/abrahamalayon/simplefilesystem.git
```

Then, you need to run the program with sudo privileges, as it needs to access the system files and directories. You can do that by executing the simplefilesystemv2.py file:

```bash
sudo python3 simplefilesystemv2.py
```

## Usage

You will see the following menu options. enter a number.

Menu options:
1. Open a File
2. View Files
3. Write to a File
4. Delete a File
5. Rename a File
6. Copy a File
7. Download a File from LDAP
8. Query LDAP Directory
9. Make a new Directory
10. View Logs
11. Change Directory
12. QUIT

Enter a menu option:  

The program executes the following commands based on your input. 

mkdir <dir>: Creates a new directory with the given name.

rmdir <dir>: Removes an existing directory with the given name.

cd <dir>: Changes the current working directory to the given directory.

ls: Lists the files and directories in the current working directory.

pwd: Prints the path of the current working directory.

touch <file>: Creates a new file with the given name.

rm <file>: Removes an existing file with the given name.

cat <file>: Prints the contents of a file to the standard output.

echo <text>: Prints the given text to the standard output.

cp <src> <dest>: Copies a file from the source to the destination.

mv <src> <dest>: Moves a file from the source to the destination.

find <name>: Searches for a file or directory with the given name in the file system.

less <filename>:  This is used to read files in a convenient format.

12 exits the program

The input is not sanitized in this version. Therefore you can also use the following operators to modify the behavior of the commands, in addition to flags and arguments for the commands:


>: Redirects the standard output of a command to a file. For example, echo hello > file.txt will write the word “hello” to the file.txt file.
>
<: Redirects the standard input of a command from a file. For example, cat < file.txt will print the contents of the file.txt file to the standard output.

|: Pipes the standard output of one command to the standard input of another command. For example, cat file.txt | wc -l will print the number of lines in the file.txt file.

&: Runs a command in the background, allowing you to enter another command without waiting for the first one to finish. For example, sleep 10 & will make the program wait for 10 seconds in the background, while you can enter another command in the foreground.



Examples of LDAP syntax are below.  For example, the search base may be "dc=example,dc=com" when prompted for search base.  The LDAP search and download function works, but you should review the documentation at the following site:  

https://ldap3.readthedocs.io/en/latest/  

Here is an excerpt of relevant information so you can understand the search base and search filter:


- `ldapsearch <base> <filter>`: Searches for entries in the LDAP server that match the given base and filter. The base is the starting point of the search, and the filter is the criteria for selecting entries. For example, `ldapsearch "dc=example,dc=com" "(objectClass=person)"` will search for all entries that are persons in the example.com domain.
- `ldapdownload <base> <filter> <file>`: Downloads a file from the LDAP server that matches the given base and filter, and saves it to the file system with the given name. The base and filter are the same as in the ldapsearch command. For example, `ldapdownload "dc=example,dc=com" "(cn=alice)" alice.txt` will download the file associated with the entry that has the common name alice in the example.com domain, and save it as alice.txt in the file system.

You can test the LDAP functionality with the following site:

https://www.forumsys.com/2022/05/10/online-ldap-test-server/

address: ldap.forumsys.com

port: 389

username: euclid

password: password

You can also download a VM from the following site to test the program:

https://www.turnkeylinux.org/openldap

## License
GNU GENERAL PUBLIC LICENSE

## Contributing

This project is open for contributions. If you want to contribute, please follow these steps:

- Fork this repository and clone it to your local machine.
- Create a new branch with a descriptive name
- Make your changes and commit them with a clear message
- Push your branch to your forked repository
- Create a pull request to the original repository
- Wait for feedback and approval

## Credits

This project was created by Abraham Alayon. The file_system6.py, filesystem2.py and filesystem3.py program was written by Abraham Alayon.
