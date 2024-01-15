import re
import subprocess
import os
import datetime
import logging
from subprocess import check_output
import ldap3
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
import getpass
import ssl
import getpass
import logging
import logging
import datetime

#i declared these global variables for use in logging and menu system

NOW = datetime.datetime.now()
QUIT = 12

# ...

def optionmenu():
    print(' ')
    print("Menu options:")
    print("1. Open a File")
    print("2. View Files")
    print("3. Write to a File")
    print("4. Delete a File")
    print("5. Rename a File")
    print("6. Copy a File")
    print("7. Download a File from LDAP") 
    print("8. Query LDAP Directory")
    print("9. Make a new Directory")
    print("10. View logs")
    print("11. Change Directory") 
    print("12. QUIT")
    
    while True:
        option = input("Enter a menu option: ")
        if re.match(r'^[1-9]|1[0-2]$', option):
            return int(option)
        else:
            print("Please enter a valid option!")

# ...

def main():
    menu_choice = 'y'
    
    while menu_choice != QUIT:
        menu_choice = optionmenu()
        
        if menu_choice == 1:
            openfile()
        elif menu_choice == 2:
            viewfile()
        elif menu_choice == 3:
            writefile()
        elif menu_choice == 4:
            deletefile()
        elif menu_choice == 5:
            renamefile()
        elif menu_choice == 6:
            copyfile()
        elif menu_choice == 7:
            downloadfile()
        elif menu_choice == 8:
            ldapquery()
        elif menu_choice == 9:
            makedirectory()
        elif menu_choice == 10:
            viewlogs()
        elif menu_choice == 11:
            changedir()
        else:
            menu_choice = QUIT
                
    print("Thank you for using SimpleFileSystem!")
        
def openfile():
   filename = str(input("Enter a filename: "))
   
   #logfile = "samplelog.txt"
   subprocess.call(['less', filename], shell=False)
   #create a log entry


def viewfile():
    print()
    print("Files in current directory:  ")
    print()
    subprocess.call(['ls'], shell=False) 
    #using the call() function
    print()  
    
    # Log the action
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "viewed the files in the current directory"
    blank2 = " "
    logwrite(username, action, "current directory", blank2)

def writefile():
    filename = input("Enter a Filename: ")
    openfile3 = open(filename, "a")
    writestuff = input("Enter text to write to file: ")
    openfile3.write(writestuff)
    openfile3.close()
    print("Text written to ", filename)
    
    # Log the action
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "wrote to a file"
    blank1 = " "
    logwrite(username, action, filename, blank1)

def deletefile():
    print()
    filename = input("Enter a filename to delete: ")
    subprocess.call(['rm', filename], shell=False)
    print("File ", filename, "deleted.")
    print()
    
    # Log the action
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "deleted a file"
    blank1 = " "
    logwrite(username, action, filename, blank1)

def renamefile():
    print()
    filename1 = input("Enter the name of the file you want to rename: ")
    print()
    filename2 = input("Enter the new filename: ")
    subprocess.call(['mv', filename1, filename2], shell=False)
    print()
    print("File ", filename1, " has been renamed to ", filename2)
    
    # Log the action
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "renamed a file"
    blank1 = " "
    logwrite(username, action, f"{filename1} to {filename2}", blank1)

def copyfile():
    print()
    filename = input("Enter the filename you wish to copy: ")
    destination = input("Enter the destination file or directory for the copy: ")
    subprocess.call(['cp', filename, destination], shell=False)
    print()
    print("File: ", filename, "has been copied", destination)
    print()
    
    # Log the action
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "copied a file"
    blank1 = " "
    logwrite(username, action, f"{filename} to {destination}", blank1)

def changedir():
    directoryvar = input("Enter the path or name of a directory you want to change to: ")
    os.chdir(directoryvar)
    cwd = os.getcwd()
    print("Directory is now ", cwd)
    
    # Log the action
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "changed current directory"
    blank1 = " "
    logwrite(username, action, directoryvar, blank1)

def makedirectory():
    newdir = input("Enter the path or directory name you wish to create: ")
    subprocess.call(['mkdir', newdir], shell=False)
    print("Directory ", newdir, " created.")
    
    # Log the action
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "created a directory"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blank1 = " "
    logwrite(username, action, f"{current_time} - {newdir}", blank1)

def viewlogs():
    # Log the action
    
    username = subprocess.check_output(['whoami']).decode('utf-8').strip()
    action = "viewed the logs "
    time = NOW 
    blank2 = " "
    logwrite(username, action, time, blank2)

    # Call the command to view the logs
    subprocess.call(['less', '/var/log/sfssamplelog.log'], shell=False)
 

def ldapquery():

    # Get user input for LDAP server details
    server_address = input("Enter the LDAP server address: ")
    server_port = int(input("Enter the LDAP server port: "))
    username = input("Enter the LDAP username: ")
    password = getpass.getpass("Enter the LDAP password: ")
    search_base = input("Enter the search base: ")
    search_filter = input("Enter the search filter: ")

    # Create an LDAP connection
    if server_port == 636:
        # Use SSL/TLS encrypted connection
        tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED)
        server = ldap3.Server(server_address, port=server_port, use_ssl=True, tls=tls_configuration)
    else:
        # Use unencrypted connection
        server = ldap3.Server(server_address, port=server_port)

    # Bind to the LDAP server
    try:
        conn = ldap3.Connection(server_address, user=username, password=password, auto_bind=True)
        print("Successfully connected to the LDAP server.")
        
        # Perform LDAP query
        conn.search(search_base, search_filter, attributes=ldap3.ALL_ATTRIBUTES)
        
        # Print the results
        for entry in conn.entries:
            print(entry)
        
        # Unbind from the LDAP server
        conn.unbind()
        print("Disconnected from the LDAP server.")
    except ldap3.core.exceptions.LDAPException as e:
        print("Failed to connect to the LDAP server:", str(e))


def downloadfile():
    # Get user input for LDAP server details
    server = input("Enter the LDAP server address: ")
    port = int(input("Enter the LDAP server port: "))
    username = input("Enter the LDAP username: ")
    password = getpass.getpass("Enter the LDAP password: ")
    file_dn = input("Enter the DN (Distinguished Name) of the file to download: ")
    file_path = input("Enter the local path to save the downloaded file: ")

    # Create an LDAP connection
    if port == 636:
        # Use SSL/TLS encrypted connection
        tls_configuration = ldap3.Tls(validate=ssl.CERT_REQUIRED)
        server = ldap3.Server(server, port=port, use_ssl=True, tls=tls_configuration)
    else:
        # Use unencrypted connection
        server = ldap3.Server(server, port=port)

        # Bind to the LDAP server
        try:
            conn = ldap3.Connection(server, user=username, password=password, auto_bind=True)
            print("Successfully connected to the LDAP server.")

            # Download the file
            conn.search(file_dn, '(objectClass=*)', attributes=['file;binary'])
            entry = conn.entries[0]
            file_data = entry.file.values[0]
            with open(file_path, 'wb') as file:
                file.write(file_data)

            print("File downloaded successfully.")
        except Exception as e:
            print("Error occurred while downloading the file:", str(e))
         
         

            #function to write logs
            
def logwrite(var1, phrase, var2, var3):
    try:
        logging.basicConfig(filename='/var/log/sfssamplelog.log', level=logging.INFO)
        logging.info(f"{var1} {phrase} {var2} by {var3}")
    except Exception as e:
        print("Error occurred while writing logs:", str(e))



    # 11) Exit the program menu
    # a. (* do not use ‘break’)
    # the loop breaks when you enter 11. see main() above

if __name__=='__main__':
    main()
