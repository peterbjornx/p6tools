import numpy as np
import sys
from uc_isa import *

label_addrs = {}

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

def asm_op(ops):
	if len(ops) is len("OP_000") and ops.startswith("OP_"):
		return int(ops[3:],16)
	if ops in uop_map_inv:
		return uop_map_inv[ops]
	i = ops.rfind("_")
	baseop = ops[:i]
	sfx = ops[i+1:]
	if baseop in aop_map_inv:
		op = aop_map_inv[baseop]
		if not sfx in dsz_map_inv:
			print "Invalid DSZ in op \"%s\""%ops
			quit()
		op |= dsz_map_inv[sfx]
		return op
	if baseop in ccuop_map_inv:
		op = ccuop_map_inv[baseop]
		if sfx in cc_map_inv:
			op |= cc_map_inv[sfx]
		elif sfx == "<MCC>":
			return op		
		else:
			print "Invalid CC in op \"%s\""%ops
			quit()
		return op
	spl = ops.split("_")
	if spl[0] in memop_map_inv:
		op = memop_map_inv[spl[0]]
		sc = spl[1]
		if sc in sc_map_inv:
			op |= sc_map_inv[sc] << 4
		else:
			print "Invalid SC in op \"%s\""%ops
			quit()			
		ds = spl[2]
		if ds in dsz_map_inv:
			op |= dsz_map_inv[ds]
		else:
			print "Invalid DS in op \"%s\""%ops
			quit()			
		return op
	print "Unknown op: ", ops, spl[0]
	quit()

def asm_reg(rs):
	if rs in reg_map_inv:
		return reg_map_inv[rs],0,0
	elif len(rs) is len("REG_00") and rs.startswith("REG_"):
		return int(rs[4:],16),0,0
	elif rs == "CONST_0":
		return 0,0,0
	elif rs == "M_IMM":
		return 0,0x11,0
	elif rs == "REG_OP_Size":
		return 0,0x11,0x10
	elif rs == "virt_ip":
		return 0,0x11,0x11
	elif rs == "next_virt_ip":
		return 0,0x11,0x12
	elif rs.startswith("ALIAS_"):
		return 0,0x11,int(rs[6:],16)
	elif rs.startswith("CONSTROM_"):
		return 0,0x0C,int(rs[9:],16)
	elif rs.startswith("CONST_"):
		return 0,int(rs[6:8],16),int(rs[9:],16)
	elif rs in creg_map_inv:
		return 0,0xe,creg_map_inv[rs]
	else:
		print "Unknown register spec: ", rs
		quit()

def asm_btarg(addr):
	if addr.startswith("UROM_"):
		return int(addr[5:],16)
	elif addr in label_addrs:
		return label_addrs[addr]
	print "Undefined label was referenced: \"%s\""%addr
	quit()

def asm_flow(s):
	f = 0
	for i in s.split("_"):
		f |= flowm_map_inv[i]
	return f

def assemble(l, pass_no):
	l = ' '.join(l.strip().split(";")[0].strip().split())
	if not l:
		return
	i = l.find(" ")
	addr_str = l[0:i]
	if addr_str[0:5] != "UROM_" or len(addr_str) > 9:
		print "Address should be UROM_XXXX in line: \n%s"%l
		quit()
	else:
		addr = int(addr_str[5:],16)
	l = l[i:].strip()
	i = l.find(":")
	if i != -1:
		lbl = l[:i]
		if pass_no == 0:
			label_addrs[lbl] = addr
		return
	elif pass_no == 0:
		return
	i = l.find("=")
	fms = ""
	if i != -1:
		dest = l[:i].strip()
		l = l[i+1:].strip()
		opcl  = dest.split(" ")
		if len(opcl) == 2:
			fms = opcl[0]
			dest = opcl[1]	
	else:
		dest = "SINK"
	ibro = l.find("(")
	ibrc = l.rfind(")")
	opcl  = l[:ibro].strip().split(" ")
	if len(opcl) == 2:
		fms = opcl[0]
		opc = opcl[1]	
	else:
		opc = l[:ibro].strip()
	parl  = l[ibro+1:ibrc].strip()
	pars  = [ s.strip() for s in parl.split(",") ]
	op    = asm_op(opc)
	ldst  = asm_reg(dest)
	lsrc1 = asm_reg(pars[0])
	ubr   = is_ubranch(op) or is_subranch(op)
	if ubr:
		btarg = asm_btarg(pars[1])
		lsrc2 = (0,0,0)
	else:	
		lsrc2 = asm_reg(pars[1])
	flow = asm_flow(fms)
	immp = 0,0,0
	lseg = 0
	u1 = 0
	u2 = 0
	u3 = 0
	oa = 0
	
	immv  = lsrc1[2] | lsrc2[2]
	imma  = lsrc1[1] | lsrc2[1]
	for p in pars[2:]:
		if p in seg_map_inv:
			lseg = seg_map_inv[p]
		elif p.startswith("U1_"):
			u1 = int(p[3:],16)
		elif p.startswith("U2_"):
			u2 = int(p[3:],16)
		elif p.startswith("U3_"):
			u3 = int(p[3:],16)
		elif p.startswith("OA_"):
			oa = int(p[3:],16)
		elif p.startswith("IA_"):
			imma = int(p[3:],16)
		else:
			immp = asm_reg(p)
			immv |= immp[2]
			imma |= immp[1]
	lsrc1 = lsrc1[0]
	lsrc2 = lsrc2[0]
	if ubr:
		lsrc2 = (btarg >> 9) & 0xff
		#imma = 0x11
		immv = btarg & 0x1ff
	p = np.zeros(80)
	p[ 0: 4] = to_arr(flow,4)
	p[ 4:13] = to_arr(immv,9)
	p[13:18] = to_arr(imma,5)
	p[18:22] = to_arr(lseg,4)
	p[22:23] = to_arr(u1,1)
	p[23:31] = to_arr(ldst[0],8)
	p[31:39] = to_arr(lsrc1,8)
	p[39:47] = to_arr(lsrc2,8)
	p[47:56] = to_arr(u2,9)
	p[56:68] = to_arr(op,12)
	p[68:72] = to_arr(oa,4)
	p[72:80] = to_arr(u3,8)
	return addr, p


fli = open(sys.argv[1],'r')

for l in fli:
	assemble(l,0)

fli.close()


fli = open(sys.argv[1],'r')
minaddr = None
maxaddr = 0
uops = {}
for l in fli:
	r = assemble(l,1)
	if r is None:
		continue
	addr, uop = r
	if addr < minaddr or minaddr is None:
		minaddr = addr
	if addr > maxaddr:
		maxaddr = addr
	uops[addr] = uop
	if addr &3 == 3:
		print "Bad address %04X"%addr

fli.close()
minaddr &= ~0x3
for addr in range(minaddr, maxaddr, 4):
	print "%04X: %s %s %s"%(addr,print_hex(uops[addr]),print_hex(uops[addr+1]),print_hex(uops[addr+2]))



