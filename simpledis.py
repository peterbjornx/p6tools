import numpy as np
import sys
from uc_isa import *

def print_one(a):
    r = ""
    for i in a:
        if i:
            r += "1 "
        else:
            r += "_ "
    return r

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

def signext9(i):
    if i < 0x100:
      return i
    else:
      return (-1 & ~0x1FF) | ( i & 0x1FF )
# 04 - Offset in memory address, ?sign extend?
# 06 - Offset 0 in memory address
# 0E - Control register addresses
# 0C - Constant ROM
# 11 - Alias/Jump target?
# 16 - General purpose literal, sign extend
def printimmc(a,i):
    if a == 0x11:
        if i == 0x0:
            return "M_IMM"
        elif i == 0x10:
            return "REG_OP_Size"
        elif i == 0x11:
            return "virt_ip"
        elif i == 0x12:
            return "next_virt_ip"
        else:
            return "ALIAS_%03x"%i
    elif a == 0x0C:
	return "CONSTROM_%03X"%i
    elif a == 0 and i == 0:
        return "CONST_0"
    else:
        return "CONST_%02x_%03x"%(a,i)

def immc_is_zero(a,i):
    if a == 0x11:
	return False
    elif a == 0x0C:
	return False
    elif a == 0x16:
        return i == 0
    elif a == 0x04:
	return i == 0
    elif a == 0 and i == 0:
	return i == 0
    else:
        return "CONST_%02x_%03x"%(a,i)

def strreg(i,a,ai,op = 0):
    if i == 0:
	if (op == 0x31 or op == 0x32) and a == 0xe and ai in creg_map:
		return creg_map[ai]
        return printimmc(a,ai)
    elif i in regmap:
        return regmap[i]
    else:
        return "REG_%02X"%i



def strop(i,opa):
    if opa == 0x2 and i in ccuop_map:
        return ccuop_map[i&0xFF0]+"_<MCC>"
    if opa == 0x6:
        op = i
        if (i & 0xC7F) == 0x400:
            return "<MGRP0>_"+dsz_map[i&dsz_msk]
        elif op == 0x420:
            return "<MGRP1>"
    if (i & 0xC7F) in arith_op and (i&dsz_msk) in dsz_map:
        return arith_op[i&0xC7F] +"_"+ dsz_map[i&dsz_msk]
    elif i in uop_map:
        return uop_map[i]
    elif (i & 0xFF0)in ccuop_map:
        return ccuop_map[i&0xff0]+"_"+cc_map[i&0xf]
    elif (i & 0xC4F) in memop_map:
	return memop_map[i & 0xC4F ] +"_"+ scstr[(i >> 4)&0x3]+"_"+dsz_map[i&dsz_msk]
    else:
        return "OP_%03X"%i


"""
 |  7    |              6        |          5      |            4  |               |3              | |  2    |         |    1            |      0|
 |1 0 9 8|7 6 5 4 3 2 1 0 9 8 7 6|5 4 3 2 1 0 9 8 7|6 5 4 3 2 1 0 9|8 7 6 5 4 3 2 1|0 9 8 7 6 5 4 3|2|1 0 9 8|7 6 5 4 3|2 1 0 9 8 7 6 5 4|3 2 1 0|
 +-------+-----------------------+-----------------+---------------+---------------+---------------+-+-------+---------+-----------------+-------+
 |opalias|         opcode        |                 |     LSrc2     |     LSrc1     |     LDest     | |  LSeg | ImmAlias|    Immediate    | FlowM |

 <LDest> = <LSrc1> <Op> <LSrc2>
"""

def printuop(p):
    flow  = p[0:4]
    imm   = to_num(p[4:13])
    ali   = to_num(p[13:18])
    lseg  = to_num(p[18:22])
    unk1  = to_num(p[22:23])
    ldst  = to_num(p[23:31])
    lsrc1 = to_num(p[31:39])
    lsrc2 = to_num(p[39:47])
    unk2  = to_num(p[47:56])
    op    = to_num(p[56:68])
    opa   = to_num(p[68:72])
    unk3  = to_num(p[72:80])
    ubtrg = lsrc2 << 9 | imm

    flows = ""
    if flow[0] and flow[1]:
        flows = "SGLUOP"
    elif flow[0]:
        flows = "BOM"
    elif flow[1]:
        flows = "EOM"
    if flow[2] > 0.1:
        flows += "_Fl2"
    if flow[3] > 0.1:
        flows += "_Fl3"


    iscrr  = op == 0x32
    ismove = (op & 0xc3f) == 0x400
    ubranch = is_ubranch(op)
    subranch = is_subranch(op)
    memop = (op&0xC0F) in memop_map
    dreg = ""
    btarg = "UROM_%04x"%ubtrg
    if printraw:
	print print_hex(p),
    if ubtrg in labels:
        btarg = labels[ubtrg]

    if ldst != 0x1:
	    dreg = "%-11s = "%strreg(ldst,0,0)
    if subranch and lsrc1 == 0:
        print "%-10s %-15s%-15s(%-14s, %-14s"%(flows,dreg,strop(op,opa), "CONST", btarg,),
    elif ubranch:
        print "%-10s %-15s%-15s(%-14s, %-14s"%(flows,dreg,strop(op,opa), strreg(lsrc1,ali,imm,op),btarg),
    elif ismove and lsrc1 == 0 and lsrc2 == 0:
        print "%-10s %-15s%-15s(%-14s, %-14s"%(flows,dreg,strop(op,opa), "CONST", strreg(lsrc2,ali,imm,op),),
    else:
        print "%-10s %-15s%-15s(%-14s, %-14s"%(flows,dreg,strop(op,opa), strreg(lsrc1,ali,imm,op),strreg(lsrc2,ali,imm,op)),
    if (imm != 0 or ali != 0) and not (lsrc1 == 0 or lsrc2 == 0 or ubranch):
        print ", %-14s"%printimmc( ali, imm ),
    #else:
    #    print "                ",
    if lseg != 0:
        print ", %-8s"%segs[lseg],
    #else:
    #    print "          ",
    if opa != 0:
        print ", OA_%01x"%opa,
    #else:
    #    print "       ",
    if ali != 0 and (ubranch or subranch):
        print ", IA_%02x"%ali,
    #else:
    #    print "       ",
    if unk1 != 0:
        print ", U1_%01x"%unk1,
    #else:
    #    print "      ",
    if unk2 != 0:
        print ", U2_%02x"%unk2,
    #else:
    #    print "       ",
    if unk3 != 0:
        print ", U3_%02x"%unk3,
    #else:
    #    print "       ",
    print ")"
    if flow[1] or (op&0xfbf) == 0x210:
	print "\n"

labels = {
	0x2EF8: "MACRO_cpuid",
	0x2F04: "cpuid_skip_sign",
	0x2F09: "cpuid_leaf0",
	0x2F10: "cpuid_try_leaf1",
	0x2351: "MACRO_wrmsr",
	0x2B64: "patch_load",
	0x22D8: "copy_seg_to_scp",
	0x15B2: "copy_scp_to_seg",
	0x0C61: "wrmsr_core",
	0x0CF0: "rwmsr_done",
	0x0CF1: "rwmsr_crbus",
	0x1D1D: "read_msrmap",
	0x1F4E: "msr_throw_gpf",
	0x0E66: "rdmsr_PROBE_GP_REG",
	0x3405: "wrmsr_PROBE_GP_REG",
	0x1F55: "rdmsr_PROBE_TO_PDR",
	0x3054: "debug_wrmsr_table",
	0x305C: "debug_rdmsr_table",
	0x1E88: "debugmsr_EOM",
	0x1F19: "rdmsr_PROBE_SEG_REG_1",
	0x1E81: "rdmsr_PROBE_SEG_REG_2",
	0x1F12: "rdmsr_PROBE_SEG_REG_3",
	0x1F0C: "wrmsr_PROBE_SEG_REG_1",
	0x1EFE: "wrmsr_PROBE_SEG_REG_2",
	0x1EF8: "wrmsr_PROBE_SEG_REG_3",
}
refs = {}

def findlabel(i,p):
    flow  = p[0:4]
    imm   = to_num(p[4:13])
    ali   = to_num(p[13:18])
    lseg  = to_num(p[18:22])
    unk1  = to_num(p[22:23])
    ldst  = to_num(p[23:31])
    lsrc1 = to_num(p[31:39])
    lsrc2 = to_num(p[39:47])
    unk2  = to_num(p[47:56])
    op    = to_num(p[56:68])
    opa   = to_num(p[68:72])
    ubtrg = lsrc2 << 9 | imm


    iscrr  = op == 0x32
    ismove = (op & 0xc3f) == 0x400
    ubranch = is_ubranch(op)
    subranch = is_subranch(op)
    memop = (op&0xC0F) in memop_map

    if ubranch or subranch:
	if ubtrg &3 == 3 or ubtrg > 0x4000:
		return
	if not (ubtrg in labels):
		labels[ ubtrg ] = "addr_%X"%ubtrg
	if not (ubtrg in refs):
		refs[ ubtrg ] = []
	refs[ubtrg].append(i)

def printlbl(i):
    if i in labels:
        print "\nUROM_%04X"%i, labels[i]+": ;  refd by: ",

	if i in refs:
		for ri in refs[i]:
			print "UROM_%04X"%ri,
	print ""



def to_arr(dw,l):
	arr = np.zeros(l)
	for i in range(0,l):
		if dw & ( 1 << i ):
			arr[i] = 1
	return arr

rgl = []

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
base = minadd


for i,dwe in dwelist:
	i = (i - minadd) / 4
	x[i,:] = to_arr(dwe[0],80)
	y[i,:] = to_arr(dwe[1],80)
	z[i,:] = to_arr(dwe[2],80)

for i in range(0,nops):
    findlabel(i*4+base  ,x[i,:])
    findlabel(i*4+base+1,y[i,:])
    findlabel(i*4+base+2,z[i,:])

printraw = False

for i in range(0,nops):
	printlbl(i*4+base)
	print "UROM_%04X\t"%(i*4+base),
        printuop(x[i,:])
	printlbl(i*4+1+base)
	print "UROM_%04X\t"%(i*4+1+base),
        printuop(y[i,:])
	printlbl(i*4+2+base)
	print "UROM_%04X\t"%(i*4+2+base),
        printuop(z[i,:])
