regmap = {
    0: "CONST",
    1: "SINK",
    2: "TMP0",
    3: "TMP1",
    4: "TMP2",
    5: "TMP3",
    6: "TMP4",
    7: "TMP5",

    0x08: "AL",
    0x09: "CL",
    0x0A: "DL",
    0x0B: "BL",
    0x0C: "AH",
    0x0D: "CH",
    0x0E: "DH",
    0x0F: "BH",

    0x10: "ST0",
    0x11: "ST1",
    0x12: "ST2",
    0x13: "ST3",
    0x14: "ST4",
    0x15: "ST5",
    0x16: "ST6",
    0x17: "ST7",

    0x18: "TMP6",
    0x19: "TMP7",
    0x1A: "TMP8",
    0x1B: "TMP9",
    0x1C: "TMPA",
    0x1D: "TMPB",
    0x1E: "FSW",
    0x1F: "SystemFlags",

    0x24: "FCC",
    0x25: "ArithFLAGS",

    0x28: "AX",
    0x29: "CX",
    0x2A: "DX",
    0x2B: "BX",
    0x2C: "SP",
    0x2D: "BP",
    0x2E: "SI",
    0x2F: "DI",

    0x33: "EIP_30",
    0x34: "R34",
    0x35: "R35",
    0x36: "R36",
    0x38: "EAX",
    0x39: "ECX",
    0x3A: "EDX",
    0x3B: "EBX",
    0x3C: "ESP",
    0x3D: "EBP",
    0x3E: "ESI",
    0x3F: "EDI",

    0x54: "ST(i)",
    0x5A: "MM_sss",
    0x5E: "MM_ddd",

    0x78: "IREG_op",

    0x88: "EAX_OPSZ",
    0x89: "ECX_OPSZ",
    0x8A: "EDX_OPSZ",
    0x8B: "EBX_OPSZ",
    0x8C: "ESP_OPSZ",
    0x8D: "EBP_OPSZ",
    0x8E: "ESI_OPSZ",
    0x8F: "EDI_OPSZ",

    0x99: "ECX_10",
    0x9B: "EBX_10",
    0x9E: "ESI_10",
    0x9F: "EDI_10",

    0xA8: "EAX_20",
    0xA9: "ECX_20",
    0xAA: "EDX_20",
    0xAB: "EBX_20",
    0xAC: "ESP_20",
    0xAD: "EBP_20",

    0xC4: "REG_op",
    0xC8: "REG_sss",
    0xCC: "REG_ddd",

}
reg_map_inv = {v: k for k, v in regmap.items()}

arith_op = {
    0x400: "MOVE",
    0x401: "AOP1",
    0x402: "AOP2",
    0x403: "AOP3",
    0x404: "BTEST",
    0x405: "BTS",
    0x406: "BTR",
    0x407: "BTC",
    0x408: "ADD",
    0x409: "OR",
    0x40A: "ADC",
    0x40B: "SBC",
    0x40C: "AND",
    0x40D: "SUB",
    0x40E: "XOR",
    0x40F: "SUBR",
    0x420: "ROL",
    0x421: "ROR",
    0x422: "RCL",
    0x423: "RCR",
    0x424: "SHL",
    0x425: "SHR",
    0x426: "SAL",
    0x427: "SAR",
    0x46F: "WUCONCAT",
}
aop_map_inv = {v: k for k, v in arith_op.items()}
aop_map_inv["<MGRP0>"] = 0x400

uop_map = {
    0x021: "BSWAP",
    0x022: "FNSTSW?",
    0x024: "FXORS",
    0x02A: "SIGEVENT",
    0x030: "FREADROM",
    0x031: "MOVETOCREG",
    0x032: "MOVEFROMCREG",
    0x033: "WRSEGFLD",
    0x03A: "RDSEGFLD",
    0x0E0: "MERGE",
    0x090: "TRANSPORTUIP",
    0x160: "INTEXTRACT.HI32",
    0x161: "INTEXTRACT.HI16",
    0x1C0: "FLAG_EXTRACT",
    0x1C6: "FLAG_SET",
    0x210: "U_JMP",
    0x250: "U_JMP_NT",
    0x212: "M_CALL",
    0x214: "M_JMP_REL",
    0x225: "FSQRT",
    0x226: "FEXAMINE",
    0x22F: "FCOMPARE",
    0x26B: "FSELECT",
    0x290: "U_JMP_INDIR",
    0x2D0: "U_JMP_INDIR_N",
    0x291: "M_RET",
    0x294: "M_JMP",
    0x414: "BSF",
    0x415: "BSR",
    0x461: "MUL",
    0x463: "IMUL",
    0x464: "DIV",
    0x466: "IDIV",
    0x611: "AAS",
    0x612: "DAA",
    0x613: "DAS",
    0x630: "STRD",
    0x7EB: "FPNORM",
}
uop_map_inv = {v: k for k, v in uop_map.items()}
uop_map_inv["<MGRP1>"] = 0x420

ccuop_map = {
    0x180: "SETcc",
    0x240: "CMOV",
    0x310: "U_JCC_T", # Possibly 350
    0x350: "U_JCC_N", # Possibly 350
    0x390: "U_JCC_I_T",
    0x3D0: "U_JCC_I_N",
}

ccuop_map_inv = {v: k for k, v in ccuop_map.items()}

memop_map = {
	0x800: "STA",
	0x804: "LOAD",
	0x840: "STA40",
	0x844: "LOAD40",
	0xC03: "PORTOUT",
	0xC05: "PORTIN",
	0xC43: "PORTOUT40",
	0xC45: "PORTIN40",
	0xC00: "LEA",
	0xC40: "LEA40",
}
memop_map_inv = {v: k for k, v in memop_map.items()}

cc_map = [
    "O",  # 0
    "NO", # 1
    "C",  # 2
    "NC", # 3
    "Z",  # 4
    "NZ", # 5
    "NA", # 6
    "A",  # 7
    "S",  # 8
    "NS", # 9
    "P",  # A
    "NP", # B
    "L",  # C
    "NL", # D
    "NG", # E
    "G"   # F
]

cc_map_inv = {v: k for k, v in enumerate(cc_map)}

scstr = [
    "SC1",
    "SC2",
    "SC4",
    "SC8"
]

sc_map_inv = {v: k for k, v in enumerate(scstr)}


dsz_map = {
	0x000: "DSZ?",
	0x100: "DSZ16",
	0x200: "DSZ32",
	0x080: "DSZ8",
	0x300: "DSZ64",
}
dsz_map_inv = {v: k for k, v in dsz_map.items()}
dsz_msk = 0x380

creg_map = {
	0x000: "CR_MTRR_PHYSBASE0_L",
	0x001: "CR_MTRR_PHYSBASE0_H",
	0x002: "CR_MTRR_PHYSMASK0_L",
	0x003: "CR_MTRR_PHYSMASK0_H",
	0x004: "CR_MTRR_PHYSBASE1_L",
	0x005: "CR_MTRR_PHYSBASE1_H",
	0x006: "CR_MTRR_PHYSMASK1_L",
	0x007: "CR_MTRR_PHYSMASK1_H",
	0x008: "CR_MTRR_PHYSBASE2_L",
	0x009: "CR_MTRR_PHYSBASE2_H",
	0x00A: "CR_MTRR_PHYSMASK2_L",
	0x00B: "CR_MTRR_PHYSMASK2_H",
	0x00C: "CR_MTRR_PHYSBASE3_L",
	0x00D: "CR_MTRR_PHYSBASE3_H",
	0x00E: "CR_MTRR_PHYSMASK3_L",
	0x00F: "CR_MTRR_PHYSMASK3_H",
	0x010: "CR_MTRR_PHYSBASE4_L",
	0x011: "CR_MTRR_PHYSBASE4_H",
	0x012: "CR_MTRR_PHYSMASK4_L",
	0x013: "CR_MTRR_PHYSMASK4_H",
	0x014: "CR_MTRR_PHYSBASE5_L",
	0x015: "CR_MTRR_PHYSBASE5_H",
	0x016: "CR_MTRR_PHYSMASK5_L",
	0x017: "CR_MTRR_PHYSMASK5_H",
	0x018: "CR_MTRR_PHYSBASE6_L",
	0x019: "CR_MTRR_PHYSBASE6_H",
	0x01A: "CR_MTRR_PHYSMASK6_L",
	0x01B: "CR_MTRR_PHYSMASK6_H",
	0x01C: "CR_MTRR_PHYSBASE7_L",
	0x01D: "CR_MTRR_PHYSBASE7_H",
	0x01E: "CR_MTRR_PHYSMASK7_L",
	0x01F: "CR_MTRR_PHYSMASK7_H",

	0x026: "CR_P5_MC_TYPE",

	0x028: "CR_P5_MC_ADDR_L",
	0x029: "CR_P5_MC_ADDR_H",

	0x02A: "EBL_CR_POWERON",

	0x02C: "BBL_CR_ADDR_L",
	0x02D: "BBL_CR_ADDR_H",
	0x02E: "CR_PLAT_ID_L",
	0x02F: "CR_PLAT_ID_H",

	0x030: "CR_MSR18_L",
	0x031: "CR_MSR18_H",
	0x033: "CR_TEST_CTL",
	0x036: "CR_APIC_BASE",

	0x043: "CR_DR0",
	0x044: "CR_DR1",
	0x045: "CR_DR2",
	0x046: "CR_DR3",
	0x047: "CR_DR7",


	0x062: "CR_A20MASK",#?
 	0x06B: "CR_CR3",



	0x0A0: "CR_MTRR_FIX_00000_L",
	0x0A1: "CR_MTRR_FIX_00000_H",
	0x0B0: "CR_MTRR_FIX_80000_L",
	0x0B1: "CR_MTRR_FIX_80000_H",
	0x0B2: "CR_MTRR_FIX_A0000_L",
	0x0B3: "CR_MTRR_FIX_A0000_H",
	0x0D0: "CR_MTRR_FIX_C0000_L",
	0x0D1: "CR_MTRR_FIX_C0000_H",
	0x0D2: "CR_MTRR_FIX_C8000_L",
	0x0D3: "CR_MTRR_FIX_C8000_H",
	0x0D4: "CR_MTRR_FIX_D0000_L",
	0x0D5: "CR_MTRR_FIX_D0000_H",
	0x0D6: "CR_MTRR_FIX_D8000_L",
	0x0D7: "CR_MTRR_FIX_D8000_H",
	0x0D8: "CR_MTRR_FIX_E0000_L",
	0x0D9: "CR_MTRR_FIX_E0000_H",
	0x0DA: "CR_MTRR_FIX_E8000_L",
	0x0DB: "CR_MTRR_FIX_E8000_H",
	0x0DC: "CR_MTRR_FIX_F0000_L",
	0x0DD: "CR_MTRR_FIX_F0000_H",
	0x0DE: "CR_MTRR_FIX_F8000_L",
	0x0DF: "CR_MTRR_FIX_F8000_H",
	0x0EE: "CR_PAT",
	0x0FE: "CR_MTRRDEFTYPE",

	0x100: "CR_CR0",
	0x101: "CR_CPL",#? MSR_PROBE_CPL in new CPUs

	0x110: "BBL_CR_D0_L",
	0x111: "BBL_CR_D0_H",
	0x112: "BBL_CR_D1_L",
	0x113: "BBL_CR_D1_H",
	0x114: "BBL_CR_D2_L",
	0x115: "BBL_CR_D2_H",
	0x116: "BBL_CR_D3_L",
	0x117: "BBL_CR_D3_H",
	0x118: "BBL_CR_DECC",
	0x119: "BBL_CR_CTL",
	0x11A: "BBL_CR_TRIG",
	0x11B: "BBL_CR_BUSY",
	0x11E: "BBL_CR_CTL3",

	0x160: "CR_SCP0_PDRL",
	0x161: "CR_SCP1_PDRH",
	0x162: "CR_SCP2",
	0x163: "CR_SCP3",
	0x164: "CR_SCP4",
	0x165: "CR_SCP5",
	0x166: "CR_SCP6",
	0x167: "CR_SCP7",
	0x168: "CR_SCP8",
	0x169: "CR_SCP9",
	0x16A: "CR_SCP10",
	0x16B: "CR_SCP11",
	0x16C: "CR_SCP12",
	0x16D: "CR_SCP13",
	0x16E: "CR_SCP14",
	0x16F: "CR_SCP15",
	#0x16E: "CR_SMM_IOR_EIP",

	0x170: "CR_SMREVID", # MSR_P6_CR_SMREVID
	0x171: "CR_SMBASE", # MSR_P6_CR_SMBASE

	0x174: "IA32_SYSENTER_CS",
	0x175: "IA32_SYSENTER_ESP",
	0x176: "IA32_SYSENTER_EIP",

	0x178: "CR_MTRRcap",
	0x179: "MCG_CAP",
	0x17A: "MCG_STATUS",
	0x17B: "CR_CR2",
	0x17C: "CR_CR4",
	0x17D: "CR_DR6",

	0x180: "CR_TSC_LOW",
	0x181: "CR_TSC_HIGH",
	0x182: "CR_PERFCTR0_L",
	0x183: "CR_PERFCTR0_H",
	0x184: "CR_PERFCTR1_L",
	0x185: "CR_PERFCTR1_H",
	0x186: "CR_EVNTSEL0",
	0x187: "CR_EVNTSEL1",
	0x188: "CR_MSRPLA_ADDR",
	0x189: "CR_MSRPLA_DATA",

	0x1B8: "MS_CR_MATCHPATCH0",
	0x1B9: "MS_CR_MATCHPATCH1",
	0x1BA: "MS_CR_MATCHPATCH2",
	0x1BC: "MS_CR_ADDR",
	0x1BD: "MS_CR_DATA",

	0x1CE: "CR_ALTDR6",
	0x1CF: "CR_SMM_status",#?

	0x1D9: "CR_DEBUGCTLMSR",
	0x1DA: "CR_DEBUGSTATUSMSR",
	0x1DB: "CR_LASTBRANCHFROMEIP",
	0x1DC: "CR_LASTBRANCHTOEIP",
	0x1DD: "CR_LASTINTFROMEIP",
	0x1DE: "CR_LASTINTTOEIP",
	0x1DF: "CR_ICECTLPMR",

	0x1E0: "ROB_CR_BKUPTMPDR6",

	0x18C: "CR_STEPPING",#?

}
creg_map_inv = {v: k for k, v in creg_map.items()}

segs = {
    0x00: "SEG_SINK",
    0x01: "LINSEG",
    0x02: "SEG_02",
    0x03: "SEG_03",
    0x04: "SEG_04",
    0x05: "SEG_05",
    0x06: "GDTR",
    0x07: "LDTR",
    0x08: "ES",
    0x09: "CS",
    0x0A: "SS",
    0x0B: "DS",
    0x0C: "FS",
    0x0D: "GS",
    0x0E: "IDTR",
    0x0F: "TR",
}
seg_map_inv = {v: k for k, v in segs.items()}

flowm_map_inv = {
	"SGLUOP": 0x003,
	"BOM"   : 0x001,
	"EOM"   : 0x002,
	"Fl2"   : 0x004,
	"Fl3"   : 0x008,
	"": 0
}

def is_ubranch(op):
	return (op&0xfbf) == 0x210 or (op & 0xfb0) == 0x310 or op == 0x90 or op == 0x010

def is_subranch(op):
	return (op&0xfbf) == 0x210 or op == 0x090 or op == 0x010
