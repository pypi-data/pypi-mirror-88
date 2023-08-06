fcadd z1.d, p0/m, z1.d, z2.d, #90

fcmla z26.d, p0/m, z29.d, z21.d, #90

fsub z1.d, z1.d, z2.d

incb x1, all, mul #13

ld1d z0.d, p0/z, [x11]
ldp x10, x1, [sp, 408]
ldr z1, [x28, #2, mul vl]
ldr z13, [x28]
ldrb w10, [x20, x10]
ldrb w7, [x2, 5]

mov z11.d, z20.d

movprfx z0, z31

prfd pldl1strm, p0, [x10]

smaddl x1, w1, w0, x19

str z12, [x30]
str z14, [x11, #2, mul vl]
sxtw x1, w1

tbl z9.d, z9.d, z7.d
