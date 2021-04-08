import re
from mkw_ghosts import MkwGhosts
from mii import Mii

track_dict = {8:'LC', 1:'MMM', 2:'MG', 4:'TF', 5:'CM', 6:'DKS', 7:'WGM', 9:'DC', 15:'KC', 11:'MT', 3:'GV', 14:'DDR', 10:'MH', 12:'BC', 13:'RR', 16:'rPB', 20:'rYF', 25:'rGV2', 26:'rMR', 27:'rSL', 31:'rSGB', 23:'rDS', 18:'rWS', 21:'rDH', 30:'rBC3', 29:'rDKJP', 17:'rMC', 24:'rMC3', 22:'rPG', 19:'rDKM', 28:'rBC'}

f = open('rksys.dat', 'rb+')
addr_list = []
f.seek(0x27999)
for m in re.finditer(b'RKGD', f.read()):
	addr_list.append(m.start() + 162201)
	print('Found ghost at: ' + str(hex(m.start() + 162201)))
ghost_list = []
for i in range(len(addr_list)):
	f.seek(addr_list[i] + 14)
	ghost_length = int(14 + int.from_bytes(f.read(2), byteorder='big') + 122)
	f.seek(addr_list[i])
	ghost = f.read(ghost_length)
	ghost_list.append(ghost)

for i, ghost in enumerate(ghost_list):
	if addr_list[i] >= 2191360:
		license = '4'
	elif addr_list[i] >= 1515520:
		license = '3'
	elif addr_list[i] >= 839680:
		license = '2'
	elif addr_list[i] >= 163840:
		license = '1'
	ghost = MkwGhosts.from_bytes(ghost_list[i])
	mii = Mii.from_bytes(ghost.driver_mii_data)
	filename = 'License' + license + '_' + (track_dict.get(ghost.track_id)) + '_' + str(ghost.finishing_time_minutes) + """'""" + str(ghost.finishing_time_seconds).zfill(2) + """'""" + """'""" + str(ghost.finishing_time_milliseconds).zfill(3) + '.rkg'
	g = open(f'{filename}', 'wb')
	g.write(ghost_list[i])

print('Successfully extracted ' + str(len(ghost_list)) +' ghosts from the rksys file.')