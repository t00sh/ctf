import socket
import datetime
import random

IP = '54.144.207.217'
PORT = 7463

basedeck = [
	"Birds of Paradise1",
	"Birds of Paradise2",
	"Birds of Paradise3",
	"Birds of Paradise4",
	"Eternal Witness1",
	"Kitchen Finks1",
	"Kitchen Finks2",
	"Kitchen Finks3",
	"Linvala, Keeper of Silence1",
	"Murderous Redcap1",
	"Noble Hierarch1",
	"Noble Hierarch2",
	"Orzhov Pontiff1",
	"Reclamation Sage1",
	"Restoration Angel1",
	"Restoration Angel2",
	"Reveillark1",
	"Scavenging Ooze1",
	"Shriekmaw1",
	"Siege Rhino1",
	"Siege Rhino2",
	"Sin Collector1",
	"Spellskite1",
	"Voice of Resurgence1",
	"Voice of Resurgence2",
	"Voice of Resurgence1",
	"Wall of Roots1",
	"Wall of Roots2",
	"Abrupt Decay1",
	"Abrupt Decay2",
	"Abrupt Decay1",
	"Birthing Pod1",
	"Birthing Pod2",
	"Birthing Pod1",
	"Birthing Pod2",
	"Thoughtseize1",
	"Thoughtseize2",
	"Forest1",
	"Forest2",
	"Forest3",
	"Gavony Township1",
	"Gavony Township2",
	"Godless Shrine1",
	"Marsh Flats1",
	"Overgrown Tomb1",
	"Overgrown Tomb2",
	"Plains1",
	"Razorverge Thicket1",
	"Razorverge Thicket2",
	"Razorverge Thicket1",
	"Swamp1",
	"Temple Garden1",
	"Verdant Catacombs1",
	"Verdant Catacombs2",
	"Verdant Catacombs1",
	"Verdant Catacombs2",
	"Windswept Heath1",
	"Windswept Heath2",
	"Windswept Heath3",
	"Windswept Heath4",
]


def shuffle(deck):
	for i in xrange(len(deck)):
		s = random.randint(0, len(deck)-1)
		t = deck[s]
		deck[s] = deck[i]
		deck[i] = t

	return deck

def get_seed(test,h,m_start=0):
    global basedeck
    seed_format = '2015-01-18T%02d:%02d:%02d.%02d'
    for m in range(m_start,59):
        for s in xrange(60):
            for mili in xrange(100):
                seed = seed_format % (h,m,s,mili)
                random.seed(seed)
                deck = basedeck[:]
                deck = shuffle(deck)
                tmp = "\', \'".join(deck[:7])
                tmp = "[\'" + tmp + "\']"
                
                if test == tmp:
                    return seed
    return ''
                        

def get_response(seed):
    global basedeck
    random.seed(seed)
    basedeck = shuffle(basedeck)
    return ','.join(basedeck[7:20])
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

for count in range(0,20):
    data = sock.recv(1024)
    data = data.rstrip('\r\n')
        
    seed = get_seed(data, datetime.datetime.now().hour-1, datetime.datetime.now().minute)
    print ('Seed %02d : ' + seed) % count
    
    resp = get_response(seed)    
    sock.send(resp + '\n')

sock.recv(1024)
flag = sock.recv(1024)
print 'FLAG: ' + flag


#####################################
# $ python2.7 crypto_mtgo.py        #
# Seed 00 : 2015-01-18T11:18:28.07  #
# Seed 01 : 2015-01-18T11:18:28.42  #
# Seed 02 : 2015-01-18T11:18:28.83  #
# Seed 03 : 2015-01-18T11:18:29.20  #
# Seed 04 : 2015-01-18T11:18:29.57  #
# Seed 05 : 2015-01-18T11:18:29.93  #
# Seed 06 : 2015-01-18T11:18:30.30  #
# Seed 07 : 2015-01-18T11:18:30.68  #
# Seed 08 : 2015-01-18T11:18:31.08  #
# Seed 09 : 2015-01-18T11:18:31.50  #
# Seed 10 : 2015-01-18T11:18:31.89  #
# Seed 11 : 2015-01-18T11:18:32.28  #
# Seed 12 : 2015-01-18T11:18:32.67  #
# Seed 13 : 2015-01-18T11:18:33.07  #
# Seed 14 : 2015-01-18T11:18:33.46  #
# Seed 15 : 2015-01-18T11:18:33.86  #
# Seed 16 : 2015-01-18T11:18:34.27  #
# Seed 17 : 2015-01-18T11:18:34.71  #
# Seed 18 : 2015-01-18T11:18:35.13  #
# Seed 19 : 2015-01-18T11:18:35.55  #
# FLAG: All is known, flee at once. #
#####################################
