.L24:
	lsl	w3, w9, 3
	add	w1, w15, w9
	ldp	x7, x2, [sp, 160]
	ld1d	z21.d, p0/z, [x2]
	sxtw	x3, w3
	ld1d	z15.d, p0/z, [x7]
	lsl	w1, w1, 3
	add	x10, x3, 1
	ldp	x7, x2, [sp, 184]
	ld1d	z10.d, p0/z, [x7]
	sxtw	x1, w1
	ld1d	z19.d, p0/z, [x2]
	ldr	x5, [x22, x3, lsl 3]
	ld1d	z8.d, p0/z, [x6]
	add	x4, x1, 1
	ld1d	z20.d, p0/z, [x26]
	ldr	x7, [x22, x1, lsl 3]
	add	x8, x22, x10, lsl 3
	ldr	x1, [sp, 208]
	ld1d	z4.d, p0/z, [x1]
	smaddl	x1, w5, w0, x19
	ld1d	z17.d, p0/z, [x1]
	smaddl	x7, w7, w0, x19
	add	x12, x1, 192
	add	x11, x1, 384
	ld1d	z24.d, p0/z, [x12]
	ld1d	z9.d, p0/z, [x11]
	add	x12, x1, 256
	add	x11, x1, 448
	ld1d	z14.d, p0/z, [x12]
	ld1d	z3.d, p0/z, [x11]
	add	x12, x1, 320
	add	x11, x1, 512
	ld1d	z0.d, p0/z, [x12]
	ld1d	z1.d, p0/z, [x11]
	add	x12, x1, 576
	add	x11, x1, 64
	ldr	x2, [sp, 176]
	ld1d	z11.d, p0/z, [x12]
	ld1d	z2.d, p0/z, [x2]
	add	x12, x1, 640
	ld1d	z13.d, p0/z, [x11]
	add	x11, x1, 128
	add	x1, x1, 704
	ld1d	z23.d, p0/z, [x12]
	ldr	x2, [sp, 200]
	ld1d	z12.d, p0/z, [x11]
	sub	x12, x7, #768
	ld1d	z22.d, p0/z, [x1]
	prfd	pldl2strm, p0, [x12]
	sub	x1, x7, #512
	sub	x7, x7, #256
	prfd	pldl2strm, p0, [x1]
	prfd	pldl2strm, p0, [x7]
	ld1d	z16.d, p0/z, [x2]
	ldr	x2, [x22, x10, lsl 3]
	fcadd	z0.d, p0/m, z0.d, z1.d, #270
	fcadd	z14.d, p0/m, z14.d, z3.d, #270
	fcadd	z17.d, p0/m, z17.d, z11.d, #270
	fcadd	z13.d, p0/m, z13.d, z23.d, #270
	fcadd	z24.d, p0/m, z24.d, z9.d, #270
	fcadd	z12.d, p0/m, z12.d, z22.d, #270
	movprfx	z9, z31
	fcmla	z9.d, p0/m, z8.d, z24.d, #0
	smaddl	x2, w2, w0, x19
	fcmla	z9.d, p0/m, z8.d, z24.d, #90
	movprfx	z1, z31
	fcmla	z1.d, p0/m, z15.d, z24.d, #0
	fcmla	z9.d, p0/m, z21.d, z14.d, #0
	add	x11, x2, 256
	add	x12, x2, 512
	fcmla	z9.d, p0/m, z21.d, z14.d, #90
	fcmla	z1.d, p0/m, z15.d, z24.d, #90
	fcmla	z9.d, p0/m, z19.d, z0.d, #0
	fcmla	z1.d, p0/m, z10.d, z14.d, #0
	fcmla	z9.d, p0/m, z19.d, z0.d, #90
	fcmla	z1.d, p0/m, z10.d, z14.d, #90
	movprfx	z3, z31
	fcmla	z3.d, p0/m, z20.d, z24.d, #0
	fcmla	z1.d, p0/m, z4.d, z0.d, #0
	fcmla	z3.d, p0/m, z20.d, z24.d, #90
	fcmla	z1.d, p0/m, z4.d, z0.d, #90
	fcmla	z3.d, p0/m, z2.d, z14.d, #0
	prfd	pldl1strm, p0, [x11]
	fcmla	z3.d, p0/m, z2.d, z14.d, #90
	fcmla	z3.d, p0/m, z16.d, z0.d, #0
	fcmla	z3.d, p0/m, z16.d, z0.d, #90
	movprfx	z0, z31
	fcmla	z0.d, p0/m, z8.d, z17.d, #0
	fcmla	z0.d, p0/m, z8.d, z17.d, #90
	movprfx	z8, z31
	fcmla	z8.d, p0/m, z20.d, z17.d, #0
	fcmla	z8.d, p0/m, z20.d, z17.d, #90
	fcmla	z8.d, p0/m, z2.d, z13.d, #0
	fcmla	z8.d, p0/m, z2.d, z13.d, #90
	movprfx	z2, z31
	fcmla	z2.d, p0/m, z15.d, z17.d, #0
	fcmla	z2.d, p0/m, z15.d, z17.d, #90
	ld1d	z15.d, p0/z, [x11]
	fcmla	z2.d, p0/m, z10.d, z13.d, #0
	add	x11, x2, 448
	fcmla	z2.d, p0/m, z10.d, z13.d, #90
	fcmla	z2.d, p0/m, z4.d, z12.d, #0
	fcmla	z2.d, p0/m, z4.d, z12.d, #90
	ld1d	z4.d, p0/z, [x11]
	prfd	pldl1strm, p0, [x12]
	fsub	z15.d, z15.d, z4.d
	ld1d	z4.d, p0/z, [x12]
	add	x12, x2, 320
	fcmla	z0.d, p0/m, z21.d, z13.d, #0
	fcmla	z0.d, p0/m, z21.d, z13.d, #90
	ld1d	z13.d, p0/z, [x12]
	add	x12, x2, 64
	ldr	x7, [x22, x4, lsl 3]
	ld1d	z24.d, p0/z, [x12]
	add	x12, x2, 640
	fsub	z13.d, z13.d, z4.d
	ldr	x1, [x8, 8]
	ld1d	z4.d, p0/z, [x12]
	add	x12, x2, 128
	ld1d	z17.d, p0/z, [x12]
	ldrb	w10, [x20, x10]
	add	x12, x2, 704
	smaddl	x7, w7, w0, x19
	fadd	z24.d, z24.d, z4.d
	smaddl	x1, w1, w0, x19
	ld1d	z4.d, p0/z, [x12]
	add	x12, x2, 192
	fcmla	z0.d, p0/m, z19.d, z12.d, #0
	ld1d	z21.d, p0/z, [x2]
	fcmla	z0.d, p0/m, z19.d, z12.d, #90
	prfd	pldl1strm, p0, [x2]
	ld1d	z19.d, p0/z, [x12]
	add	x12, x2, 384
	add	x2, x2, 576
	fcmla	z8.d, p0/m, z16.d, z12.d, #0
	add	x11, x1, 256
	fcmla	z8.d, p0/m, z16.d, z12.d, #90
	add	x13, x1, 512
	fadd	z17.d, z17.d, z4.d
	ld1d	z10.d, p0/z, [x12]
	ld1d	z4.d, p0/z, [x2]
	lsl	x4, x4, 3
	sub	x30, x7, #768
	add	x2, x3, 2
	movprfx	z18, z31
	fcadd	z18.d, p0/m, z18.d, z9.d, #90
	movprfx	z11, z31
	fcadd	z11.d, p0/m, z11.d, z1.d, #90
	movprfx	z14, z31
	fcadd	z14.d, p0/m, z14.d, z3.d, #90
	movprfx	z25, z31
	fcadd	z25.d, p0/m, z25.d, z0.d, #90
	movprfx	z23, z31
	fcadd	z23.d, p0/m, z23.d, z8.d, #90
	movprfx	z16, z31
	fcadd	z16.d, p0/m, z16.d, z2.d, #90
	fsub	z19.d, z19.d, z10.d
	fadd	z21.d, z21.d, z4.d
	prfd	pldl1strm, p0, [x1]
	prfd	pldl1strm, p0, [x11]
	prfd	pldl1strm, p0, [x13]
	cbz	w10, .L17
	tbl	z21.d, z21.d, z5.d
	tbl	z24.d, z24.d, z5.d
	tbl	z17.d, z17.d, z5.d
	tbl	z19.d, z19.d, z5.d
	tbl	z15.d, z15.d, z5.d
	tbl	z13.d, z13.d, z5.d
.L17:
	ldr	x12, [sp, 256]
	ld1d	z12.d, p0/z, [x12]
	add	x4, x22, x4
	prfd	pldl2strm, p0, [x30]
	ldr	x12, [sp, 216]
	add	x30, x1, 448
	ldr	x10, [sp, 616]
	ld1d	z10.d, p0/z, [x10]
	movprfx	z22, z31
	fcmla	z22.d, p0/m, z10.d, z21.d, #0
	movprfx	z4, z31
	fcmla	z4.d, p0/m, z10.d, z19.d, #0
	fcmla	z22.d, p0/m, z10.d, z21.d, #90
	fcmla	z4.d, p0/m, z10.d, z19.d, #90
	ldr	x10, [sp, 232]
	ld1d	z20.d, p0/z, [x10]
	fcmla	z22.d, p0/m, z20.d, z24.d, #0
	fcmla	z22.d, p0/m, z20.d, z24.d, #90
	fcmla	z22.d, p0/m, z12.d, z17.d, #0
	fcmla	z22.d, p0/m, z12.d, z17.d, #90
	fadd	z10.d, z0.d, z22.d
	fadd	z22.d, z25.d, z22.d
	ld1d	z25.d, p0/z, [x12]
	ldr	x12, [sp, 240]
	fcmla	z4.d, p0/m, z20.d, z15.d, #0
	fcmla	z4.d, p0/m, z20.d, z15.d, #90
	fcmla	z4.d, p0/m, z12.d, z13.d, #0
	fcmla	z4.d, p0/m, z12.d, z13.d, #90
	ld1d	z12.d, p0/z, [x12]
	ldr	x12, [sp, 264]
	ld1d	z0.d, p0/z, [x12]
	movprfx	z20, z31
	fcmla	z20.d, p0/m, z25.d, z21.d, #0
	ldr	x12, [sp, 224]
	fcmla	z20.d, p0/m, z25.d, z21.d, #90
	fcmla	z20.d, p0/m, z12.d, z24.d, #0
	fcmla	z20.d, p0/m, z12.d, z24.d, #90
	ldrb	w28, [x20, x2]
	fcmla	z20.d, p0/m, z0.d, z17.d, #0
	fcmla	z20.d, p0/m, z0.d, z17.d, #90
	fadd	z8.d, z8.d, z20.d
	fadd	z20.d, z23.d, z20.d
	ld1d	z23.d, p0/z, [x12]
	ldr	x2, [x8, 16]
	fadd	z9.d, z9.d, z4.d
	fsub	z4.d, z18.d, z4.d
	movprfx	z18, z31
	fcmla	z18.d, p0/m, z25.d, z19.d, #0
	ldr	x12, [sp, 248]
	fcmla	z18.d, p0/m, z25.d, z19.d, #90
	fcmla	z18.d, p0/m, z12.d, z15.d, #0
	fcmla	z18.d, p0/m, z12.d, z15.d, #90
	movprfx	z12, z31
	fcmla	z12.d, p0/m, z23.d, z21.d, #0
	fcmla	z18.d, p0/m, z0.d, z13.d, #0
	fcmla	z12.d, p0/m, z23.d, z21.d, #90
	fcmla	z18.d, p0/m, z0.d, z13.d, #90
	ld1d	z21.d, p0/z, [x12]
	ldr	x12, [sp, 272]
	ld1d	z0.d, p0/z, [x12]
	fadd	z3.d, z3.d, z18.d
	fcmla	z12.d, p0/m, z21.d, z24.d, #0
	fsub	z18.d, z14.d, z18.d
	fcmla	z12.d, p0/m, z21.d, z24.d, #90
	movprfx	z14, z31
	fcmla	z14.d, p0/m, z23.d, z19.d, #0
	fcmla	z12.d, p0/m, z0.d, z17.d, #0
	fcmla	z14.d, p0/m, z23.d, z19.d, #90
	fcmla	z12.d, p0/m, z0.d, z17.d, #90
	fcmla	z14.d, p0/m, z21.d, z15.d, #0
	fcmla	z14.d, p0/m, z21.d, z15.d, #90
	fcmla	z14.d, p0/m, z0.d, z13.d, #0
	fcmla	z14.d, p0/m, z0.d, z13.d, #90
	ld1d	z0.d, p0/z, [x13]
	sub	x13, x7, #512
	sub	x7, x7, #256
	ldr	x10, [x4, 8]
	prfd	pldl2strm, p0, [x7]
	add	x7, x1, 64
	ld1d	z17.d, p0/z, [x7]
	smaddl	x2, w2, w0, x19
	add	x7, x1, 128
	ld1d	z15.d, p0/z, [x7]
	add	x7, x1, 576
	prfd	pldl2strm, p0, [x13]
	smaddl	x10, w10, w0, x19
	add	x12, x2, 256
	add	x13, x2, 512
	prfd	pldl1strm, p0, [x2]
	fadd	z2.d, z2.d, z12.d
	fadd	z1.d, z1.d, z14.d
	fadd	z12.d, z16.d, z12.d
	fsub	z14.d, z11.d, z14.d
	prfd	pldl1strm, p0, [x12]
	ld1d	z11.d, p0/z, [x30]
	prfd	pldl1strm, p0, [x13]
	add	x30, x1, 192
	fcadd	z15.d, p0/m, z15.d, z0.d, #270
	ld1d	z16.d, p0/z, [x30]
	ld1d	z0.d, p0/z, [x7]
	add	x7, x1, 320
	add	x30, x1, 704
	fcadd	z17.d, p0/m, z17.d, z11.d, #270
	ld1d	z13.d, p0/z, [x30]
	ld1d	z11.d, p0/z, [x7]
	fcadd	z16.d, p0/m, z16.d, z0.d, #90
	add	x7, x1, 640
	ld1d	z0.d, p0/z, [x7]
	ld1d	z19.d, p0/z, [x1]
	add	x7, x1, 384
	fcadd	z11.d, p0/m, z11.d, z13.d, #90
	sub	x27, x10, #768
	ld1d	z13.d, p0/z, [x11]
	add	x1, x3, 3
	fcadd	z13.d, p0/m, z13.d, z0.d, #90
	ld1d	z0.d, p0/z, [x7]
	fcadd	z19.d, p0/m, z19.d, z0.d, #270
	cbz	w28, .L18
	tbl	z19.d, z19.d, z6.d
	tbl	z17.d, z17.d, z6.d
	tbl	z15.d, z15.d, z6.d
	tbl	z16.d, z16.d, z6.d
	tbl	z13.d, z13.d, z6.d
	tbl	z11.d, z11.d, z6.d
.L18:
	ldr	x11, [sp, 656]
	ld1d	z25.d, p0/z, [x11]
	prfd	pldl2strm, p0, [x27]
	movprfx	z0, z31
	fcmla	z0.d, p0/m, z25.d, z19.d, #0
	ldr	x11, [sp, 296]
	ld1d	z23.d, p0/z, [x11]
	sub	x27, x10, #512
	fcmla	z0.d, p0/m, z25.d, z19.d, #90
	ldr	x11, [x8, 24]
	fcmla	z0.d, p0/m, z23.d, z17.d, #0
	sub	x10, x10, #256
	fcmla	z0.d, p0/m, z23.d, z17.d, #90
	ldr	x28, [sp, 320]
	ld1d	z24.d, p0/z, [x28]
	movprfx	z21, z31
	fcmla	z21.d, p0/m, z25.d, z16.d, #0
	fcmla	z21.d, p0/m, z25.d, z16.d, #90
	ldrb	w28, [x20, x1]
	smaddl	x1, w11, w0, x19
	ldr	x11, [sp, 280]
	fcmla	z21.d, p0/m, z23.d, z13.d, #0
	fcmla	z21.d, p0/m, z23.d, z13.d, #90
	ld1d	z23.d, p0/z, [x11]
	add	x11, sp, 720
	prfd	pldl2strm, p0, [x27]
	prfd	pldl2strm, p0, [x10]
	prfd	pldl1strm, p0, [x1]
	add	x10, x1, 512
	fcmla	z21.d, p0/m, z24.d, z11.d, #0
	prfd	pldl1strm, p0, [x10]
	fcmla	z21.d, p0/m, z24.d, z11.d, #90
	fcadd	z22.d, p0/m, z22.d, z21.d, #270
	fadd	z9.d, z9.d, z21.d
	str	z22, [x11, #4, mul vl]
	str	z9, [x11, #5, mul vl]
	ldr	x11, [sp, 304]
	ld1d	z22.d, p0/z, [x11]
	fcmla	z0.d, p0/m, z24.d, z15.d, #0
	fcmla	z0.d, p0/m, z24.d, z15.d, #90
	ldr	x11, [sp, 328]
	ld1d	z21.d, p0/z, [x11]
	add	x11, sp, 720
	fcadd	z4.d, p0/m, z4.d, z0.d, #90
	fadd	z0.d, z10.d, z0.d
	movprfx	z10, z31
	fcmla	z10.d, p0/m, z23.d, z19.d, #0
	fcmla	z10.d, p0/m, z23.d, z19.d, #90
	fcmla	z10.d, p0/m, z22.d, z17.d, #0
	fcmla	z10.d, p0/m, z22.d, z17.d, #90
	fcmla	z10.d, p0/m, z21.d, z15.d, #0
	fcmla	z10.d, p0/m, z21.d, z15.d, #90
	fcadd	z18.d, p0/m, z18.d, z10.d, #90
	fadd	z8.d, z8.d, z10.d
	str	z8, [x11, #1, mul vl]
	str	z18, [x11]
	ldr	x11, [sp, 288]
	ld1d	z18.d, p0/z, [x11]
	add	x11, sp, 720
	add	x30, sp, 720
	movprfx	z9, z31
	fcmla	z9.d, p0/m, z23.d, z16.d, #0
	fcmla	z9.d, p0/m, z23.d, z16.d, #90
	fcmla	z9.d, p0/m, z22.d, z13.d, #0
	fcmla	z9.d, p0/m, z22.d, z13.d, #90
	fcmla	z9.d, p0/m, z21.d, z11.d, #0
	fcmla	z9.d, p0/m, z21.d, z11.d, #90
	fadd	z3.d, z3.d, z9.d
	fcadd	z20.d, p0/m, z20.d, z9.d, #270
	str	z3, [x11, #7, mul vl]
	str	z20, [x11, #6, mul vl]
	ldr	x11, [sp, 312]
	incb	x30, all, mul #8
	ld1d	z10.d, p0/z, [x11]
	movprfx	z8, z31
	fcmla	z8.d, p0/m, z18.d, z19.d, #0
	fcmla	z8.d, p0/m, z18.d, z19.d, #90
	fcmla	z8.d, p0/m, z10.d, z17.d, #0
	fcmla	z8.d, p0/m, z10.d, z17.d, #90
	ldr	x11, [sp, 336]
	ld1d	z9.d, p0/z, [x11]
	fcmla	z8.d, p0/m, z9.d, z15.d, #0
	fcmla	z8.d, p0/m, z9.d, z15.d, #90
	fadd	z2.d, z2.d, z8.d
	add	x11, sp, 720
	fcadd	z14.d, p0/m, z14.d, z8.d, #90
	movprfx	z3, z31
	fcmla	z3.d, p0/m, z18.d, z16.d, #0
	fcmla	z3.d, p0/m, z18.d, z16.d, #90
	fcmla	z3.d, p0/m, z10.d, z13.d, #0
	fcmla	z3.d, p0/m, z10.d, z13.d, #90
	ldr	x7, [x4, 16]
	str	z14, [x11, #2, mul vl]
	str	z2, [x11, #3, mul vl]
	movprfx	z2, z3
	fcmla	z2.d, p0/m, z9.d, z11.d, #0
	fcmla	z2.d, p0/m, z9.d, z11.d, #90
	fcadd	z12.d, p0/m, z12.d, z2.d, #270
	str	z12, [x30]
	add	x30, sp, 720
	fadd	z1.d, z1.d, z2.d
	incb	x30, all, mul #9
	str	z1, [x30]
	add	x30, x2, 64
	ld1d	z2.d, p0/z, [x13]
	ld1d	z3.d, p0/z, [x30]
	add	x13, x2, 128
	add	x30, x2, 448
	ld1d	z1.d, p0/z, [x13]
	ld1d	z8.d, p0/z, [x30]
	add	x13, x2, 576
	add	x30, x2, 192
	fsub	z30.d, z3.d, z8.d
	ld1d	z3.d, p0/z, [x13]
	smaddl	x7, w7, w0, x19
	add	x13, x2, 320
	fsub	z1.d, z1.d, z2.d
	ld1d	z2.d, p0/z, [x30]
	add	x30, x2, 704
	fsub	z10.d, z2.d, z3.d
	ld1d	z3.d, p0/z, [x30]
	ld1d	z2.d, p0/z, [x13]
	add	x13, x2, 640
	fsub	z2.d, z2.d, z3.d
	ld1d	z8.d, p0/z, [x13]
	ld1d	z3.d, p0/z, [x12]
	add	x11, x1, 256
	fsub	z9.d, z3.d, z8.d
	add	x12, x2, 384
	ld1d	z3.d, p0/z, [x2]
	ld1d	z8.d, p0/z, [x12]
	sub	x27, x7, #768
	prfd	pldl1strm, p0, [x11]
	fsub	z26.d, z3.d, z8.d
	cbz	w28, .L19
	tbl	z26.d, z26.d, z7.d
	tbl	z30.d, z30.d, z7.d
	tbl	z1.d, z1.d, z7.d
	tbl	z10.d, z10.d, z7.d
	tbl	z9.d, z9.d, z7.d
	tbl	z2.d, z2.d, z7.d
.L19:
	add	x2, x20, x3
	sub	x12, x7, #512
	sub	x7, x7, #256
	prfd	pldl2strm, p0, [x7]
	ldr	x13, [x8, 32]
	prfd	pldl2strm, p0, [x12]
	prfd	pldl2strm, p0, [x27]
	ld1d	z23.d, p0/z, [x11]
	ldrb	w7, [x2, 5]
	ld1d	z22.d, p0/z, [x10]
	ldr	x2, [sp, 640]
	ld1d	z18.d, p0/z, [x2]
	smaddl	x12, w13, w0, x19
	prfd	pldl1strm, p0, [x12]
	ldr	x2, [sp, 648]
	ld1d	z19.d, p0/z, [x2]
	add	x13, x12, 256
	prfd	pldl1strm, p0, [x13]
	ldr	x2, [sp, 344]
	ld1d	z15.d, p0/z, [x2]
	add	x11, x12, 512
	prfd	pldl1strm, p0, [x11]
	ldr	x2, [sp, 352]
	ld1d	z11.d, p0/z, [x2]
	ldr	x2, [sp, 360]
	ld1d	z17.d, p0/z, [x2]
	ldr	x2, [sp, 368]
	ld1d	z14.d, p0/z, [x2]
	ldr	x2, [sp, 376]
	ld1d	z3.d, p0/z, [x2]
	add	x2, sp, 720
	incb	x2, all, mul #11
	str	z3, [x2]
	ldr	x2, [sp, 384]
	ld1d	z16.d, p0/z, [x2]
	ldr	x2, [sp, 392]
	ld1d	z12.d, p0/z, [x2]
	ldr	x2, [sp, 400]
	ld1d	z8.d, p0/z, [x2]
	add	x2, sp, 720
	incb	x2, all, mul #12
	str	z8, [x2]
	add	x2, x1, 64
	ld1d	z20.d, p0/z, [x1]
	ld1d	z29.d, p0/z, [x2]
	add	x2, x1, 640
	ld1d	z21.d, p0/z, [x2]
	add	x2, x1, 128
	ld1d	z27.d, p0/z, [x2]
	add	x2, x1, 704
	ld1d	z28.d, p0/z, [x2]
	add	x2, x1, 192
	ld1d	z25.d, p0/z, [x2]
	add	x2, x1, 384
	ld1d	z24.d, p0/z, [x2]
	add	x2, sp, 720
	incb	x2, all, mul #10
	str	z24, [x2]
	add	x2, x1, 320
	ld1d	z3.d, p0/z, [x2]
	add	x2, x1, 448
	add	x1, x1, 576
	ld1d	z8.d, p0/z, [x1]
	add	x1, sp, 720
	incb	x1, all, mul #13
	ld1d	z24.d, p0/z, [x2]
	str	z8, [x1]
	ldr	x2, [x4, 24]
	fcadd	z29.d, p0/m, z29.d, z21.d, #90
	fcadd	z3.d, p0/m, z3.d, z22.d, #90
	ldp	x10, x1, [sp, 408]
	ld1d	z8.d, p0/z, [x1]
	fcadd	z27.d, p0/m, z27.d, z28.d, #90
	ld1d	z13.d, p0/z, [x10]
	ldr	x28, [x8, 40]
	add	x1, sp, 720
	ldr	z21, [x1, #10, mul vl]
	smaddl	x1, w2, w0, x19
	add	x2, sp, 720
	fcadd	z25.d, p0/m, z25.d, z21.d, #90
	ldr	z21, [x2, #13, mul vl]
	sub	x27, x1, #768
	smaddl	x2, w28, w0, x19
	prfd	pldl2strm, p0, [x27]
	add	x28, sp, 720
	sub	x27, x1, #512
	sub	x1, x1, #256
	fcadd	z20.d, p0/m, z20.d, z21.d, #90
	prfd	pldl2strm, p0, [x1]
	incb	x28, all, mul #10
	mov	z28.d, z25.d
	ldr	x1, [sp, 424]
	movprfx	z25, z23
	fcadd	z25.d, p0/m, z25.d, z24.d, #90
	ld1d	z22.d, p0/z, [x1]
	mov	z24.d, z20.d
	prfd	pldl2strm, p0, [x27]
	movprfx	z23, z31
	fcmla	z23.d, p0/m, z18.d, z28.d, #0
	movprfx	z20, z31
	fcmla	z20.d, p0/m, z19.d, z26.d, #0
	fcmla	z23.d, p0/m, z18.d, z28.d, #90
	fcmla	z20.d, p0/m, z19.d, z26.d, #90
	prfd	pldl1strm, p0, [x2]
	fcmla	z20.d, p0/m, z17.d, z30.d, #0
	fcmla	z23.d, p0/m, z22.d, z25.d, #0
	fcmla	z20.d, p0/m, z17.d, z30.d, #90
	fcmla	z23.d, p0/m, z22.d, z25.d, #90
	fcmla	z20.d, p0/m, z16.d, z1.d, #0
	fcmla	z20.d, p0/m, z16.d, z1.d, #90
	fsub	z4.d, z4.d, z20.d
	ldr	x1, [sp, 448]
	ld1d	z21.d, p0/z, [x1]
	fcmla	z23.d, p0/m, z21.d, z3.d, #0
	fcmla	z23.d, p0/m, z21.d, z3.d, #90
	fcadd	z4.d, p0/m, z4.d, z23.d, #270
	str	z4, [x28]
	add	x28, sp, 720
	movprfx	z4, z31
	fcmla	z4.d, p0/m, z19.d, z10.d, #0
	fcmla	z4.d, p0/m, z19.d, z10.d, #90
	fcmla	z4.d, p0/m, z17.d, z9.d, #0
	fcmla	z4.d, p0/m, z17.d, z9.d, #90
	ldr	z17, [x28, #4, mul vl]
	fcmla	z4.d, p0/m, z16.d, z2.d, #0
	fcmla	z4.d, p0/m, z16.d, z2.d, #90
	ldr	z16, [x28, #5, mul vl]
	ldr	x10, [x4, 32]
	movprfx	z19, z31
	fcmla	z19.d, p0/m, z18.d, z24.d, #0
	fadd	z0.d, z0.d, z20.d
	fcmla	z19.d, p0/m, z18.d, z24.d, #90
	ldr	x28, [sp, 432]
	fcmla	z19.d, p0/m, z22.d, z29.d, #0
	ld1d	z20.d, p0/z, [x28]
	fcmla	z19.d, p0/m, z22.d, z29.d, #90
	fcmla	z19.d, p0/m, z21.d, z27.d, #0
	fcmla	z19.d, p0/m, z21.d, z27.d, #90
	ldr	x28, [sp, 456]
	fadd	z16.d, z16.d, z4.d
	fadd	z0.d, z0.d, z19.d
	fsub	z4.d, z17.d, z4.d
	fcadd	z4.d, p0/m, z4.d, z19.d, #270
	ld1d	z19.d, p0/z, [x28]
	add	x28, sp, 720
	movprfx	z17, z31
	fcmla	z17.d, p0/m, z13.d, z24.d, #0
	ldr	z21, [x28, #7, mul vl]
	fcmla	z17.d, p0/m, z13.d, z24.d, #90
	movprfx	z18, z31
	fcmla	z18.d, p0/m, z15.d, z26.d, #0
	fcmla	z17.d, p0/m, z20.d, z29.d, #0
	fcmla	z18.d, p0/m, z15.d, z26.d, #90
	fcmla	z17.d, p0/m, z20.d, z29.d, #90
	fcmla	z18.d, p0/m, z14.d, z30.d, #0
	fcmla	z17.d, p0/m, z19.d, z27.d, #0
	fcmla	z18.d, p0/m, z14.d, z30.d, #90
	fcmla	z17.d, p0/m, z19.d, z27.d, #90
	fcmla	z18.d, p0/m, z12.d, z1.d, #0
	fadd	z23.d, z16.d, z23.d
	fcmla	z18.d, p0/m, z12.d, z1.d, #90
	movprfx	z16, z31
	fcmla	z16.d, p0/m, z15.d, z10.d, #0
	fcmla	z16.d, p0/m, z15.d, z10.d, #90
	ldr	z15, [x28, #6, mul vl]
	fcmla	z16.d, p0/m, z14.d, z9.d, #0
	fcmla	z16.d, p0/m, z14.d, z9.d, #90
	movprfx	z14, z31
	fcmla	z14.d, p0/m, z13.d, z28.d, #0
	fcmla	z16.d, p0/m, z12.d, z2.d, #0
	fcmla	z14.d, p0/m, z13.d, z28.d, #90
	fcmla	z16.d, p0/m, z12.d, z2.d, #90
	ldr	z12, [x28, #1, mul vl]
	ldr	z13, [x28]
	ldr	x28, [sp, 440]
	fsub	z15.d, z15.d, z16.d
	fadd	z12.d, z12.d, z18.d
	fadd	z16.d, z21.d, z16.d
	fcadd	z15.d, p0/m, z15.d, z17.d, #270
	fadd	z12.d, z12.d, z17.d
	ld1d	z17.d, p0/z, [x28]
	ldr	x28, [sp, 464]
	fcmla	z14.d, p0/m, z20.d, z25.d, #0
	fsub	z18.d, z13.d, z18.d
	fcmla	z14.d, p0/m, z20.d, z25.d, #90
	movprfx	z20, z31
	fcmla	z20.d, p0/m, z11.d, z26.d, #0
	fcmla	z14.d, p0/m, z19.d, z3.d, #0
	fcmla	z20.d, p0/m, z11.d, z26.d, #90
	fcmla	z14.d, p0/m, z19.d, z3.d, #90
	movprfx	z19, z31
	fcmla	z19.d, p0/m, z11.d, z10.d, #0
	fcadd	z18.d, p0/m, z18.d, z14.d, #270
	fcmla	z19.d, p0/m, z11.d, z10.d, #90
	fadd	z14.d, z16.d, z14.d
	mov	z11.d, z20.d
	ld1d	z16.d, p0/z, [x28]
	add	x28, sp, 720
	ldr	z10, [x28, #11, mul vl]
	fcmla	z19.d, p0/m, z10.d, z9.d, #0
	fcmla	z11.d, p0/m, z10.d, z30.d, #0
	fcmla	z19.d, p0/m, z10.d, z9.d, #90
	fcmla	z11.d, p0/m, z10.d, z30.d, #90
	ldr	z9, [x28, #12, mul vl]
	fcmla	z19.d, p0/m, z9.d, z2.d, #0
	fcmla	z11.d, p0/m, z9.d, z1.d, #0
	fcmla	z19.d, p0/m, z9.d, z2.d, #90
	fcmla	z11.d, p0/m, z9.d, z1.d, #90
	ldr	z2, [x28, #8, mul vl]
	ldr	z1, [x28, #3, mul vl]
	fsub	z10.d, z2.d, z19.d
	fadd	z22.d, z1.d, z11.d
	ldr	z2, [x28, #9, mul vl]
	ldr	z1, [x28, #2, mul vl]
	add	x27, x12, 448
	add	x1, x12, 320
	movprfx	z13, z31
	fcmla	z13.d, p0/m, z8.d, z24.d, #0
	fadd	z19.d, z2.d, z19.d
	fcmla	z13.d, p0/m, z8.d, z24.d, #90
	movprfx	z2, z31
	fcmla	z2.d, p0/m, z8.d, z28.d, #0
	fcmla	z2.d, p0/m, z8.d, z28.d, #90
	fsub	z8.d, z1.d, z11.d
	ld1d	z1.d, p0/z, [x27]
	ld1d	z21.d, p0/z, [x13]
	ld1d	z9.d, p0/z, [x1]
	fadd	z21.d, z21.d, z1.d
	add	x1, x12, 64
	ld1d	z1.d, p0/z, [x11]
	add	x11, x12, 640
	ld1d	z24.d, p0/z, [x1]
	smaddl	x10, w10, w0, x19
	add	x1, x12, 128
	fadd	z9.d, z9.d, z1.d
	ld1d	z1.d, p0/z, [x11]
	add	x11, x12, 704
	fcmla	z2.d, p0/m, z17.d, z25.d, #0
	fsub	z24.d, z24.d, z1.d
	fcmla	z2.d, p0/m, z17.d, z25.d, #90
	ld1d	z1.d, p0/z, [x11]
	fcmla	z2.d, p0/m, z16.d, z3.d, #0
	add	x11, x12, 384
	fcmla	z2.d, p0/m, z16.d, z3.d, #90
	movprfx	z11, z8
	fcadd	z11.d, p0/m, z11.d, z2.d, #270
	fadd	z2.d, z19.d, z2.d
	ld1d	z19.d, p0/z, [x1]
	add	x1, x12, 192
	ld1d	z3.d, p0/z, [x11]
	ld1d	z8.d, p0/z, [x12]
	add	x11, x2, 256
	fcmla	z13.d, p0/m, z17.d, z29.d, #0
	fsub	z19.d, z19.d, z1.d
	fcmla	z13.d, p0/m, z17.d, z29.d, #90
	sub	x13, x10, #768
	fcmla	z13.d, p0/m, z16.d, z27.d, #0
	add	x27, x3, 6
	fcmla	z13.d, p0/m, z16.d, z27.d, #90
	prfd	pldl1strm, p0, [x11]
	fcadd	z10.d, p0/m, z10.d, z13.d, #270
	fadd	z13.d, z22.d, z13.d
	ld1d	z22.d, p0/z, [x1]
	add	x1, x12, 576
	fadd	z22.d, z22.d, z3.d
	add	x12, x2, 512
	ld1d	z1.d, p0/z, [x1]
	prfd	pldl1strm, p0, [x12]
	fsub	z8.d, z8.d, z1.d
	cbz	w7, .L20
	tbl	z8.d, z8.d, z5.d
	tbl	z24.d, z24.d, z5.d
	tbl	z19.d, z19.d, z5.d
	tbl	z22.d, z22.d, z5.d
	tbl	z21.d, z21.d, z5.d
	tbl	z9.d, z9.d, z5.d
.L20:
	ldr	x1, [sp, 632]
	ld1d	z20.d, p0/z, [x1]
	movprfx	z3, z31
	fcmla	z3.d, p0/m, z20.d, z22.d, #0
	fcmla	z3.d, p0/m, z20.d, z22.d, #90
	ldr	x1, [x8, 48]
	movprfx	z1, z31
	fcmla	z1.d, p0/m, z20.d, z8.d, #0
	fcmla	z1.d, p0/m, z20.d, z8.d, #90
	add	x28, x2, 64
	ldr	x8, [sp, 488]
	ld1d	z17.d, p0/z, [x8]
	fcmla	z3.d, p0/m, z17.d, z21.d, #0
	fcmla	z3.d, p0/m, z17.d, z21.d, #90
	ldr	x8, [sp, 512]
	ld1d	z16.d, p0/z, [x8]
	fcmla	z1.d, p0/m, z17.d, z24.d, #0
	fcmla	z1.d, p0/m, z17.d, z24.d, #90
	ldr	x8, [sp, 472]
	ld1d	z25.d, p0/z, [x8]
	add	x8, sp, 720
	fcmla	z1.d, p0/m, z16.d, z19.d, #0
	fcmla	z1.d, p0/m, z16.d, z19.d, #90
	fadd	z20.d, z0.d, z1.d
	fsub	z1.d, z4.d, z1.d
	movprfx	z4, z3
	fcmla	z4.d, p0/m, z16.d, z9.d, #0
	ldr	z3, [x8, #10, mul vl]
	ldr	x8, [sp, 496]
	ld1d	z17.d, p0/z, [x8]
	movprfx	z0, z31
	fcmla	z0.d, p0/m, z25.d, z8.d, #0
	ldr	x8, [sp, 520]
	fcmla	z4.d, p0/m, z16.d, z9.d, #90
	fadd	z16.d, z23.d, z4.d
	movprfx	z23, z0
	fcmla	z23.d, p0/m, z25.d, z8.d, #90
	fadd	z4.d, z3.d, z4.d
	fcmla	z23.d, p0/m, z17.d, z24.d, #0
	ld1d	z3.d, p0/z, [x8]
	fcmla	z23.d, p0/m, z17.d, z24.d, #90
	fcmla	z23.d, p0/m, z3.d, z19.d, #0
	fcmla	z23.d, p0/m, z3.d, z19.d, #90
	ldr	x8, [sp, 480]
	movprfx	z0, z31
	fcmla	z0.d, p0/m, z25.d, z22.d, #0
	fsub	z15.d, z15.d, z23.d
	fcmla	z0.d, p0/m, z25.d, z22.d, #90
	fcmla	z0.d, p0/m, z17.d, z21.d, #0
	fcmla	z0.d, p0/m, z17.d, z21.d, #90
	fadd	z17.d, z12.d, z23.d
	fcmla	z0.d, p0/m, z3.d, z9.d, #0
	ld1d	z23.d, p0/z, [x8]
	fcmla	z0.d, p0/m, z3.d, z9.d, #90
	ldr	x7, [x4, 40]
	fadd	z14.d, z14.d, z0.d
	fadd	z18.d, z18.d, z0.d
	smaddl	x1, w1, w0, x19
	ldr	x8, [sp, 504]
	ld1d	z12.d, p0/z, [x8]
	movprfx	z3, z31
	fcmla	z3.d, p0/m, z23.d, z8.d, #0
	fcmla	z3.d, p0/m, z23.d, z8.d, #90
	ldr	x8, [sp, 528]
	ld1d	z0.d, p0/z, [x8]
	movprfx	z8, z31
	fcmla	z8.d, p0/m, z23.d, z22.d, #0
	fcmla	z3.d, p0/m, z12.d, z24.d, #0
	fcmla	z8.d, p0/m, z23.d, z22.d, #90
	fcmla	z3.d, p0/m, z12.d, z24.d, #90
	fcmla	z8.d, p0/m, z12.d, z21.d, #0
	fcmla	z3.d, p0/m, z0.d, z19.d, #0
	fcmla	z8.d, p0/m, z12.d, z21.d, #90
	fcmla	z3.d, p0/m, z0.d, z19.d, #90
	fcmla	z8.d, p0/m, z0.d, z9.d, #0
	ldrb	w27, [x20, x27]
	fcmla	z8.d, p0/m, z0.d, z9.d, #90
	ld1d	z0.d, p0/z, [x12]
	add	x12, x2, 128
	ld1d	z25.d, p0/z, [x28]
	ld1d	z24.d, p0/z, [x12]
	add	x28, x2, 448
	add	x12, x2, 576
	prfd	pldl2strm, p0, [x13]
	sub	x13, x10, #512
	sub	x10, x10, #256
	prfd	pldl2strm, p0, [x13]
	prfd	pldl2strm, p0, [x10]
	fadd	z9.d, z2.d, z8.d
	smaddl	x7, w7, w0, x19
	ld1d	z2.d, p0/z, [x28]
	add	x10, x1, 512
	add	x28, x2, 192
	add	x8, x1, 256
	prfd	pldl1strm, p0, [x1]
	prfd	pldl1strm, p0, [x10]
	fadd	z22.d, z13.d, z3.d
	prfd	pldl1strm, p0, [x8]
	fsub	z3.d, z10.d, z3.d
	fcadd	z24.d, p0/m, z24.d, z0.d, #90
	ld1d	z10.d, p0/z, [x28]
	ld1d	z0.d, p0/z, [x12]
	add	x12, x2, 320
	fadd	z8.d, z11.d, z8.d
	fcadd	z10.d, p0/m, z10.d, z0.d, #270
	ld1d	z11.d, p0/z, [x12]
	add	x12, x2, 640
	ld1d	z0.d, p0/z, [x12]
	ld1d	z21.d, p0/z, [x11]
	add	x28, x2, 704
	add	x11, x2, 384
	fcadd	z25.d, p0/m, z25.d, z2.d, #90
	fcadd	z21.d, p0/m, z21.d, z0.d, #270
	ld1d	z2.d, p0/z, [x28]
	ld1d	z0.d, p0/z, [x11]
	ld1d	z26.d, p0/z, [x2]
	add	x3, x3, 7
	sub	x13, x7, #768
	fcadd	z11.d, p0/m, z11.d, z2.d, #270
	fcadd	z26.d, p0/m, z26.d, z0.d, #90
	cbz	w27, .L21
	tbl	z26.d, z26.d, z6.d
	tbl	z25.d, z25.d, z6.d
	tbl	z24.d, z24.d, z6.d
	tbl	z10.d, z10.d, z6.d
	tbl	z21.d, z21.d, z6.d
	tbl	z11.d, z11.d, z6.d
.L21:
	ldr	x2, [x4, 48]
	prfd	pldl2strm, p0, [x13]
	smaddl	x5, w5, w0, x19
	prfd	pldl1strm, p0, [x5]
	ldr	x4, [sp, 624]
	ld1d	z13.d, p0/z, [x4]
	movprfx	z23, z31
	fcmla	z23.d, p0/m, z13.d, z10.d, #0
	fcmla	z23.d, p0/m, z13.d, z10.d, #90
	ldrb	w4, [x20, x3]
	movprfx	z0, z31
	fcmla	z0.d, p0/m, z13.d, z26.d, #0
	ldr	x3, [sp, 552]
	ld1d	z2.d, p0/z, [x3]
	fcmla	z23.d, p0/m, z2.d, z21.d, #0
	fcmla	z23.d, p0/m, z2.d, z21.d, #90
	ldr	x3, [sp, 576]
	ld1d	z12.d, p0/z, [x3]
	fcmla	z23.d, p0/m, z12.d, z11.d, #0
	fcmla	z0.d, p0/m, z13.d, z26.d, #90
	ldr	x3, [sp, 536]
	ld1d	z19.d, p0/z, [x3]
	fcmla	z0.d, p0/m, z2.d, z25.d, #0
	fcmla	z0.d, p0/m, z2.d, z25.d, #90
	ldr	x3, [sp, 560]
	movprfx	z2, z23
	fcmla	z2.d, p0/m, z12.d, z11.d, #90
	fadd	z23.d, z16.d, z2.d
	ld1d	z16.d, p0/z, [x3]
	ldr	x3, [sp, 584]
	ld1d	z13.d, p0/z, [x3]
	fcmla	z0.d, p0/m, z12.d, z24.d, #0
	add	x11, x5, 256
	ldr	x3, [sp, 544]
	fcmla	z0.d, p0/m, z12.d, z24.d, #90
	add	x5, x5, 512
	movprfx	z12, z31
	fcmla	z12.d, p0/m, z19.d, z26.d, #0
	fcadd	z1.d, p0/m, z1.d, z2.d, #90
	fcmla	z12.d, p0/m, z19.d, z26.d, #90
	movprfx	z2, z31
	fcmla	z2.d, p0/m, z19.d, z10.d, #0
	fcmla	z2.d, p0/m, z19.d, z10.d, #90
	ld1d	z19.d, p0/z, [x3]
	ldr	x3, [sp, 568]
	fcmla	z2.d, p0/m, z16.d, z21.d, #0
	prfd	pldl1strm, p0, [x5]
	fcmla	z2.d, p0/m, z16.d, z21.d, #90
	add	x5, x1, 64
	fcmla	z2.d, p0/m, z13.d, z11.d, #0
	fcmla	z12.d, p0/m, z16.d, z25.d, #0
	fcmla	z2.d, p0/m, z13.d, z11.d, #90
	fcmla	z12.d, p0/m, z16.d, z25.d, #90
	fcmla	z12.d, p0/m, z13.d, z24.d, #0
	fcmla	z12.d, p0/m, z13.d, z24.d, #90
	movprfx	z13, z31
	fcmla	z13.d, p0/m, z19.d, z26.d, #0
	fcadd	z18.d, p0/m, z18.d, z12.d, #270
	fcmla	z13.d, p0/m, z19.d, z26.d, #90
	fadd	z12.d, z17.d, z12.d
	ld1d	z17.d, p0/z, [x3]
	fcmla	z13.d, p0/m, z17.d, z25.d, #0
	fcmla	z13.d, p0/m, z17.d, z25.d, #90
	ldr	x3, [sp, 592]
	ld1d	z16.d, p0/z, [x3]
	fcmla	z13.d, p0/m, z16.d, z24.d, #0
	fcadd	z15.d, p0/m, z15.d, z2.d, #90
	fadd	z14.d, z14.d, z2.d
	movprfx	z2, z31
	fcmla	z2.d, p0/m, z19.d, z10.d, #0
	fcmla	z2.d, p0/m, z19.d, z10.d, #90
	movprfx	z10, z13
	fcmla	z10.d, p0/m, z16.d, z24.d, #90
	fcmla	z2.d, p0/m, z17.d, z21.d, #0
	fadd	z13.d, z22.d, z10.d
	fcmla	z2.d, p0/m, z17.d, z21.d, #90
	ld1d	z22.d, p0/z, [x5]
	fcmla	z2.d, p0/m, z16.d, z11.d, #0
	add	x5, x1, 128
	fcmla	z2.d, p0/m, z16.d, z11.d, #90
	fcadd	z3.d, p0/m, z3.d, z2.d, #90
	fadd	z2.d, z9.d, z2.d
	ld1d	z9.d, p0/z, [x10]
	sub	x10, x7, #512
	sub	x7, x7, #256
	ld1d	z21.d, p0/z, [x5]
	prfd	pldl2strm, p0, [x7]
	add	x5, x1, 576
	add	x7, x1, 448
	smaddl	x2, w2, w0, x19
	fcadd	z8.d, p0/m, z8.d, z10.d, #270
	fadd	z21.d, z21.d, z9.d
	ld1d	z10.d, p0/z, [x7]
	ld1d	z9.d, p0/z, [x5]
	add	x7, x1, 192
	add	x5, x1, 320
	ld1d	z11.d, p0/z, [x7]
	prfd	pldl1strm, p0, [x11]
	add	x7, x1, 704
	prfd	pldl2strm, p0, [x10]
	fadd	z22.d, z22.d, z10.d
	fadd	z11.d, z11.d, z9.d
	ld1d	z9.d, p0/z, [x5]
	add	x5, x1, 640
	ld1d	z10.d, p0/z, [x7]
	ld1d	z16.d, p0/z, [x5]
	fcadd	z4.d, p0/m, z4.d, z0.d, #270
	add	x5, x1, 384
	fadd	z9.d, z9.d, z10.d
	ld1d	z24.d, p0/z, [x1]
	ld1d	z10.d, p0/z, [x8]
	sub	x3, x2, #768
	fadd	z10.d, z10.d, z16.d
	fadd	z0.d, z20.d, z0.d
	ld1d	z16.d, p0/z, [x5]
	fadd	z24.d, z24.d, z16.d
	cbz	w4, .L22
	tbl	z24.d, z24.d, z7.d
	tbl	z22.d, z22.d, z7.d
	tbl	z21.d, z21.d, z7.d
	tbl	z11.d, z11.d, z7.d
	tbl	z10.d, z10.d, z7.d
	tbl	z9.d, z9.d, z7.d
.L22:
	ldr	x1, [sp, 664]
	ld1d	z20.d, p0/z, [x14]
	ld1d	z29.d, p0/z, [x18]
	ld1d	z28.d, p0/z, [x25]
	ldr	x4, [sp, 600]
	ld1d	z25.d, p0/z, [x24]
	ld1d	z30.d, p0/z, [x4]
	ld1d	z27.d, p0/z, [x23]
	smaddl	x1, w9, w0, x1
	ld1d	z19.d, p0/z, [x21]
	ld1d	z16.d, p0/z, [x17]
	prfd	pldl2strm, p0, [x3]
	movprfx	z26, z31
	fcmla	z26.d, p0/m, z20.d, z24.d, #0
	sub	x3, x2, #512
	fcmla	z26.d, p0/m, z20.d, z24.d, #90
	prfd	pldl2strm, p0, [x3]
	sub	x2, x2, #256
	fcmla	z26.d, p0/m, z30.d, z22.d, #0
	prfd	pldl2strm, p0, [x2]
	fcmla	z26.d, p0/m, z30.d, z22.d, #90
	fcmla	z26.d, p0/m, z29.d, z21.d, #0
	fcmla	z26.d, p0/m, z29.d, z21.d, #90
	fadd	z0.d, z0.d, z26.d
	ldr	x4, [sp, 608]
	ld1d	z17.d, p0/z, [x4]
	st1d	z0.d, p0, [x1]
	add	x2, x1, 64
	movprfx	z0, z31
	fcmla	z0.d, p0/m, z28.d, z24.d, #0
	fcmla	z0.d, p0/m, z28.d, z24.d, #90
	fcmla	z0.d, p0/m, z27.d, z22.d, #0
	fcmla	z0.d, p0/m, z27.d, z22.d, #90
	fcmla	z0.d, p0/m, z16.d, z21.d, #0
	fcmla	z0.d, p0/m, z16.d, z21.d, #90
	fadd	z12.d, z12.d, z0.d
	st1d	z12.d, p0, [x2]
	add	x2, x1, 128
	movprfx	z12, z31
	fcmla	z12.d, p0/m, z25.d, z24.d, #0
	fcmla	z12.d, p0/m, z25.d, z24.d, #90
	fcmla	z12.d, p0/m, z19.d, z22.d, #0
	fcmla	z12.d, p0/m, z19.d, z22.d, #90
	fcmla	z12.d, p0/m, z17.d, z21.d, #0
	fcmla	z12.d, p0/m, z17.d, z21.d, #90
	fadd	z13.d, z13.d, z12.d
	st1d	z13.d, p0, [x2]
	add	x2, x1, 192
	movprfx	z13, z31
	fcmla	z13.d, p0/m, z20.d, z11.d, #0
	fcmla	z13.d, p0/m, z20.d, z11.d, #90
	movprfx	z20, z13
	fcmla	z20.d, p0/m, z30.d, z10.d, #0
	fcmla	z20.d, p0/m, z30.d, z10.d, #90
	fcmla	z20.d, p0/m, z29.d, z9.d, #0
	fcmla	z20.d, p0/m, z29.d, z9.d, #90
	fadd	z23.d, z23.d, z20.d
	st1d	z23.d, p0, [x2]
	movprfx	z21, z31
	fcmla	z21.d, p0/m, z28.d, z11.d, #0
	add	x2, x1, 256
	fcmla	z21.d, p0/m, z28.d, z11.d, #90
	fcmla	z21.d, p0/m, z27.d, z10.d, #0
	fcmla	z21.d, p0/m, z27.d, z10.d, #90
	fcmla	z21.d, p0/m, z16.d, z9.d, #0
	fcmla	z21.d, p0/m, z16.d, z9.d, #90
	fadd	z14.d, z14.d, z21.d
	st1d	z14.d, p0, [x2]
	movprfx	z13, z31
	fcmla	z13.d, p0/m, z25.d, z11.d, #0
	add	x2, x1, 320
	fcmla	z13.d, p0/m, z25.d, z11.d, #90
	movprfx	z11, z13
	fcmla	z11.d, p0/m, z19.d, z10.d, #0
	fcmla	z11.d, p0/m, z19.d, z10.d, #90
	movprfx	z10, z11
	fcmla	z10.d, p0/m, z17.d, z9.d, #0
	fcmla	z10.d, p0/m, z17.d, z9.d, #90
	fadd	z2.d, z2.d, z10.d
	st1d	z2.d, p0, [x2]
	fadd	z26.d, z4.d, z26.d
	add	x2, x1, 384
	st1d	z26.d, p0, [x2]
	fadd	z18.d, z18.d, z0.d
	add	x2, x1, 448
	st1d	z18.d, p0, [x2]
	fadd	z8.d, z8.d, z12.d
	add	x2, x1, 512
	st1d	z8.d, p0, [x2]
	fadd	z1.d, z1.d, z20.d
	add	x2, x1, 576
	st1d	z1.d, p0, [x2]
	fadd	z15.d, z15.d, z21.d
	add	x2, x1, 640
	st1d	z15.d, p0, [x2]
	add	x1, x1, 704
	fadd	z3.d, z3.d, z10.d
	add	w9, w9, 1
	st1d	z3.d, p0, [x1]
	cmp	w9, w16
	bne	.L24
