Collection of scripts used for hacking P6 (Pentium Pro,II,III) microcode.

# Disclaimer
Only public resources and publically available hardware were used by the author
to produce this program.

The code in these scripts was written as part of ongoing research and as such
is not very tidy, it is provided for study only and should not be relied on in
any way

# Scramble / Descramble
These scripts are used to convert between "physical" MSROM/RAM layout of
microcode and logical micro-op layout.

Micro-ops occur in triplets and as such every fourth address in the descrambled
form is unused.

The scrambled form represents the layout as it is found in patch files and in
the on-chip mask-ROM.

# SimpleDis / SimpleAs

These scripts are a simple disassembler and assembler for P6 microcode.
They are not yet released but will be added here soon.

