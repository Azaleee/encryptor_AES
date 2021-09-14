#! /usr/bin/env python3
# -*- coding: utf-8 -*- 

#Import Modules

from hashlib import sha256
import os, glob, string, random, time, sys, getopt
try:
	import pyAesCrypt
except ImportError:
	print('=========================================================================')
	print(' Necessary component missing')
	print(' Please run: pip3 install pyAesCrypt')
	print('=========================================================================')
	exit()

try:
	from progressbar import progressbar
except ImportError:
	print('=========================================================================')
	print(' Necessary component missing')
	print(' Please run: pip3 install progress progressbar2 alive-progress tqdm')
	print('=========================================================================')
	exit()
try:
	from colorama import init
except ImportError:
	print('=========================================================================')
	print(' Necessary component missing')
	print(' Please run: pip3 install colorama')
	print('=========================================================================')
	exit()
init()

class colors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'

global char
global bufferSize
char = string.ascii_lowercase + string.digits 
bufferSize = 64 * 1024

def welcome():
	print('''
▓█████  ███▄    █  ▄████▄   ██▀███ ▓██   ██▓ ██▓███  ▄▄▄█████▓ ▒█████   ██▀███  
▓█   ▀  ██ ▀█   █ ▒██▀ ▀█  ▓██ ▒ ██▒▒██  ██▒▓██░  ██▒▓  ██▒ ▓▒▒██▒  ██▒▓██ ▒ ██▒
▒███   ▓██  ▀█ ██▒▒▓█    ▄ ▓██ ░▄█ ▒ ▒██ ██░▓██░ ██▓▒▒ ▓██░ ▒░▒██░  ██▒▓██ ░▄█ ▒
▒▓█  ▄ ▓██▒  ▐▌██▒▒▓▓▄ ▄██▒▒██▀▀█▄   ░ ▐██▓░▒██▄█▓▒ ▒░ ▓██▓ ░ ▒██   ██░▒██▀▀█▄  
░▒████▒▒██░   ▓██░▒ ▓███▀ ░░██▓ ▒██▒ ░ ██▒▓░▒██▒ ░  ░  ▒██▒ ░ ░ ████▓▒░░██▓ ▒██▒
░░ ▒░ ░░ ▒░   ▒ ▒ ░ ░▒ ▒  ░░ ▒▓ ░▒▓░  ██▒▒▒ ▒▓▒░ ░  ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
 ░ ░  ░░ ░░   ░ ▒░  ░  ▒     ░▒ ░ ▒░▓██ ░▒░ ░▒ ░         ░      ░ ▒ ▒░   ░▒ ░ ▒░
   ░      ░   ░ ░ ░          ░░   ░ ▒ ▒ ░░  ░░         ░      ░ ░ ░ ▒    ░░   ░ 
   ░  ░         ░ ░ ░         ░     ░ ░                           ░ ░     ░     
                  ░                 ░ ░                                         
	
	''')
	print("encryptor v1.0\n")

def all_files_Finder(path_folder): 
	all_files = []
	for r, d, f in os.walk(path_folder):
	    for file in f:
	        if file.endswith(""):
	            all_files.append(os.path.join(r, file))
	return all_files

def genKey(key): 
	return sha256(key.encode('utf-16')).hexdigest()

def path_good(path_folder):
	if not os.path.exists(path_folder):
		print(colors.WARNING + "\nThe directory", "'", path_folder, "'" , "does not exists !" + colors.RESET)
		exit()

def is_valide(value):
	try:
		value = int(value)
	except ValueError:
		print(colors.FAIL + "Incorrect value !" + colors.RESET)
		exit()

def if_folder_empty(all_files):
	if all_files == []:
		print(colors.WARNING + "\nThere are no files to encrypt here !" + colors.RESET)
		exit()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def cryptDir(path_folder, keys):
	itter = 0
	path_good(path_folder) 
	all_files = all_files_Finder(path_folder) 
	if_folder_empty(all_files)
	for i in progressbar(range(len(all_files))):
		itter += 1
		with open(all_files[i], "rb") as fIn:
			with open(all_files[i] + ".crypt", "wb") as fOut:
				pyAesCrypt.encryptStream(fIn, fOut, genKey(keys), bufferSize)
		os.remove(all_files[i])
	print(colors.OK + "\n",path_folder,"is completely encrypted !" + colors.RESET)
	print(colors.OK , itter , "file(s) encrypted")

def decryptDir(path_folder, keys):
	itter = 0
	path_good(path_folder)
	all_files = all_files_Finder(path_folder) 
	if_folder_empty(all_files)
	for i in progressbar(range(len(all_files))):
		itter += 1
		encFileSize = os.stat(all_files[i]).st_size
		with open(all_files[i], "rb") as fIn:
			with open(all_files[i].replace(".crypt", ""), "wb") as fOut:
				try:
					pyAesCrypt.decryptStream(fIn, fOut, genKey(keys), bufferSize, encFileSize)
				except ValueError:
					print(colors.FAIL + "Wrong password (or file is corrupted)" + colors.RESET)	
					exit()	
		os.remove(all_files[i])
	print(colors.OK + "\n",path_folder,"is completely decrypted !" + colors.RESET)
	print(colors.OK , itter , "file(s) decrypted")
	

def main(argv):

	path_folder = ""
	key = ""
	cipher = ""
	try:
		opts, args = getopt.getopt(argv,"hc:p:k:",["cipher=","path_folder=","key="])
	except getopt.GetoptError:
		print('usage : test_b.py -c <encrypt/decrypt> -p <path_dir> -k <key>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('usage : test_b.py -c <encrypt/decrypt> -p <path_dir> -k <key>')
			sys.exit()
		elif opt in ("-c", "--cipher"):
			cipher = arg
		elif opt in ("-p"):
			path_folder = arg
		elif opt in ("-k", "--key"):
			key = arg

	if path_folder == "" or key == "" or cipher == "":
		print('usage : test_b.py -c <encrypt/decrypt> -p <path_dir> -k <key>')
		sys.exit()

	if cipher == "encrypt":
		welcome()
		keys = genKey(key)
		cryptDir(path_folder, keys)
	elif cipher == "decrypt":
		welcome()
		keys = genKey(key)
		decryptDir(path_folder, keys)
	else:
		pass

if __name__ == '__main__':
	main(sys.argv[1:])