import re
from mkw_ghosts import MkwGhosts
import shutil
from os import path, mkdir
from mii import Mii


track_dict = {8:'LC', 1:'MMM', 2:'MG', 4:'TF', 0:'MC', 5:'CM', 6:'DKS', 7:'WGM', 9:'DC', 15:'KC', 11:'MT', 3:'GV', 14:'DDR', 10:'MH', 12:'BC', 13:'RR', 16:'rPB', 20:'rYF', 25:'rGV2', 26:'rMR', 27:'rSL', 31:'rSGB', 23:'rDS', 18:'rWS', 21:'rDH', 30:'rBC3', 29:'rDKJP', 17:'rMC', 24:'rMC3', 22:'rPG', 19:'rDKM', 28:'rBC'}

def remove_illegal_chars(string):
	#removes characters from the filename that can't be used in files
	illegal_chars = '\/:?"<>|'
	for char in illegal_chars:
		string = string.replace(char, "")

	return string

with open('rksys.dat', 'rb+') as f:
	filename_list = []
	addr_list = []
	f.seek(162201) #162201 = 0x27999, this is start of the ghosts in the rksys
	for m in re.finditer(b'RKGD', f.read()): #go through rksys to find all instances of RKGD header (indicates start of a ghost)
		addr_list.append(m.start() + 162201) #162201 = 0x27999, adds the address of the ghost which is relative found location to 0x27999 + 27999
	ghost_list = []
	for i in range(len(addr_list)):
		f.seek(addr_list[i] + 14) #seeking to part in file where ghost input length is stored
		ghost_length = 0x2800 #122 is length up until ghost inputs
		f.seek(addr_list[i]) #go to file start to read the contents of the file
		ghost = f.read(ghost_length)
		ghost_list.append(ghost)
	f.close()
	print(f'Found {str(len(ghost_list))} ghosts') 
	for i, ghost in enumerate(ghost_list):
		if addr_list[i] >= 2191360: #these just check where the ghost is in the file to see what license it is
			license = '4'
		elif addr_list[i] >= 1515520:
			license = '3'
		elif addr_list[i] >= 839680:
			license = '2'
		elif addr_list[i] >= 163840:
			license = '1'
		else:
			license = 'unknown'
		ghost = MkwGhosts.from_bytes(ghost_list[i])
		mii = Mii.from_bytes(ghost.driver_mii_data)
		filename = 'License' + str(license) + '_' + (track_dict.get(ghost.track_id)) + '_' + str(ghost.finishing_time_minutes) + """'""" + str(ghost.finishing_time_seconds).zfill(2) + """'""" + """'""" + str(ghost.finishing_time_milliseconds).zfill(3) + '_' + str(remove_illegal_chars(mii.mii_name)) + '.rkg'
		with open(f'{filename}', 'wb') as g:
			filename_list.append(filename)
			print('Exported ghost at address: ' + hex(addr_list[i]))
			g.write(ghost_list[i])
			g.close()

print('Successfully extracted ' + str(len(ghost_list)) +' ghosts from the rksys file.')