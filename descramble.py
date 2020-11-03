import numpy as np
import sys

def to_num(a):
    s = 0
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
        s |= r << i
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


def to_arr(dw):
	arr = np.zeros(32)
	for i in range(0,32):
		if dw & ( 1 << i ):
			arr[i] = 1
	return arr

ord_left_x = np.array([58,71,69,57,56,68,55,43,42,49,48,41,40,47,46,39,36,45,44,35,34,38,37,33,27,20,21,26,25,19,18,24,23,16,2,17])
ord_right_a = np.array([8,6,13])
ord_right_b = np.array([7,11,10,14,9,4,12,15,5,1,67,65])
ord_right_c = np.array([59,66,54,60,61,53,52,62,64,51,30,63,32,29,3,31,28,0,22,50])

def mapr(l0,l1,r0,r1):
    sh = np.shape(l0)
    uopx = np.zeros((sh[0],72+5+2+1), dtype=l0.dtype)
    uopy = np.zeros((sh[0],72+5+2+1), dtype=l0.dtype)
    uopz = np.zeros((sh[0],72+5+2+1), dtype=l0.dtype)
    uopx[::,ord_left_x] = l0[::,0:36]
    uopy[::,ord_left_x] = l0[::,36:36*2]
    uopz[::,ord_left_x] = l0[::,36*2:36*3]
    uopx[::,ord_right_a] = r0[::,0:3]
    uopy[::,ord_right_a] = r0[::,3:6]
    uopz[::,ord_right_a] = r0[::,6:9]
    uopx[::,ord_right_b] = r0[::,9:21]
    uopy[::,ord_right_b] = r0[::,21:33]
    uopz[::,ord_right_b] = r0[::,33:45]
    uopx[::,ord_right_c] = r0[::,45:65]
    uopy[::,ord_right_c] = r0[::,65:85]
    uopz[::,ord_right_c] = r0[::,85:105]
    uopx[::,70] = r1[::,6]
    uopy[::,70] = r1[::,9]
    uopz[::,70] = l1[::,2]
    remdr = l1[:,[0,1]]
    lmx = l1[::,[3]]
    lmy = l1[::,[4]]
    lmz = l1[::,[5]]
    rmx = r1[::,[0,3,7,8]]
    rmy = r1[::,[1,4,10,11]]
    rmz = np.empty(np.shape(rmy))
    rmz[::,0:2] = r1[::,[2,5]]
    uopx[:,72] = lmx[:,0]
    uopy[:,72] = lmy[:,0]
    uopz[:,72] = lmz[:,0]
    uopx[:,73:77] = rmx[:,:]
    uopy[:,73:77] = rmy[:,:]
    uopz[:,73:77] = rmz[:,:]
    uopx[:,77:79] = remdr
    uopy[:,77:79] = remdr
    uopz[:,77:79] = remdr
    _uopx = np.zeros((sh[0],72+5+2+1), dtype=l0.dtype)
    _uopy = np.zeros((sh[0],72+5+2+1), dtype=l0.dtype)
    _uopz = np.zeros((sh[0],72+5+2+1), dtype=l0.dtype)
    _uopx[:,0:72] = uopx[:,0:72][:,::-1]
    _uopy[:,0:72] = uopy[:,0:72][:,::-1]
    _uopz[:,0:72] = uopz[:,0:72][:,::-1]
    _uopx[:,72:80] = uopx[:,72:80]
    _uopy[:,72:80] = uopy[:,72:80]
    _uopz[:,72:80] = uopz[:,72:80]

    return _uopx, _uopy, _uopz

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
	addr = int(sa[0], 16) / 8
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

nops = maxadd-minadd+1
base = minadd * 4
left_0a = np.zeros((nops,108))
left_1a = np.zeros((nops,6))
right_0a = np.empty((nops,105))
right_1a = np.empty((nops,12))

for i,dwe in dwelist:
	i = i - minadd
	left_0a [i,  0: 21] = to_arr(dwe[0])[10:31]
	left_0a [i, 21: 52] = to_arr(dwe[1])[ 0:31]
	left_0a [i, 52: 83] = to_arr(dwe[2])[ 0:31]
	left_0a [i, 83:108] = to_arr(dwe[3])[ 0:25]
	left_1a [i,  0:  6] = to_arr(dwe[3])[25:31]
	right_1a[i,  0: 12] = to_arr(dwe[4])[ 7:19]
	right_0a[i,  0: 12] = to_arr(dwe[4])[19:31]
	right_0a[i, 12: 43] = to_arr(dwe[5])[ 0:31]
	right_0a[i, 43: 74] = to_arr(dwe[6])[ 0:31]
	right_0a[i, 74:105] = to_arr(dwe[7])[ 0:31]

x,y,z = mapr(left_0a,left_1a,right_0a,right_1a)

for i in range(0, nops):
	xn = to_num(x[i])
	yn = to_num(y[i])
	zn = to_num(z[i])
	addr = base + i * 4
	s = "%04X: %020X %020X %020X"%(addr, xn, yn, zn)
	print s
