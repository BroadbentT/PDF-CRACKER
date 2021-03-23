#!/usr/bin/python3
# coding:UTF-8

# -------------------------------------------------------------------------------------
#                  PYTHON SCRIPT FILE TO CRACK ENCRYPTED .PDF FILES
#                BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)
# -------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Load required imports.
# Modified: N/A
# -------------------------------------------------------------------------------------

import os
import sys
import pyfiglet
import fileinput

from termcolor import colored

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Conduct simple and routine tests on supplied arguements.   
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

if os.geteuid() != 0:
   print("\nPlease run this python script as root...")
   exit()

if len(sys.argv) < 2:
   print("\nUse the command python3 pdf-cracker.py topsecret.pdf\n")
   exit()

fileName = sys.argv[1]

if not os.path.exists(fileName):
   print("\nFile " + fileName + " was not found, did you spell it correctly?")
   exit()

if fileName[-3:] != "pdf":
   print("This is not a .pdf file...\n")
   exit()

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Create function call for my header display.    
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def header():
   os.system("clear")
   ascii_banner = pyfiglet.figlet_format("PDF CRACKER").upper()
   print(colored(ascii_banner.rstrip("\n"), 'red', attrs=['bold']))
   print(colored("     BY TERENCE BROADBENT BSC CYBER SECURITY (FIRST CLASS)     \n", 'yellow', attrs=['bold']))
   return

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Check all required dependencies are installed on the system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

installed = True
dirLocate = "/usr/bin/"
checkList = ["pdfid", "pdf-parser", "pdfcrack", "hashcat", "qpdf"]

header()
for check in checkList:
   cmd = "locate -i " + dirLocate + check + " > /dev/null"
   checked = os.system(cmd)
   if checked != 0:
      print("[-] I cannot find " + check + "...")
      installed = False

if installed == False:
   print("[!] Install the above missing dependencies before you begin...\n")
   exit ()

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Conduct a set of complex tests on the specified file.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

def crack(fileName):
   os.system("pdfid '" + fileName + "' > F1.tmp")
   os.system("awk '/PDF Header/{print $NF}' F1.tmp > F2.tmp")
   os.system("awk '/Encrypt/{print $NF}' F1.tmp > F3.tmp")
   pdftype = open("F2.tmp").readline().rstrip().replace("%","")
   pdfstat = open("F3.tmp").readline().rstrip()
   
   if pdfstat == "0":
      print("File " + fileName + " is not an encrypted .pdf file...\n")
      exit ()

   print("Filename          : " + fileName)
   print("Version           : " + pdftype)
   print("Encryption Status : Encrypted")
   print("Encryption Level  : " + pdfstat)
      
   os.system("pdf-parser -s /Encrypt '" + fileName + "' > F4.tmp")
   os.system("awk '/Encrypt/{print $(NF-2)}' F4.tmp > F5.tmp")
   pdfobject = open("F5.tmp").readline().rstrip()
   print("Encryption Object : " + pdfobject)

   os.system("pdf-parser -o " + pdfobject + " '" + fileName +  "' > F6.tmp")
   os.system("awk '/Filter/{print $NF}' F6.tmp > F7.tmp")
   objectcrypt = open("F7.tmp").readline().rstrip().replace("/","")
   print("Object Filter     : " + objectcrypt)

   os.system("qpdf --show-encryption '" + fileName + "' 2>&1 | tee F7.tmp > F8.tmp")
   os.system("awk '/" + fileName + ":/{print $(NF-1)}' F8.tmp > F9.tmp")
   pdfpassword = open("F9.tmp").readline().rstrip()
   
   if pdfpassword == "invalid":
      print("Password Protected: Yes\n")
   else:
      print("Password Protected: Owner\n")
   os.system("rm *.tmp")
   return pdfstat

# -------------------------------------------------------------------------------------
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Main menu system.
# Modified: N/A                                                               
# -------------------------------------------------------------------------------------

menu = {}
menu['1']="Dictionary Attack."
menu['2']="Hash Attack."
menu['3']="Exit"

while True: 
   header()
   pdfstat = crack(fileName)
   options=list(menu.keys())
   options.sort()
   for entry in options: 
      print(entry, menu[entry])
   print(colored("\n[?] Please select an option: ",'green'),end='')
   selection=input()

# ------------------------------------------------------------------------------------- 
# AUTHOR: Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version: 2.0                                                                
# Details: Menu option selected - Dictionary attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection =='1':
      dictionary = "/usr/share/wordlists/rockyou.txt"						# USER CHANGEABLE LOCATION OF DICTIONARY
      if os.path.exists(dictionary):
         print("\nUsing Dictionary  : " + dictionary)
      else:
         print("\nSystem Error      : The identified dictionary on line 166 of this script, was not found!!...")
         exit()         
         
      os.system("pdfcrack '" + fileName + "' -n 6 -w " + dictionary + " > F1.tmp")
      os.system("awk '/found user-password: /{print $NF}' F1.tmp > F2.tmp")
      pdfpassword = open("F2.tmp").readline().rstrip()
      
      if pdfpassword != "":
         print("PDF File Password : " + pdfpassword)
         os.system("qpdf --password=" + pdfpassword + " --decrypt '" + fileName + "' Cracked.pdf")
         print("Cracked Filename  : Cracked.pdf\n")
      else:
         print("Crack Status      : Dictionary exhausted...\n")     
            
      os.system("rm *.tmp")
      exit ()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Menu option selected - Hash attack.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '2':     
      hashcracker = "/usr/share/john/pdf2john.pl"									# USER CHANGEABLE LOCATION OF PDF2JOHN
      if not os.path.exists(hashcracker):
         print("\nSystem Error      : The identified file on line 196 of this script, was not found!!...")
         exit()
         
      os.system(hashcracker + " '" + fileName + "' > F1.tmp")
      os.system("sed -i 's/" + fileName + "://g' F1.tmp")
      hashdata = open("F1.tmp").readline().rstrip()
      print("\nHash Extracted    : " + hashdata[:55] + "...")
      
      if pdfstat == "2":
         level = "10500"
      elif pdfstat == "3":
         level = "10600"
      elif pdfstat == "8":
         level = "10700"
      else:
         print("Encryption level  : Unknown...")
         os.system("rm *.tmp")
         exit ()                  
      print("Hash Mode/Level   : " + level)
      
      os.system("hashcat -m " + level + " -a 3 F1.tmp -i ?d?d?d?d?d?d --force > F2.tmp")
      os.system("hashcat --show -m " + level + " F1.tmp --force > F2.tmp")
      os.system("awk -F: '{ print $2 }' F2.tmp > F3.tmp")
      hashpass = open("F3.tmp").readline().rstrip()
      
      if hashpass != "":
         print("PDF File Password : '" + hashpass + "'")
         os.system("qpdf --password=" + hashpass + " --decrypt '" + fileName + "' Cracked.pdf")
         print("Cracked Filename  : Cracked.pdf\n")
      else:
         print("Crack Status      : Algorithm exhausted...\n")    
          
      os.system("rm *.tmp")
      exit ()
 
# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Menu option selected - Quit program.
# Modified: N/A
# -------------------------------------------------------------------------------------

   if selection == '3': 
      quit()

# ------------------------------------------------------------------------------------- 
# AUTHOR  : Terence Broadbent                                                    
# CONTRACT: GitHub                                                               
# Version : 3.0                                                                
# Details : Catch all other entries.
# Modified: N/A
# -------------------------------------------------------------------------------------

   else:
      pass

#Eof
