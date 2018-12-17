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

print "\n     PDF-CRACKER - CRACK PDF FILES THE EASY WAY"
print "\nBY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)\n"

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Conduct routine and simple tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "\nUse the command python pdf-cracker.py filename.pdf\n"
    exit(True)

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "\nFile " + filename + " was not found, did you spell it correctly?"
    exit(True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

installed = False

if os.path.isfile('/usr/share/pdfid/pdfid.py') != 1:
    print "Installing pdfid...\n"
    os.system("apt-get install pdfid")
    installed = True

if os.path.isfile('/usr/bin/pdf-parser') != 1:
    print "Installing pdf-parser...\n"
    os.system("apt-get install pdf-parser")
    installed = True

if os.path.isfile('/usr/bin/pdfcrack') != 1:
    print "Installing pdf-parser...\n"
    os.system("apt-get install pdfcrack")
    installed = True  

if os.path.isfile('/usr/share/wordlists/rockyou.txt') != 1:
    print "Installing rockyou.txt...\n"
    os.system("gunzip /usr/share/wordlists/rockyou.txt.gz > /dev/null 2>&1")
    installed = True

if os.path.isfile('/usr/share/wordlists/rockyou.txt') != 1:
    print "Rockyou.txt.gz missing - are you using Kali?...\n"
    print "You will need place the file Rockyou.txt.gz in the directory /usr/share/wordlists/ ....\n"
    exit (True)

if installed == False:
    print "\nAll required dependencies are pre-installed...\n"
else:
    print "\nMissing dependencies have been installed for you...\n"

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check file extension is .pdf and capture any rogue spaces in filename.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

typetest = filename[-3:]

if typetest != "pdf":
    print "Is this not a .pdf file...\n"
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check that the file is encrypted.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("pdfid " + filename + " > F1.txt")
os.system("tail -n +2 F1.txt > F2.txt")
os.system("awk '/PDF Header/{print $NF}' F2.txt > F3.txt")
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
    print filename + " is not an encrypted .pdf file...\n"
    exit (True)
else:
    print "Filename         : " + filename
    print "Filetype         : " + pdftype
    print "Encryption Status: " + pdfstatus

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Extract the encryption object  
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

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

print "Object           : " + pdfobject

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Extract the standard encryption information from the object  
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

os.system("pdf-parser -o " + pdfobject + " " + filename +  " > F1.txt")
os.system("grep -o 'Filter[^\"]*' F1.txt > F2.txt")

for line in fileinput.input('F2.txt', inplace=1):
    sys.stdout.write(line.replace('Filter /', ''))

with open('F2.txt', 'r') as myfile:
    objectencrypt = myfile.read().replace('\n', '')

os.remove('./F1.txt')
os.remove('./F2.txt')

print "Object Encryption: " + objectencrypt

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Check if password encrypted
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

passrequired = False

os.system("qpdf --show-encryption " + filename + " 2>&1 | tee F1.txt > F2.txt")

for line in fileinput.input('F2.txt', inplace=1):
    sys.stdout.write(line.replace(filename + ": ", ''))

with open('F2.txt', 'r') as myfile:
    pdfpassword = myfile.read().replace('\n', '')

os.remove('./F1.txt')
os.remove('./F2.txt')

if pdfpassword == "invalid password":
    print "Password         : protected"
    passrequired = True

# -------------------------------------------------------------------------------------
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: SME                                                               
# Version: 1.0                                                                
# Details: Start cracking 
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

print "Crack type       : password bruteforce - please wait..."
os.system("pdfcrack " + filename + " -n 6 -w /usr/share/wordlists/rockyou.txt > F1.txt")
os.system("awk '/found user-password/{print $NF}' F1.txt > F2.txt")

with open('F2.txt', 'r') as myfile:
    pdfpassword = myfile.read().replace('\n', '')

pdfpassword = pdfpassword.replace("'", "")
print "Password         : " + pdfpassword

os.remove('./F1.txt')
os.remove('./F2.txt')

if passrequired == True:
    os.system("qpdf --password=" + pdfpassword + " --decrypt " + filename + " cracked.pdf")
    print "Crack file       : cracked.pdf"

exit (True)

#EOF
