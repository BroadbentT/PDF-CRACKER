#!/usr/bin/python
# coding:UTF-8

# -------------------------------------------------------------------------------------
#                  PYTHON SCRIPT FILE TO CRACK ENCRYPTED .PDF FILES
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import fileinput

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
    print "\nPlease run this python script as root..."
    exit(True)

if len(sys.argv) < 2:
    print "\nUse the command python pdf-cracker.py pdffile.pdf\n"
    exit(True)

filename = sys.argv[1]

if os.path.exists(filename) == 0:
    print "\nFile " + filename + " was not found, did you spell it correctly?"
    exit(True)

pdftest = filename[-3:]

if pdftest != "pdf":
    print "This is not a .pdf file...\n"
    exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Create function call for my header display.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def header():
   os.system("clear")
   print " ____  ____  _____    ____ ____      _    ____ _  _______ ____   "
   print "|  _ \|  _ \|  ___|  / ___|  _ \    / \  / ___| |/ / ____|  _ \  "
   print "| |_) | | | | |_    | |   | |_) |  / _ \| |   | ' /|  _| | |_) | "
   print "|  __/| |_| |  _|   | |___|  _ <  / ___ \ |___| . \| |___|  _ <  "
   print "|_|   |____/|_|      \____|_| \_\/_/   \_\____|_|\_\_____|_| \_\ "
   print "                                                                 "
   print "     BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)     \n"

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

checklist = ["pdfid", "pdf-parser", "pdfcrack", "rockyou", "pdf2john", "hashcat", "qpdf"]
installed = True

header()
for check in checklist:
    cmd = "locate -i " + check + " > /dev/null"
    checked = os.system(cmd)
    if checked != 0:
        print "I cannot find " + check + "..."
        installed = False

if installed == False:
   print "\nInstall missing dependencies before you begin...\n"
   exit (True)

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Conduct a set of complex tests on the specified file.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def crack(filename):
   os.system("pdfid '" + filename + "' > F1.txt")
   os.system("awk '/PDF Header/{print $NF}' F1.txt > F2.txt")
   os.system("awk '/Encrypt/{print $NF}' F1.txt > F3.txt")
   pdftype = open("F2.txt").readline().rstrip()
   pdfstat = open("F3.txt").readline().rstrip()
   os.remove('F1.txt')
   os.remove('F2.txt')
   os.remove('F3.txt')
   if pdfstat == "0":
      print "File " + filename + " is not an encrypted .pdf file...\n"
      exit (True)
   else:
      print "Filename          : " + filename
      print "Version           : " + pdftype
      print "Encryption Status : Encrypted"
      print "Encryption Level  : " + pdfstat
   os.system("pdf-parser -s /Encrypt '" + filename + "' > F1.txt")
   os.system("awk '/Encrypt/{print $(NF-2)}' F1.txt > F2.txt")
   pdfobject = open("F2.txt").readline().rstrip()
   os.remove('./F1.txt')
   os.remove('./F2.txt')
   print "Encryption Object : " + pdfobject
   os.system("pdf-parser -o " + pdfobject + " '" + filename +  "' > F1.txt")
   os.system("awk '/Filter/{print $NF}' F1.txt > F2.txt")
   objectcrypt = open("F2.txt").readline().rstrip()
   os.remove('F1.txt')
   os.remove('F2.txt')
   print "Object Filter     : " + objectcrypt
   os.system("qpdf --show-encryption '" + filename + "' 2>&1 | tee F1.txt > F1.txt")
   os.system("awk '/" + filename + ":/{print $(NF-1)}' F1.txt > F2.txt")
   pdfpassword = open("F2.txt").readline().rstrip()
   os.remove('F1.txt')
   os.remove('F2.txt')
   if pdfpassword == "invalid":
      print "Password Protected: Yes\n"
   else:
      print "Password Protected: Owner\n"
   return pdfstat

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['1']="Dictionary Attack."
menu['2']="Hash Attack."
menu['3']="Exit"

while True: 
    header()
    pdfstat = crack(filename)
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]
    selection=raw_input("\nPlease Select: ") 
    print ""

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version: 2.0                                                                
# Details: Menu option selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    if selection =='1':
        print "Crack Selected    : Dictionary attack..."
        dictionary = "/usr/share/wordlists/rockyou.txt"
        if os.path.isfile(dictionary):
            print "Using Dictionary  : " + dictionary + "..."
        else:
            print "System Error      : Dictionary not found..."
            exit(True)
        os.system("pdfcrack '" + filename + "' -n 6 -w " + dictionary + " > F1.txt")
        os.system("awk '/found user-password: /{print $NF}' F1.txt > F2.txt")
        pdfpassword = open("F2.txt").readline().rstrip()
        if pdfpassword == "":
            print "Crack Status      : Dictionary exhausted...\n"
        else:      
            print "File Password     : " + pdfpassword
            os.system("qpdf --password=" + pdfpassword + " --decrypt '" + filename + "' Cracked.pdf")
            print "Cracked filename  : Cracked.pdf\n"
        os.remove('F1.txt')
        os.remove('F2.txt')
        exit (False)

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '2':
        print "Crack Selected    : Hash attack..."
        os.system("pdf2john.pl '" + filename + "' > F1.txt")
        for line in fileinput.input('F1.txt', inplace=1):
            sys.stdout.write(line.replace(filename + ":", ''))
        hashdata = open("F1.txt").readline().rstrip()
        hashdata = hashdata[:25] + "..."     
        print "Hash Extracted    : " + hashdata + "..."
	if pdfstat == "2":
            level = "10500"
        elif pdfstat == "3":
            level = "10600"
	elif pdfstat == "8":
            level = "10700"
        else:
            print "Encryption level  : Unknown..."
            os.remove('./F1.txt')
            exit (True)
        print "Hash Mode/Level   : " + level
        os.system("hashcat -m " + level + " -a 3 F1.txt -i ?d?d?d?d?d?d --force > F2.txt 2>&1")
        os.system("hashcat --show -m " + level + " F1.txt --force > F2.txt")
        os.system("awk -F: '{ print $2 }' F2.txt > F3.txt")
        hashpass = open("F3.txt").readline().rstrip()
        if hashpass == "":
            print "Crack Status      : Algorithm exhausted...\n"
        else:
            print "Password          : '" + hashpass + "'"
            os.system("qpdf --password=" + hashpass + " --decrypt '" + filename + "' Cracked.pdf")
            print "Cracked filename  : Cracked.pdf\n"
        os.remove('F1.txt')
        os.remove('F2.txt')
        os.remove('F3.txt')
        exit (True)
 
# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Menu option selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

    elif selection == '3': 
        break

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 2.0                                                                
# Details : Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

    else:
        print ""

#Eof
