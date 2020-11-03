import numpy as np
import sys

def to_num_b(a):
    s = 0
    for i in range(0,len(a)):
        if a[i] > 0.5:
        	s |= 1 << i
    return s

def print_hex(a):
    s = ""
    for i in range(0,len(a),4):
        b = a[i:i+4]
        r=0
        if b[0] > 0.5:
            r += 1
        if len(b) >= 2 and b[1] > 0.5:
            r += 2
        if len(b) >= 3 and b[2] > 0.5:
            r += 4
        if len(b) >= 4 and b[3] > 0.5:
            r += 8
        h = "0123456789ABCDEF"[int(r)]
        s += h
    return s[::-1]


def to_arr(dw,l=32):
	arr = np.zeros(l)
	for i in range(0,l):
		if dw & ( 1 << i ):
			arr[i] = 1
	return arr

ord_left_x = np.array([58,71,69,57,56,68,55,43,42,49,48,41,40,47,46,39,36,45,44,35,34,38,37,33,27,20,21,26,25,19,18,24,23,16,2,17])
ord_right_a = np.array([8,6,13])
ord_right_b = np.array([7,11,10,14,9,4,12,15,5,1,67,65])
ord_right_c = np.array([59,66,54,60,61,53,52,62,64,51,30,63,32,29,3,31,28,0,22,50])

def scramble(_uopx,_uopy,_uopz):
    nops = np.shape(_uopx)[0]
    uopx = np.zeros((nops,72+5+2+1), dtype=_uopx.dtype)
    uopy = np.zeros((nops,72+5+2+1), dtype=_uopx.dtype)
    uopz = np.zeros((nops,72+5+2+1), dtype=_uopx.dtype)
    uopx[:,0:72] = _uopx[:,0:72][:,::-1]
    uopy[:,0:72] = _uopy[:,0:72][:,::-1]
    uopz[:,0:72] = _uopz[:,0:72][:,::-1]
    uopx[:,72:80] = _uopx[:,72:80]
    uopy[:,72:80] = _uopy[:,72:80]
    uopz[:,72:80] = _uopz[:,72:80]
    l0 = np.zeros((nops,108))
    l1 = np.zeros((nops,6))
    r0 = np.zeros((nops,105))
    r1 = np.zeros((nops,12))
    lmx = np.zeros((nops,1))
    lmy = np.zeros((nops,1))
    lmz = np.zeros((nops,1))
    rmx = np.zeros((nops,4))
    rmy = np.zeros((nops,4))
    rmz = np.zeros((nops,4))
    l0[::,0:36]    = uopx[::,ord_left_x]
    l0[::,36:36*2] = uopy[::,ord_left_x]
    l0[::,36*2:36*3] = uopz[::,ord_left_x]
    r0[::,0:3] = uopx[::,ord_right_a]
    r0[::,3:6] = uopy[::,ord_right_a]
    r0[::,6:9] = uopz[::,ord_right_a]

    r0[::,9:21]  = uopx[::,ord_right_b]
    r0[::,21:33] = uopy[::,ord_right_b]
    r0[::,33:45] = uopz[::,ord_right_b]

    r0[::,45:65] = uopx[::,ord_right_c]
    r0[::,65:85] = uopy[::,ord_right_c]
    r0[::,85:105] = uopz[::,ord_right_c]
    r1[::,6] = uopx[::,70]
    r1[::,9] = uopy[::,70]
    l1[::,2] = uopz[::,70]
    lmx[:,0] = uopx[:,72]
    lmy[:,0] = uopy[:,72]
    lmz[:,0] = uopz[:,72]
    rmx[:,:] = uopx[:,73:77]
    rmy[:,:] = uopy[:,73:77]
    rmz[:,:] = uopz[:,73:77]
    remdr1 = uopx[:,77:79]
    remdr2 = uopy[:,77:79]
    remdr3 = uopz[:,77:79]
    #TODO: Better combine
    remdr = remdr1
    l1[:,[0,1]] = remdr
    l1[::,[3]] = lmx
    l1[::,[4]] = lmy
    l1[::,[5]] = lmz
    r1[::,[0,3,7,8]] = rmx
    r1[::,[1,4,10,11]] = rmy
    r1[::,[2,5]] = rmz[::,0:2]

    return l0,l1,r1,r0

fli = open(sys.argv[1],'r')

base = 0
if len(sys.argv) >= 4:
	base = eval(sys.argv[2])

dwelist = []
maxadd = 0
minadd = None
for l in fli:
	l = l.strip()
	if not l:
		continue
	sa = l.split(": ")
	addr = int(sa[0], 16)
	if addr > maxadd:
		maxadd = addr
	if minadd is None or addr < minadd:
		minadd = addr
	sb = sa[1].split(" ")
	dwe = []
	for s in sb:
		dwe.append(int(s,16))
	dwelist.append((addr,dwe))
fli.close()

nops = maxadd-minadd+4
nops = nops / 4
x = np.zeros((nops,80))
y = np.zeros((nops,80))
z = np.zeros((nops,80))
base = minadd / 4


for i,dwe in dwelist:
	i = (i - minadd) / 4
	x[i,:] = to_arr(dwe[0],80)
	y[i,:] = to_arr(dwe[1],80)
	z[i,:] = to_arr(dwe[2],80)

la,lm,rm,ra = scramble(x,y,z)

def to_dwenc(la,lm,rm,ra):
	return [
		to_num_b(la[ 0: 21]) << 10, to_num_b(la[21: 52]),
		to_num_b(la[52: 83]),
		to_num_b(la[83:108]) | (to_num_b(lm[0:6]) << 25),
		(to_num_b(rm[ 0: 12]) << 7) | (to_num_b(ra[0:12]) << 19),
		to_num_b(ra[12: 43]),
		to_num_b(ra[43: 74]),
		to_num_b(ra[74:105])]

for i in range(0,nops):
	dwe = to_dwenc(la[i],lm[i],rm[i],ra[i])
	s = "%04X: "%((i + base)*8)
	for j in dwe:
		s += "%08X "%j
	print s[:-1]
