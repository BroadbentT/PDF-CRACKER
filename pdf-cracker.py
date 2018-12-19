#!/usr/bin/python

# -------------------------------------------------------------------------------------
#                  PYTHON UTILITY FILE TO CRACK ENCRYPTED .PDF FILES
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Load any required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import fileinput

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Show a universal header.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------
print " ____    ____    _____    ____   ____       _       ____   _  __  _____   ____   "
print "|  _ \  |  _ \  |  ___|  / ___| |  _ \     / \     / ___| | |/ / | ____| |  _ \  "
print "| |_) | | | | | | |_    | |     | |_) |   / _ \   | |     | ' /  |  _|   | |_) | "
print "|  __/  | |_| | |  _|   | |___  |  _ <   / ___ \  | |___  | . \  | |___  |  _ <  "
print "|_|     |____/  |_|      \____| |_| \_\ /_/   \_\  \____| |_|\_\ |_____| |_| \_\ "
print "                                                                                 "
print "             BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)               "

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(True)
if len(sys.argv) < 2:
    print "\nUse the command python pdf-cracker.py topsecret.pdf\n"
    exit(True)
filename = sys.argv[1]
if os.path.exists(filename) == 0:
    print "\nFile " + filename + " was not found, did you spell it correctly?"
    exit(True)
typetest = filename[-3:]
if typetest != "pdf":
    print "This is not a .pdf file...\n"
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print "\nChecking dependencies...."
install = False
if os.path.isfile('/usr/share/pdfid/pdfid.py') != 1:
    print "pdfid - missing"
    install = True
if os.path.isfile('/usr/bin/pdf-parser') != 1:
    print "pdf-parser - missing"
    install = True
if os.path.isfile('/usr/bin/pdfcrack') != 1:
    print "pdfcrack - missing"
    install = True
if os.path.isfile('/usr/share/wordlists/rockyou.txt') != 1:
    print "Rockyou.txt - missing"
    install = True
if os.path.isfile('/root/Downloads/bleeding-jumbo/JohnTheRipper-bleeding-jumbo/run/pdf2john.pl') != 1:
    print "John the ripper bleeding jumbo - missing"
    install = True
if os.path.isfile('/root/.hashcat/hashcat.potfile') != 1:
    print "Hashcat - missing"
    install = True
if install == False:
    print "All required dependencies are pre-installed..."
else:
    print "Install any missing dependencies before you begin..."
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Conduct a set of complex tests on the specified file.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("pdfid " + filename + " > F1.txt")
os.system("tail -n +2 F1.txt > F2.txt")
os.system("awk '/PDF Header/{print $NF}' F2.txt > F3.txt")
for line in fileinput.input('F3.txt', inplace=1):
    sys.stdout.write(line.replace('%', ''))        
os.system("awk '/Encrypt/{print $NF}' F2.txt > F4.txt")
with open('F3.txt', 'r') as myfile:
    pdftype = myfile.read().replace('\n', '')
with open('F4.txt', 'r') as myfile:
    pdfstatus = myfile.read().replace('\n', '')
os.remove('./F1.txt')
os.remove('./F2.txt')
os.remove('./F3.txt')
os.remove('./F4.txt')
if pdfstatus == "0":
    print "\n" + filename + " is not an encrypted .pdf file...\n"
    exit (True)
else:
    print "\nFilename          : " + filename
    print "Version           : " + pdftype
    print "Encryption Status : Encrypted"
    print "Encryption Level  : " + pdfstatus
    os.system("pdf-parser -s /Encrypt " + filename +  " > F1.txt")
    os.system("grep -o 'Encrypt[^\"]*' F1.txt > F2.txt")
    os.system("tail -n +2 F2.txt > F3.txt")
    for line in fileinput.input('F3.txt', inplace=1):
        sys.stdout.write(line.replace('Encrypt ', ''))
    os.system("cat F3.txt | grep -o -E '[0-9]+' > F4.txt")
    os.system("sed '2d' F4.txt > F5.txt")
    with open('F5.txt', 'r') as myfile:
        pdfobject = myfile.read().replace('\n', '')
    os.remove('./F1.txt')
    os.remove('./F2.txt')
    os.remove('./F3.txt')
    os.remove('./F4.txt')
    os.remove('./F5.txt')
    print "Encryption Object : " + pdfobject
    os.system("pdf-parser -o " + pdfobject + " " + filename +  " > F1.txt")
    os.system("grep -o 'Filter[^\"]*' F1.txt > F2.txt")
    for line in fileinput.input('F2.txt', inplace=1):
        sys.stdout.write(line.replace('Filter /', ''))
    with open('F2.txt', 'r') as myfile:
        objectencrypt = myfile.read().replace('\n', '')
    os.remove('./F1.txt')
    os.remove('./F2.txt')
    print "Object Filter     : " + objectencrypt
    os.system("qpdf --show-encryption " + filename + " 2>&1 | tee F1.txt > F2.txt")
    for line in fileinput.input('F2.txt', inplace=1):
        sys.stdout.write(line.replace(filename + ": ", ''))
    with open('F2.txt', 'r') as myfile:
        pdfpassword = myfile.read().replace('\n', '')
    os.remove('./F1.txt')
    os.remove('./F2.txt')
    if pdfpassword == "invalid password":
        print "Password Protected: Yes\n"
    else:
        print "Password Protected: Owner\n"

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['1']="Dictionary Attack."
menu['2']="Hash Attack."
menu['3']="Exit"

while True: 
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]
    selection=raw_input("Please Select: ") 

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option one selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    if selection =='1':
        print "\nCrack Selected    : Dictionary Attack"
        print "Using Dictionary  : /usr/share/wordlists/rockyou.txt"
        print "Crack Status      : Cracking, please wait..."
        os.system("pdfcrack " + filename + " -n 6 -w /usr/share/wordlists/rockyou.txt > F1.txt")
        os.system("awk 'END {print $(NF-3), $(NF-2), $(NF-1),$NF}' F1.txt > F2.txt")
        with open('F2.txt', 'r') as myfile:
            testfound = myfile.read().replace('\n', '')
        if testfound == "Could not find password":
            print "Crack Status      : Dictionary exhausted...\n"
        else:      
            os.system("awk '/found user-password/{print $NF}' F1.txt > F2.txt")
            with open('F2.txt', 'r') as myfile:
                pdfpassword = myfile.read().replace('\n', '')
            pdfpassword = pdfpassword.replace("'", "")
            print "File Password     : " + pdfpassword
            os.system("qpdf --password=" + pdfpassword + " --decrypt " + filename + " Cracked.pdf")
            print "Cracked filename  : Cracked.pdf\n"
        os.remove('./F1.txt')
        os.remove('./F2.txt')
        exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option two selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '2':
        print "\nCrack Selected    : Hash Attack"
        os.system("perl ../../Downloads/bleeding-jumbo/JohnTheRipper-bleeding-jumbo/run/pdf2john.pl " + filename + " > F1.txt")
        for line in fileinput.input('F1.txt', inplace=1):
            sys.stdout.write(line.replace(filename + ":", ''))
        with open('F1.txt', 'r') as myfile:
            hashdata = myfile.read().replace('\n', '')
        hashdata = hashdata[:25] + "..."     
        print "Hash Extracted    : " + hashdata
	if pdfstatus == "2":
            level = "10500"
        elif pdfstatus == "3":
            level = "10600"
	elif pdfstatus == "8":
            level = "10700"
        else:
            print "Encryption level  : Unknown"
            exit (True)
        print "Hash Mode/Level   : " + level
        print "Crack Status      : Cracking, please wait..."
        os.system("hashcat -m " + level + " -a 3 F1.txt -i ?d?d?d?d?d?d --force > F2.txt") # Note - Currently set for six decimal password only
        os.system("hashcat --show -m 10500 F1.txt --force > F3.txt")
        os.system("awk -F: '{ print $2 }' F3.txt > F4.txt")
        with open('F4.txt', 'r') as myfile:
            hashpass = myfile.read().replace('\n', '')
        if hashpass == "":
            print "Crack Status      : Algorithm exhausted...\n"
        else:
            print "Password          : " + hashpass
            os.system("qpdf --password=" + hashpass + " --decrypt " + filename + " Cracked.pdf")
            print "Cracked filename  : Cracked.pdf\n"
        os.remove('./F1.txt')
        os.remove('./F2.txt')
        os.remove('./F3.txt')
        os.remove('./F4.txt')
        exit (True)
 
# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Menu option three selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '3': 
        break

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

    else:
        print ""

#Eof
