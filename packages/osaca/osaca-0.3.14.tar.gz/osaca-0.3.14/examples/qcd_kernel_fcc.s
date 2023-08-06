.L7469:					// :entr
	.loc 66 321 0 is_stmt 1
..LDL464:
	mov	w4, w6
	.loc 66 322 0
..LDL465:
	mov	w7, w3
	.loc 66 330 0
..LDL466:
	ldr	x9, [x1]	//  "nbr"
	ldr	x10, [x1, -40]	//  "in"
	lsl	w0, w4, 3
	sxtw	x15, w0
	add	x14, x15, 1
	.loc 66 331 0
..LDL467:
	add	x25, x15, 2
	.loc 66 330 0
..LDL468:
	ldr	x0, [x9, x15, lsl #3]	//  (*)
	sxtw	x8, w0
	add	x0, x8, x8
	add	x0, x0, x8
	lsl	x0, x0, 8
	add	x11, x0, x10
	lsl	w0, w7, 3
	ldr	x7, [x9, x14, lsl #3]	//  (*)
	add	x13, x11, 64
	sxtw	x8, w0
	ld1d	{z6.d}, p0/z, [x11, 0, mul vl]	//  (*)
	add	x17, x11, 192
	add	x16, x11, 128
	ldr	x0, [x9, x8, lsl #3]	//  (*)
	ld1d	{z1.d}, p0/z, [x13, 0, mul vl]	//  (*)
	add	x12, x11, 256
	ld1d	{z5.d}, p0/z, [x16, 0, mul vl]	//  (*)
	ld1d	{z4.d}, p0/z, [x17, 0, mul vl]	//  (*)
	ld1d	{z2.d}, p0/z, [x12, 0, mul vl]	//  (*)
	sxtw	x7, w7
	add	x13, x7, x7
	add	x7, x13, x7
	add	x13, x11, 512
	lsl	x7, x7, 8
	ld1d	{z18.d}, p0/z, [x13, 0, mul vl]	//  (*)
	add	x23, x7, x10
	sxtw	x7, w0
	add	x22, x23, 512
	add	x0, x7, x7
	.loc 66 331 0
..LDL469:
	ld1d	{z8.d}, p0/z, [x23, 0, mul vl]	//  (*)
	.loc 66 330 0
..LDL470:
	add	x24, x23, 256
	add	x0, x0, x7
	ldr	x7, [x1, -24]	//  "prm"
	lsl	x0, x0, 8
	.loc 66 331 0
..LDL471:
	add	x26, x23, 64
	ld1d	{z29.d}, p0/z, [x26, 0, mul vl]	//  (*)
	add	x26, x23, 128
	.loc 66 330 0
..LDL472:
	add	x18, x0, x10
	add	x0, x11, 320
	sub	x17, x18, 768
	ld1d	{z3.d}, p0/z, [x0, 0, mul vl]	//  (*)
	add	x0, x11, 384
	ld1d	{z0.d}, p0/z, [x0, 0, mul vl]	//  (*)
	add	x0, x11, 448
	ldrb	w16, [x7, x14]	//  (*)
	ld1d	{z19.d}, p0/z, [x0, 0, mul vl]	//  (*)
	add	x0, x11, 576
	ld1d	{z17.d}, p0/z, [x0, 0, mul vl]	//  (*)
	add	x0, x11, 640
	ld1d	{z16.d}, p0/z, [x0, 0, mul vl]	//  (*)
	add	x0, x11, 704
	ld1d	{z7.d}, p0/z, [x0, 0, mul vl]	//  (*)
	ldr	x0, [x1, -48]	//  "U"
	prfd	1, p0, [x22, 0, mul vl]	//  (*)
	prfd	1, p0, [x24, 0, mul vl]	//  (*)
	prfd	3, p0, [x17, 0, mul vl]	//  (*)
	prfd	1, p0, [x23, 0, mul vl]	//  (*)
	add	x14, x5, x0
	fcadd	z3.d, p0/m, z3.d, z18.d, 270
	ld1d	{z26.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x30, x14, 192
	fcadd	z4.d, p0/m, z4.d, z0.d, 270
	ld1d	{z25.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 384
	fcadd	z2.d, p0/m, z2.d, z19.d, 270
	ld1d	{z24.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 64
	fcadd	z6.d, p0/m, z6.d, z17.d, 270
	ld1d	{z23.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 256
	fcadd	z1.d, p0/m, z1.d, z16.d, 270
	ld1d	{z22.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 448
	fcadd	z5.d, p0/m, z5.d, z7.d, 270
	ld1d	{z21.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 128
	fmov	z0.d, 0.000000e+00
	mov	z18.d, z0.d
	mov	z17.d, z0.d
	mov	z20.d, z0.d
	mov	z19.d, z0.d
	mov	z16.d, z0.d
	mov	z7.d, z0.d
	fcmla	z17.d, p0/m, z25.d, z4.d, #0
	fcmla	z18.d, p0/m, z25.d, z6.d, #0
	fcmla	z20.d, p0/m, z26.d, z6.d, #0
	fcmla	z19.d, p0/m, z26.d, z4.d, #0
	fcmla	z16.d, p0/m, z24.d, z6.d, #0
	fcmla	z7.d, p0/m, z24.d, z4.d, #0
	fcmla	z18.d, p0/m, z25.d, z6.d, #90
	fcmla	z17.d, p0/m, z25.d, z4.d, #90
	.loc 66 331 0
..LDL473:
	ld1d	{z25.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x23, 576
	ld1d	{z28.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x23, 640
	ld1d	{z30.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x23, 704
	.loc 66 330 0
..LDL474:
	fcmla	z20.d, p0/m, z26.d, z6.d, #90
	fcmla	z19.d, p0/m, z26.d, z4.d, #90
	.loc 66 331 0
..LDL475:
	ld1d	{z26.d}, p0/z, [x26, 0, mul vl]	//  (*)
	add	x26, x23, 192
	ld1d	{z9.d}, p0/z, [x26, 0, mul vl]	//  (*)
	.loc 66 330 0
..LDL476:
	fcmla	z16.d, p0/m, z24.d, z6.d, #90
	fcmla	z7.d, p0/m, z24.d, z4.d, #90
	ld1d	{z24.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 320
	add	x14, x14, 512
	ld1d	{z6.d}, p0/z, [x30, 0, mul vl]	//  (*)
	ld1d	{z4.d}, p0/z, [x14, 0, mul vl]	//  (*)
	sub	x14, x18, 512
	.loc 66 331 0
..LDL477:
	fadd	z28.d, z8.d, z28.d
	.loc 66 330 0
..LDL478:
	fcmla	z18.d, p0/m, z22.d, z1.d, #0
	.loc 66 331 0
..LDL479:
	fadd	z15.d, z29.d, z30.d
	.loc 66 330 0
..LDL480:
	fcmla	z17.d, p0/m, z22.d, z2.d, #0
	fcmla	z20.d, p0/m, z23.d, z1.d, #0
	fcmla	z19.d, p0/m, z23.d, z2.d, #0
	fcmla	z16.d, p0/m, z21.d, z1.d, #0
	fcmla	z7.d, p0/m, z21.d, z2.d, #0
	fcmla	z18.d, p0/m, z22.d, z1.d, #90
	fcmla	z17.d, p0/m, z22.d, z2.d, #90
	.loc 66 331 0
..LDL481:
	ld1d	{z22.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x23, 320
	.loc 66 330 0
..LDL482:
	fcmla	z20.d, p0/m, z23.d, z1.d, #90
	fcmla	z19.d, p0/m, z23.d, z2.d, #90
	fcmla	z16.d, p0/m, z21.d, z1.d, #90
	mov	z1.d, z0.d
	fcmla	z7.d, p0/m, z21.d, z2.d, #90
	.loc 66 331 0
..LDL483:
	ld1d	{z21.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x23, 384
	.loc 66 330 0
..LDL484:
	mov	z2.d, z0.d
	.loc 66 331 0
..LDL485:
	ld1d	{z23.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x23, 448
	ld1d	{z31.d}, p0/z, [x24, 0, mul vl]	//  (*)
	.loc 66 330 0
..LDL486:
	fcmla	z18.d, p0/m, z6.d, z5.d, #0
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	sub	x14, x18, 256
	fcmla	z20.d, p0/m, z24.d, z5.d, #0
	fcmla	z19.d, p0/m, z24.d, z3.d, #0
	.loc 66 331 0
..LDL487:
	fsub	z10.d, z21.d, z25.d
	fsub	z12.d, z9.d, z23.d
	.loc 66 330 0
..LDL488:
	fcmla	z17.d, p0/m, z6.d, z3.d, #0
	.loc 66 331 0
..LDL489:
	fsub	z11.d, z22.d, z31.d
	.loc 66 330 0
..LDL490:
	fcmla	z16.d, p0/m, z4.d, z5.d, #0
	fcmla	z7.d, p0/m, z4.d, z3.d, #0
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	.loc 66 331 0
..LDL491:
	add	x14, x8, 1
	.loc 66 330 0
..LDL492:
	fcmla	z20.d, p0/m, z24.d, z5.d, #90
	.loc 66 331 0
..LDL493:
	ldr	x14, [x9, x14, lsl #3]	//  (*)
	.loc 66 330 0
..LDL494:
	fcmla	z19.d, p0/m, z24.d, z3.d, #90
	.loc 66 331 0
..LDL495:
	ld1d	{z24.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x27, 128
	ld1d	{z27.d}, p0/z, [x22, 0, mul vl]	//  "lut"
	.loc 66 330 0
..LDL496:
	fcmla	z18.d, p0/m, z6.d, z5.d, #90
	.loc 66 331 0
..LDL497:
	sxtw	x14, w14
	add	x17, x14, x14
	add	x14, x17, x14
	.loc 66 330 0
..LDL498:
	fcmla	z17.d, p0/m, z6.d, z3.d, #90
	mov	z6.d, z0.d
	.loc 66 331 0
..LDL499:
	lsl	x14, x14, 8
	add	x14, x14, x10
	.loc 66 330 0
..LDL500:
	fcmla	z16.d, p0/m, z4.d, z5.d, #90
	mov	z5.d, z0.d
	.loc 66 331 0
..LDL501:
	sub	x30, x14, 768
	ldr	x14, [x9, x25, lsl #3]	//  (*)
	fadd	z8.d, z26.d, z24.d
	.loc 66 330 0
..LDL502:
	fcmla	z7.d, p0/m, z4.d, z3.d, #90
	mov	z4.d, z0.d
	mov	z3.d, z0.d
	.loc 66 331 0
..LDL503:
	sxtw	x14, w14
	.loc 66 330 0
..LDL504:
	fcadd	z6.d, p0/m, z6.d, z19.d, 90
	.loc 66 331 0
..LDL505:
	add	x17, x14, x14
	.loc 66 330 0
..LDL506:
	fcadd	z3.d, p0/m, z3.d, z20.d, 90
	.loc 66 331 0
..LDL507:
	add	x14, x17, x14
	lsl	x14, x14, 8
	.loc 66 330 0
..LDL508:
	fcadd	z2.d, p0/m, z2.d, z18.d, 90
	.loc 66 331 0
..LDL509:
	add	x18, x14, x10
	add	x14, x18, 256
	add	x17, x18, 512
	.loc 66 330 0
..LDL510:
	fcadd	z5.d, p0/m, z5.d, z17.d, 90
	.loc 66 331 0
..LDL511:
	prfd	1, p0, [x18, 0, mul vl]	//  (*)
	prfd	1, p0, [x14, 0, mul vl]	//  (*)
	.loc 66 330 0
..LDL512:
	fcadd	z1.d, p0/m, z1.d, z16.d, 90
	.loc 66 331 0
..LDL513:
	prfd	1, p0, [x17, 0, mul vl]	//  (*)
	.loc 66 330 0
..LDL514:
	fcadd	z4.d, p0/m, z4.d, z7.d, 90
	.loc 66 331 0
..LDL515:
	cbz	w16, .L7471
	tbl	z28.d, {z28.d}, z27.d
	tbl	z15.d, {z15.d}, z27.d
	tbl	z8.d, {z8.d}, z27.d
	tbl	z12.d, {z12.d}, z27.d
	tbl	z11.d, {z11.d}, z27.d
	tbl	z10.d, {z10.d}, z27.d
.L7471:
	add	x16, x5, 576
	mov	z26.d, z0.d
	mov	z24.d, z0.d
	.loc 66 332 0
..LDL516:
	add	x28, x18, 64
	.loc 66 331 0
..LDL517:
	ldrb	w23, [x7, x25]	//  (*)
	mov	z22.d, z0.d
	mov	z21.d, z0.d
	add	x16, x16, x0
	mov	z25.d, z0.d
	mov	z23.d, z0.d
	ld1d	{z30.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x24, x16, 192
	ld1d	{z9.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x16, 384
	ld1d	{z31.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x16, 64
	ld1d	{z29.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x16, 256
	ld1d	{z14.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x16, 448
	ld1d	{z13.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x16, 128
	prfd	3, p0, [x30, 0, mul vl]	//  (*)
	fcmla	z26.d, p0/m, z30.d, z28.d, #0
	fcmla	z24.d, p0/m, z9.d, z28.d, #0
	fcmla	z22.d, p0/m, z31.d, z28.d, #0
	fcmla	z21.d, p0/m, z31.d, z12.d, #0
	fcmla	z25.d, p0/m, z30.d, z12.d, #0
	fcmla	z26.d, p0/m, z30.d, z28.d, #90
	fcmla	z24.d, p0/m, z9.d, z28.d, #90
	fcmla	z22.d, p0/m, z31.d, z28.d, #90
	ld1d	{z28.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x24, x16, 320
	add	x16, x16, 512
	fcmla	z21.d, p0/m, z31.d, z12.d, #90
	ld1d	{z31.d}, p0/z, [x24, 0, mul vl]	//  (*)
	fcmla	z23.d, p0/m, z9.d, z12.d, #0
	fcmla	z26.d, p0/m, z29.d, z15.d, #0
	fcmla	z24.d, p0/m, z14.d, z15.d, #0
	fcmla	z22.d, p0/m, z13.d, z15.d, #0
	fcmla	z25.d, p0/m, z30.d, z12.d, #90
	ld1d	{z30.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x30, 256
	fcmla	z23.d, p0/m, z9.d, z12.d, #90
	prfd	3, p0, [x16, 0, mul vl]	//  (*)
	add	x16, x30, 512
	fcmla	z26.d, p0/m, z29.d, z15.d, #90
	fcmla	z24.d, p0/m, z14.d, z15.d, #90
	fcmla	z22.d, p0/m, z13.d, z15.d, #90
	fcmla	z25.d, p0/m, z29.d, z11.d, #0
	fcmla	z23.d, p0/m, z14.d, z11.d, #0
	prfd	3, p0, [x16, 0, mul vl]	//  (*)
	.loc 66 332 0
..LDL518:
	add	x16, x8, 2
	.loc 66 331 0
..LDL519:
	fcmla	z26.d, p0/m, z28.d, z8.d, #0
	.loc 66 332 0
..LDL520:
	ldr	x16, [x9, x16, lsl #3]	//  (*)
	.loc 66 331 0
..LDL521:
	fcmla	z24.d, p0/m, z31.d, z8.d, #0
	fcmla	z22.d, p0/m, z30.d, z8.d, #0
	.loc 66 332 0
..LDL522:
	sxtw	x30, w16
	add	x16, x30, x30
	add	x16, x16, x30
	.loc 66 331 0
..LDL523:
	fcmla	z25.d, p0/m, z29.d, z11.d, #90
	.loc 66 332 0
..LDL524:
	lsl	x16, x16, 8
	add	x16, x16, x10
	.loc 66 331 0
..LDL525:
	fcmla	z23.d, p0/m, z14.d, z11.d, #90
	.loc 66 332 0
..LDL526:
	sub	x30, x16, 768
	add	x16, x15, 3
	ldr	x24, [x9, x16, lsl #3]	//  (*)
	.loc 66 331 0
..LDL527:
	fcmla	z26.d, p0/m, z28.d, z8.d, #90
	fcmla	z24.d, p0/m, z31.d, z8.d, #90
	.loc 66 332 0
..LDL528:
	sxtw	x24, w24
	add	x25, x24, x24
	add	x24, x25, x24
	.loc 66 331 0
..LDL529:
	fcmla	z22.d, p0/m, z30.d, z8.d, #90
	.loc 66 332 0
..LDL530:
	lsl	x24, x24, 8
	add	x24, x24, x10
	.loc 66 331 0
..LDL531:
	fcmla	z25.d, p0/m, z28.d, z10.d, #0
	.loc 66 332 0
..LDL532:
	add	x25, x24, 256
	add	x26, x24, 512
	.loc 66 331 0
..LDL533:
	fcmla	z23.d, p0/m, z31.d, z10.d, #0
	.loc 66 332 0
..LDL534:
	prfd	1, p0, [x24, 0, mul vl]	//  (*)
	.loc 66 331 0
..LDL535:
	fadd	z20.d, z20.d, z26.d
	fcmla	z21.d, p0/m, z13.d, z11.d, #0
	.loc 66 332 0
..LDL536:
	prfd	1, p0, [x25, 0, mul vl]	//  (*)
	prfd	1, p0, [x26, 0, mul vl]	//  (*)
	.loc 66 331 0
..LDL537:
	str	z20, [x29, 11, mul vl]	//  (*)
	fadd	z20.d, z3.d, z26.d
	fadd	z3.d, z18.d, z24.d
	fadd	z24.d, z2.d, z24.d
	fadd	z2.d, z16.d, z22.d
	fadd	z22.d, z1.d, z22.d
	fcmla	z25.d, p0/m, z28.d, z10.d, #90
	fcmla	z23.d, p0/m, z31.d, z10.d, #90
	.loc 66 332 0
..LDL538:
	ld1d	{z31.d}, p0/z, [x18, 0, mul vl]	//  (*)
	.loc 66 331 0
..LDL539:
	fcmla	z21.d, p0/m, z13.d, z11.d, #90
	str	z3, [x29, 12, mul vl]	//  (*)
	str	z2, [x29, 13, mul vl]	//  (*)
	fadd	z1.d, z19.d, z25.d
	fsub	z25.d, z6.d, z25.d
	fadd	z19.d, z17.d, z23.d
	fsub	z26.d, z5.d, z23.d
	.loc 66 332 0
..LDL540:
	ld1d	{z23.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 320
	ld1d	{z16.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 384
	ld1d	{z6.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 448
	.loc 66 331 0
..LDL541:
	fcmla	z21.d, p0/m, z30.d, z10.d, #0
	.loc 66 332 0
..LDL542:
	ld1d	{z5.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 576
	ld1d	{z3.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 640
	ld1d	{z2.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 704
	.loc 66 331 0
..LDL543:
	str	z1, [x29, 14, mul vl]	//  (*)
	.loc 66 332 0
..LDL544:
	ld1d	{z1.d}, p0/z, [x14, 0, mul vl]	//  (*)
	sub	x14, x22, 64
	ld1d	{z18.d}, p0/z, [x14, 0, mul vl]	//  "lut"
	fcadd	z31.d, p0/m, z31.d, z6.d, 270
	fcadd	z23.d, p0/m, z23.d, z2.d, 90
	fcadd	z16.d, p0/m, z16.d, z1.d, 90
	.loc 66 331 0
..LDL545:
	fcmla	z21.d, p0/m, z30.d, z10.d, #90
	fadd	z17.d, z7.d, z21.d
	.loc 66 332 0
..LDL546:
	ld1d	{z7.d}, p0/z, [x28, 0, mul vl]	//  (*)
	add	x28, x18, 128
	.loc 66 331 0
..LDL547:
	fsub	z29.d, z4.d, z21.d
	.loc 66 332 0
..LDL548:
	ld1d	{z28.d}, p0/z, [x28, 0, mul vl]	//  (*)
	add	x28, x18, 192
	ld1d	{z4.d}, p0/z, [x17, 0, mul vl]	//  (*)
	ld1d	{z10.d}, p0/z, [x28, 0, mul vl]	//  (*)
	fcadd	z7.d, p0/m, z7.d, z5.d, 270
	fcadd	z28.d, p0/m, z28.d, z4.d, 270
	fcadd	z10.d, p0/m, z10.d, z3.d, 90
	cbz	w23, .L7473
	tbl	z31.d, {z31.d}, z18.d
	tbl	z7.d, {z7.d}, z18.d
	tbl	z28.d, {z28.d}, z18.d
	tbl	z10.d, {z10.d}, z18.d
	tbl	z23.d, {z23.d}, z18.d
	tbl	z16.d, {z16.d}, z18.d
.L7473:
	add	x14, x5, 1152
	mov	z6.d, z0.d
	mov	z5.d, z0.d
	.loc 66 333 0
..LDL549:
	add	x22, x24, 64
	.loc 66 332 0
..LDL550:
	ldrb	w16, [x7, x16]	//  (*)
	mov	z4.d, z0.d
	mov	z2.d, z0.d
	add	x14, x14, x0
	mov	z3.d, z0.d
	mov	z1.d, z0.d
	ld1d	{z8.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x17, x14, 192
	ld1d	{z9.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x17, x14, 384
	ld1d	{z21.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x17, x14, 64
	ld1d	{z30.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x17, x14, 256
	ld1d	{z11.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x17, x14, 448
	ld1d	{z12.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x17, x14, 128
	prfd	3, p0, [x30, 0, mul vl]	//  (*)
	fcmla	z6.d, p0/m, z8.d, z31.d, #0
	fcmla	z5.d, p0/m, z8.d, z10.d, #0
	fcmla	z4.d, p0/m, z9.d, z31.d, #0
	fcmla	z2.d, p0/m, z21.d, z31.d, #0
	fcmla	z3.d, p0/m, z9.d, z10.d, #0
	fcmla	z6.d, p0/m, z8.d, z31.d, #90
	fcmla	z5.d, p0/m, z8.d, z10.d, #90
	ld1d	{z8.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x17, x14, 320
	add	x14, x14, 512
	fcmla	z4.d, p0/m, z9.d, z31.d, #90
	fcmla	z2.d, p0/m, z21.d, z31.d, #90
	ld1d	{z31.d}, p0/z, [x17, 0, mul vl]	//  (*)
	fcmla	z3.d, p0/m, z9.d, z10.d, #90
	fcmla	z6.d, p0/m, z30.d, z7.d, #0
	fcmla	z1.d, p0/m, z21.d, z10.d, #0
	fcmla	z4.d, p0/m, z11.d, z7.d, #0
	fcmla	z2.d, p0/m, z12.d, z7.d, #0
	fcmla	z3.d, p0/m, z11.d, z23.d, #0
	fcmla	z6.d, p0/m, z30.d, z7.d, #90
	fcmla	z1.d, p0/m, z21.d, z10.d, #90
	ld1d	{z21.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x30, 256
	fcmla	z4.d, p0/m, z11.d, z7.d, #90
	fcmla	z2.d, p0/m, z12.d, z7.d, #90
	ldr	z7, [x29, 11, mul vl]	//  (*)
	fcmla	z3.d, p0/m, z11.d, z23.d, #90
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	add	x14, x30, 512
	fcmla	z6.d, p0/m, z8.d, z28.d, #0
	fcmla	z5.d, p0/m, z30.d, z23.d, #0
	fcmla	z4.d, p0/m, z31.d, z28.d, #0
	fcmla	z1.d, p0/m, z12.d, z23.d, #0
	fcmla	z3.d, p0/m, z31.d, z16.d, #0
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	.loc 66 333 0
..LDL551:
	add	x14, x8, 3
	.loc 66 332 0
..LDL552:
	fcmla	z6.d, p0/m, z8.d, z28.d, #90
	.loc 66 333 0
..LDL553:
	ldr	x14, [x9, x14, lsl #3]	//  (*)
	.loc 66 332 0
..LDL554:
	fcmla	z2.d, p0/m, z21.d, z28.d, #0
	fcmla	z4.d, p0/m, z31.d, z28.d, #90
	.loc 66 333 0
..LDL555:
	sxtw	x17, w14
	add	x14, x17, x17
	add	x14, x14, x17
	.loc 66 332 0
..LDL556:
	fcmla	z5.d, p0/m, z30.d, z23.d, #90
	.loc 66 333 0
..LDL557:
	lsl	x14, x14, 8
	add	x14, x14, x10
	.loc 66 332 0
..LDL558:
	fcmla	z3.d, p0/m, z31.d, z16.d, #90
	.loc 66 333 0
..LDL559:
	sub	x17, x14, 768
	add	x14, x15, 4
	ldr	x14, [x9, x14, lsl #3]	//  (*)
	.loc 66 332 0
..LDL560:
	fcadd	z25.d, p0/m, z25.d, z6.d, 90
	fadd	z6.d, z7.d, z6.d
	fcmla	z1.d, p0/m, z12.d, z23.d, #90
	.loc 66 333 0
..LDL561:
	sxtw	x18, w14
	.loc 66 332 0
..LDL562:
	fcmla	z2.d, p0/m, z21.d, z28.d, #90
	.loc 66 333 0
..LDL563:
	add	x14, x18, x18
	ld1d	{z28.d}, p0/z, [x24, 0, mul vl]	//  (*)
	add	x14, x14, x18
	.loc 66 332 0
..LDL564:
	fcadd	z26.d, p0/m, z26.d, z4.d, 90
	.loc 66 333 0
..LDL565:
	lsl	x14, x14, 8
	add	x18, x14, x10
	.loc 66 332 0
..LDL566:
	str	z6, [x29, 7, mul vl]	//  (*)
	.loc 66 333 0
..LDL567:
	add	x14, x18, 256
	add	x30, x18, 512
	.loc 66 332 0
..LDL568:
	fcmla	z5.d, p0/m, z8.d, z16.d, #0
	fcadd	z24.d, p0/m, z24.d, z3.d, 270
	.loc 66 333 0
..LDL569:
	prfd	1, p0, [x18, 0, mul vl]	//  (*)
	.loc 66 332 0
..LDL570:
	ldr	z6, [x29, 12, mul vl]	//  (*)
	.loc 66 333 0
..LDL571:
	prfd	1, p0, [x14, 0, mul vl]	//  (*)
	.loc 66 332 0
..LDL572:
	fcmla	z1.d, p0/m, z21.d, z16.d, #0
	fcadd	z29.d, p0/m, z29.d, z2.d, 90
	.loc 66 333 0
..LDL573:
	prfd	1, p0, [x30, 0, mul vl]	//  (*)
	.loc 66 332 0
..LDL574:
	fadd	z31.d, z6.d, z4.d
	ldr	z4, [x29, 13, mul vl]	//  (*)
	fcmla	z5.d, p0/m, z8.d, z16.d, #90
	fadd	z8.d, z19.d, z3.d
	.loc 66 333 0
..LDL575:
	ld1d	{z6.d}, p0/z, [x25, 0, mul vl]	//  (*)
	.loc 66 332 0
..LDL576:
	fcmla	z1.d, p0/m, z21.d, z16.d, #90
	.loc 66 333 0
..LDL577:
	ld1d	{z16.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 128
	.loc 66 332 0
..LDL578:
	fadd	z30.d, z4.d, z2.d
	ldr	z2, [x29, 14, mul vl]	//  (*)
	.loc 66 333 0
..LDL579:
	ld1d	{z4.d}, p0/z, [x26, 0, mul vl]	//  (*)
	.loc 66 332 0
..LDL580:
	fcadd	z20.d, p0/m, z20.d, z5.d, 270
	fadd	z2.d, z2.d, z5.d
	fcadd	z22.d, p0/m, z22.d, z1.d, 270
	fadd	z9.d, z17.d, z1.d
	.loc 66 333 0
..LDL581:
	ld1d	{z17.d}, p0/z, [x27, 0, mul vl]	//  "lut"
	.loc 66 332 0
..LDL582:
	str	z2, [x29, 9, mul vl]	//  (*)
	.loc 66 333 0
..LDL583:
	ld1d	{z2.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 192
	ld1d	{z1.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 320
	ld1d	{z5.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 384
	ld1d	{z23.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 448
	ld1d	{z7.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 576
	ld1d	{z21.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 640
	ld1d	{z19.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x24, 704
	ld1d	{z3.d}, p0/z, [x22, 0, mul vl]	//  (*)
	fsub	z14.d, z2.d, z4.d
	fsub	z11.d, z28.d, z23.d
	fsub	z16.d, z16.d, z7.d
	fsub	z7.d, z1.d, z21.d
	fsub	z15.d, z6.d, z19.d
	fsub	z23.d, z5.d, z3.d
	cbz	w16, .L7475
	tbl	z11.d, {z11.d}, z17.d
	tbl	z16.d, {z16.d}, z17.d
	tbl	z14.d, {z14.d}, z17.d
	tbl	z7.d, {z7.d}, z17.d
	tbl	z15.d, {z15.d}, z17.d
	tbl	z23.d, {z23.d}, z17.d
.L7475:
	add	x16, x5, 1728
	mov	z6.d, z0.d
	mov	z5.d, z0.d
	.loc 66 335 0
..LDL584:
	add	x26, x18, 64
	.loc 66 333 0
..LDL585:
	mov	z4.d, z0.d
	mov	z3.d, z0.d
	.loc 66 335 0
..LDL586:
	add	x25, x15, 5
	.loc 66 333 0
..LDL587:
	add	x16, x16, x0
	mov	z2.d, z0.d
	mov	z1.d, z0.d
	ld1d	{z10.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x22, x16, 192
	ld1d	{z21.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x16, 384
	ld1d	{z12.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x16, 64
	ld1d	{z28.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x16, 256
	ld1d	{z13.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x16, 448
	ld1d	{z19.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x16, 128
	prfd	3, p0, [x17, 0, mul vl]	//  (*)
	fcmla	z6.d, p0/m, z10.d, z11.d, #0
	fcmla	z5.d, p0/m, z10.d, z7.d, #0
	fcmla	z4.d, p0/m, z21.d, z11.d, #0
	fcmla	z3.d, p0/m, z21.d, z7.d, #0
	fcmla	z1.d, p0/m, z12.d, z7.d, #0
	fcmla	z6.d, p0/m, z10.d, z11.d, #90
	fcmla	z5.d, p0/m, z10.d, z7.d, #90
	fcmla	z2.d, p0/m, z12.d, z11.d, #0
	fcmla	z4.d, p0/m, z21.d, z11.d, #90
	fcmla	z3.d, p0/m, z21.d, z7.d, #90
	fcmla	z6.d, p0/m, z28.d, z16.d, #0
	fcmla	z5.d, p0/m, z28.d, z15.d, #0
	fcmla	z1.d, p0/m, z12.d, z7.d, #90
	ld1d	{z7.d}, p0/z, [x22, 0, mul vl]	//  (*)
	add	x22, x16, 320
	add	x16, x16, 512
	ld1d	{z10.d}, p0/z, [x22, 0, mul vl]	//  (*)
	ld1d	{z21.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x17, 256
	fcmla	z2.d, p0/m, z12.d, z11.d, #90
	.loc 66 335 0
..LDL588:
	ld1d	{z11.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 320
	.loc 66 333 0
..LDL589:
	fcmla	z4.d, p0/m, z13.d, z16.d, #0
	prfd	3, p0, [x16, 0, mul vl]	//  (*)
	add	x16, x17, 512
	fcmla	z6.d, p0/m, z28.d, z16.d, #90
	fcmla	z5.d, p0/m, z28.d, z15.d, #90
	fcmla	z1.d, p0/m, z19.d, z15.d, #0
	fcmla	z2.d, p0/m, z19.d, z16.d, #0
	fcmla	z4.d, p0/m, z13.d, z16.d, #90
	prfd	3, p0, [x16, 0, mul vl]	//  (*)
	.loc 66 335 0
..LDL590:
	add	x16, x8, 4
	.loc 66 333 0
..LDL591:
	fcmla	z6.d, p0/m, z7.d, z14.d, #0
	.loc 66 335 0
..LDL592:
	ldr	x16, [x9, x16, lsl #3]	//  (*)
	.loc 66 333 0
..LDL593:
	fcmla	z5.d, p0/m, z7.d, z23.d, #0
	fcmla	z1.d, p0/m, z19.d, z15.d, #90
	.loc 66 335 0
..LDL594:
	sxtw	x17, w16
	add	x16, x17, x17
	add	x16, x16, x17
	.loc 66 333 0
..LDL595:
	fcmla	z2.d, p0/m, z19.d, z16.d, #90
	.loc 66 335 0
..LDL596:
	lsl	x16, x16, 8
	add	x24, x16, x10
	ldr	x16, [x9, x25, lsl #3]	//  (*)
	.loc 66 333 0
..LDL597:
	fcmla	z3.d, p0/m, z13.d, z15.d, #0
	.loc 66 335 0
..LDL598:
	sub	x23, x24, 768
	prfd	3, p0, [x23, 0, mul vl]	//  (*)
	.loc 66 333 0
..LDL599:
	fcmla	z6.d, p0/m, z7.d, z14.d, #90
	.loc 66 335 0
..LDL600:
	sxtw	x17, w16
	add	x16, x17, x17
	.loc 66 333 0
..LDL601:
	fcmla	z5.d, p0/m, z7.d, z23.d, #90
	ldr	z7, [x29, 7, mul vl]	//  (*)
	.loc 66 335 0
..LDL602:
	add	x16, x16, x17
	lsl	x16, x16, 8
	.loc 66 333 0
..LDL603:
	fcmla	z4.d, p0/m, z10.d, z14.d, #0
	.loc 66 335 0
..LDL604:
	add	x17, x16, x10
	add	x16, x17, 256
	add	x22, x17, 512
	.loc 66 333 0
..LDL605:
	fcmla	z2.d, p0/m, z21.d, z14.d, #0
	fcmla	z1.d, p0/m, z21.d, z23.d, #0
	fcmla	z3.d, p0/m, z13.d, z15.d, #90
	fadd	z7.d, z7.d, z6.d
	fsub	z19.d, z25.d, z6.d
	.loc 66 335 0
..LDL606:
	prfd	1, p0, [x16, 0, mul vl]	//  (*)
	prfd	1, p0, [x17, 0, mul vl]	//  (*)
	prfd	1, p0, [x22, 0, mul vl]	//  (*)
	.loc 66 333 0
..LDL607:
	fcmla	z4.d, p0/m, z10.d, z14.d, #90
	fcmla	z2.d, p0/m, z21.d, z14.d, #90
	fcmla	z1.d, p0/m, z21.d, z23.d, #90
	fcmla	z3.d, p0/m, z10.d, z23.d, #0
	str	z7, [x29, 6, mul vl]	//  (*)
	fadd	z6.d, z31.d, z4.d
	.loc 66 335 0
..LDL608:
	ld1d	{z31.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 384
	.loc 66 333 0
..LDL609:
	fsub	z7.d, z26.d, z4.d
	.loc 66 335 0
..LDL610:
	ld1d	{z26.d}, p0/z, [x26, 0, mul vl]	//  (*)
	add	x26, x18, 128
	ld1d	{z4.d}, p0/z, [x30, 0, mul vl]	//  (*)
	.loc 66 333 0
..LDL611:
	fadd	z16.d, z30.d, z2.d
	fsub	z21.d, z29.d, z2.d
	.loc 66 335 0
..LDL612:
	ld1d	{z30.d}, p0/z, [x18, 0, mul vl]	//  (*)
	.loc 66 333 0
..LDL613:
	fsub	z28.d, z22.d, z1.d
	.loc 66 335 0
..LDL614:
	ld1d	{z22.d}, p0/z, [x26, 0, mul vl]	//  (*)
	add	x26, x18, 192
	.loc 66 333 0
..LDL615:
	str	z6, [x29, 8, mul vl]	//  (*)
	fcmla	z3.d, p0/m, z10.d, z23.d, #90
	fsub	z23.d, z20.d, z5.d
	.loc 66 335 0
..LDL616:
	ld1d	{z6.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 448
	.loc 66 333 0
..LDL617:
	fadd	z10.d, z9.d, z1.d
	.loc 66 335 0
..LDL618:
	ld1d	{z20.d}, p0/z, [x26, 0, mul vl]	//  (*)
	fcadd	z31.d, p0/m, z31.d, z4.d, 90
	mov	z4.d, z0.d
	.loc 66 333 0
..LDL619:
	ldr	z2, [x29, 9, mul vl]	//  (*)
	.loc 66 335 0
..LDL620:
	fcadd	z20.d, p0/m, z20.d, z6.d, 90
	mov	z6.d, z0.d
	.loc 66 333 0
..LDL621:
	fadd	z25.d, z2.d, z5.d
	fadd	z2.d, z8.d, z3.d
	.loc 66 335 0
..LDL622:
	ld1d	{z5.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 576
	.loc 66 333 0
..LDL623:
	fsub	z24.d, z24.d, z3.d
	.loc 66 335 0
..LDL624:
	ld1d	{z3.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 640
	.loc 66 333 0
..LDL625:
	str	z2, [x29, 10, mul vl]	//  (*)
	.loc 66 335 0
..LDL626:
	ld1d	{z2.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x18, 704
	ldrb	w18, [x7, x25]	//  (*)
	.loc 66 336 0
..LDL627:
	add	x25, x15, 6
	.loc 66 335 0
..LDL628:
	ld1d	{z1.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x14, x5, 2304
	fcadd	z30.d, p0/m, z30.d, z3.d, 90
	mov	z3.d, z0.d
	fcadd	z11.d, p0/m, z11.d, z5.d, 90
	add	x14, x14, x0
	ld1d	{z8.d}, p0/z, [x14, 0, mul vl]	//  (*)
	add	x30, x14, 192
	mov	z5.d, z0.d
	ld1d	{z13.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 384
	ld1d	{z29.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 64
	ld1d	{z9.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 256
	ld1d	{z12.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 448
	ld1d	{z14.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 128
	fcadd	z26.d, p0/m, z26.d, z2.d, 90
	mov	z2.d, z0.d
	fcadd	z22.d, p0/m, z22.d, z1.d, 90
	mov	z1.d, z0.d
	fcmla	z5.d, p0/m, z8.d, z20.d, #0
	fcmla	z6.d, p0/m, z8.d, z30.d, #0
	fcmla	z4.d, p0/m, z13.d, z30.d, #0
	fcmla	z3.d, p0/m, z13.d, z20.d, #0
	fcmla	z2.d, p0/m, z29.d, z30.d, #0
	fcmla	z1.d, p0/m, z29.d, z20.d, #0
	fcmla	z6.d, p0/m, z8.d, z30.d, #90
	fcmla	z4.d, p0/m, z13.d, z30.d, #90
	fcmla	z3.d, p0/m, z13.d, z20.d, #90
	fcmla	z2.d, p0/m, z29.d, z30.d, #90
	ld1d	{z30.d}, p0/z, [x30, 0, mul vl]	//  (*)
	add	x30, x14, 320
	add	x14, x14, 512
	fcmla	z5.d, p0/m, z8.d, z20.d, #90
	fcmla	z6.d, p0/m, z9.d, z26.d, #0
	fcmla	z4.d, p0/m, z12.d, z26.d, #0
	fcmla	z3.d, p0/m, z12.d, z11.d, #0
	fcmla	z1.d, p0/m, z29.d, z20.d, #90
	ld1d	{z20.d}, p0/z, [x30, 0, mul vl]	//  (*)
	ld1d	{z29.d}, p0/z, [x14, 0, mul vl]	//  (*)
	sub	x14, x24, 512
	.loc 66 336 0
..LDL629:
	ldr	x30, [x9, x25, lsl #3]	//  (*)
	.loc 66 335 0
..LDL630:
	fcmla	z2.d, p0/m, z14.d, z26.d, #0
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	sub	x14, x24, 256
	fcmla	z6.d, p0/m, z9.d, z26.d, #90
	.loc 66 336 0
..LDL631:
	sxtw	x30, w30
	add	x23, x30, x30
	add	x30, x23, x30
	.loc 66 335 0
..LDL632:
	fcmla	z4.d, p0/m, z12.d, z26.d, #90
	.loc 66 336 0
..LDL633:
	lsl	x30, x30, 8
	add	x30, x30, x10
	.loc 66 335 0
..LDL634:
	fcmla	z3.d, p0/m, z12.d, z11.d, #90
	.loc 66 336 0
..LDL635:
	add	x24, x30, 512
	add	x23, x30, 256
	.loc 66 335 0
..LDL636:
	fcmla	z5.d, p0/m, z9.d, z11.d, #0
	fcmla	z1.d, p0/m, z14.d, z11.d, #0
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	.loc 66 336 0
..LDL637:
	add	x14, x8, 5
	.loc 66 335 0
..LDL638:
	fcmla	z6.d, p0/m, z30.d, z22.d, #0
	.loc 66 336 0
..LDL639:
	ldr	x14, [x9, x14, lsl #3]	//  (*)
	.loc 66 335 0
..LDL640:
	fcmla	z4.d, p0/m, z20.d, z22.d, #0
	fcmla	z3.d, p0/m, z20.d, z31.d, #0
	.loc 66 336 0
..LDL641:
	sxtw	x14, w14
	add	x26, x14, x14
	add	x14, x26, x14
	.loc 66 335 0
..LDL642:
	fcmla	z2.d, p0/m, z14.d, z26.d, #90
	.loc 66 336 0
..LDL643:
	lsl	x14, x14, 8
	add	x26, x14, x10
	add	x14, x17, 64
	.loc 66 335 0
..LDL644:
	fcmla	z5.d, p0/m, z9.d, z11.d, #90
	.loc 66 336 0
..LDL645:
	prfd	1, p0, [x24, 0, mul vl]	//  (*)
	.loc 66 335 0
..LDL646:
	fcmla	z6.d, p0/m, z30.d, z22.d, #90
	fcmla	z4.d, p0/m, z20.d, z22.d, #90
	fcmla	z3.d, p0/m, z20.d, z31.d, #90
	ldr	z20, [x29, 6, mul vl]	//  (*)
	fcmla	z1.d, p0/m, z14.d, z11.d, #90
	fcmla	z2.d, p0/m, z29.d, z22.d, #0
	.loc 66 336 0
..LDL647:
	prfd	1, p0, [x23, 0, mul vl]	//  (*)
	.loc 66 335 0
..LDL648:
	fcadd	z23.d, p0/m, z23.d, z6.d, 270
	fcmla	z5.d, p0/m, z30.d, z31.d, #0
	fadd	z6.d, z20.d, z6.d
	fcadd	z24.d, p0/m, z24.d, z4.d, 270
	.loc 66 336 0
..LDL649:
	prfd	1, p0, [x30, 0, mul vl]	//  (*)
	.loc 66 335 0
..LDL650:
	fcadd	z7.d, p0/m, z7.d, z3.d, 270
	fcmla	z1.d, p0/m, z29.d, z31.d, #0
	str	z6, [x29, 4, mul vl]	//  (*)
	fcmla	z2.d, p0/m, z29.d, z22.d, #90
	fcmla	z5.d, p0/m, z30.d, z31.d, #90
	.loc 66 336 0
..LDL651:
	ld1d	{z30.d}, p0/z, [x17, 0, mul vl]	//  (*)
	.loc 66 335 0
..LDL652:
	ldr	z6, [x29, 8, mul vl]	//  (*)
	fcmla	z1.d, p0/m, z29.d, z31.d, #90
	.loc 66 336 0
..LDL653:
	ld1d	{z29.d}, p0/z, [x14, 0, mul vl]	//  (*)
	sub	x14, x26, 768
	add	x26, x17, 128
	ld1d	{z22.d}, p0/z, [x26, 0, mul vl]	//  (*)
	add	x26, x17, 192
	.loc 66 335 0
..LDL654:
	fadd	z4.d, z6.d, z4.d
	fadd	z31.d, z16.d, z2.d
	fcadd	z28.d, p0/m, z28.d, z2.d, 270
	fcadd	z19.d, p0/m, z19.d, z5.d, 270
	fadd	z9.d, z25.d, z5.d
	.loc 66 336 0
..LDL655:
	ld1d	{z5.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x17, 320
	.loc 66 335 0
..LDL656:
	str	z4, [x29, 5, mul vl]	//  (*)
	fcadd	z21.d, p0/m, z21.d, z1.d, 270
	fadd	z16.d, z10.d, z1.d
	.loc 66 336 0
..LDL657:
	ld1d	{z1.d}, p0/z, [x22, 0, mul vl]	//  (*)
	.loc 66 335 0
..LDL658:
	ldr	z2, [x29, 10, mul vl]	//  (*)
	fadd	z8.d, z2.d, z3.d
	.loc 66 336 0
..LDL659:
	ld1d	{z2.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x17, 384
	ld1d	{z3.d}, p0/z, [x26, 0, mul vl]	//  (*)
	ld1d	{z25.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x17, 448
	ld1d	{z4.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x17, 576
	ld1d	{z26.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x17, 640
	add	x17, x17, 704
	ld1d	{z20.d}, p0/z, [x16, 0, mul vl]	//  (*)
	ld1d	{z6.d}, p0/z, [x17, 0, mul vl]	//  (*)
	fadd	z25.d, z3.d, z25.d
	fadd	z12.d, z5.d, z4.d
	fsub	z26.d, z30.d, z26.d
	fsub	z29.d, z29.d, z20.d
	fsub	z22.d, z22.d, z6.d
	fadd	z20.d, z2.d, z1.d
	cbz	w18, .L7477
	tbl	z26.d, {z26.d}, z27.d
	tbl	z29.d, {z29.d}, z27.d
	tbl	z22.d, {z22.d}, z27.d
	tbl	z25.d, {z25.d}, z27.d
	tbl	z12.d, {z12.d}, z27.d
	tbl	z20.d, {z20.d}, z27.d
.L7477:
	ldrb	w16, [x7, x25]	//  (*)
	add	x17, x5, 2880
	mov	z5.d, z0.d
	mov	z3.d, z0.d
	mov	z4.d, z0.d
	mov	z1.d, z0.d
	.loc 66 337 0
..LDL660:
	add	x25, x30, 64
	.loc 66 336 0
..LDL661:
	add	x17, x17, x0
	mov	z6.d, z0.d
	mov	z2.d, z0.d
	.loc 66 337 0
..LDL662:
	add	x15, x15, 7
	.loc 66 336 0
..LDL663:
	ld1d	{z14.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x18, x17, 192
	ld1d	{z10.d}, p0/z, [x18, 0, mul vl]	//  (*)
	add	x18, x17, 384
	ld1d	{z11.d}, p0/z, [x18, 0, mul vl]	//  (*)
	add	x18, x17, 64
	ld1d	{z13.d}, p0/z, [x18, 0, mul vl]	//  (*)
	add	x18, x17, 256
	ld1d	{z27.d}, p0/z, [x18, 0, mul vl]	//  (*)
	add	x18, x17, 448
	ld1d	{z30.d}, p0/z, [x18, 0, mul vl]	//  (*)
	add	x18, x17, 128
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	fcmla	z5.d, p0/m, z14.d, z25.d, #0
	fcmla	z3.d, p0/m, z10.d, z25.d, #0
	fcmla	z1.d, p0/m, z11.d, z25.d, #0
	fcmla	z4.d, p0/m, z10.d, z26.d, #0
	fcmla	z6.d, p0/m, z14.d, z26.d, #0
	fcmla	z2.d, p0/m, z11.d, z26.d, #0
	fcmla	z5.d, p0/m, z14.d, z25.d, #90
	fcmla	z3.d, p0/m, z10.d, z25.d, #90
	fcmla	z1.d, p0/m, z11.d, z25.d, #90
	fcmla	z4.d, p0/m, z10.d, z26.d, #90
	ld1d	{z10.d}, p0/z, [x18, 0, mul vl]	//  (*)
	add	x18, x17, 320
	add	x17, x17, 512
	ld1d	{z25.d}, p0/z, [x17, 0, mul vl]	//  (*)
	add	x17, x14, 256
	add	x14, x14, 512
	fcmla	z6.d, p0/m, z14.d, z26.d, #90
	fcmla	z2.d, p0/m, z11.d, z26.d, #90
	ld1d	{z26.d}, p0/z, [x18, 0, mul vl]	//  (*)
	fcmla	z5.d, p0/m, z13.d, z12.d, #0
	fcmla	z3.d, p0/m, z27.d, z12.d, #0
	fcmla	z1.d, p0/m, z30.d, z12.d, #0
	prfd	3, p0, [x14, 0, mul vl]	//  (*)
	.loc 66 337 0
..LDL664:
	add	x14, x8, 6
	.loc 66 336 0
..LDL665:
	fcmla	z6.d, p0/m, z13.d, z29.d, #0
	.loc 66 337 0
..LDL666:
	ldr	x14, [x9, x14, lsl #3]	//  (*)
	.loc 66 336 0
..LDL667:
	fcmla	z2.d, p0/m, z30.d, z29.d, #0
	fcmla	z5.d, p0/m, z13.d, z12.d, #90
	fcmla	z3.d, p0/m, z27.d, z12.d, #90
	fcmla	z1.d, p0/m, z30.d, z12.d, #90
	prfd	3, p0, [x17, 0, mul vl]	//  (*)
	.loc 66 337 0
..LDL668:
	sxtw	x17, w14
	.loc 66 336 0
..LDL669:
	fcmla	z6.d, p0/m, z13.d, z29.d, #90
	.loc 66 337 0
..LDL670:
	add	x14, x17, x17
	add	x14, x14, x17
	lsl	x14, x14, 8
	.loc 66 336 0
..LDL671:
	fcmla	z2.d, p0/m, z30.d, z29.d, #90
	.loc 66 337 0
..LDL672:
	add	x14, x14, x10
	sub	x17, x14, 768
	ldr	x14, [x9, x15, lsl #3]	//  (*)
	.loc 66 336 0
..LDL673:
	fcmla	z5.d, p0/m, z10.d, z20.d, #0
	fcmla	z3.d, p0/m, z26.d, z20.d, #0
	.loc 66 337 0
..LDL674:
	sxtw	x14, w14
	.loc 66 336 0
..LDL675:
	fcmla	z1.d, p0/m, z25.d, z20.d, #0
	.loc 66 337 0
..LDL676:
	add	x18, x14, x14
	add	x14, x18, x14
	lsl	x14, x14, 8
	.loc 66 336 0
..LDL677:
	fcmla	z4.d, p0/m, z27.d, z29.d, #0
	.loc 66 337 0
..LDL678:
	add	x14, x14, x10
	add	x18, x14, 256
	add	x22, x14, 512
	.loc 66 336 0
..LDL679:
	fcmla	z6.d, p0/m, z10.d, z22.d, #0
	fcmla	z2.d, p0/m, z25.d, z22.d, #0
	fcmla	z5.d, p0/m, z10.d, z20.d, #90
	fcmla	z3.d, p0/m, z26.d, z20.d, #90
	fcmla	z1.d, p0/m, z25.d, z20.d, #90
	ldr	z20, [x29, 4, mul vl]	//  (*)
	fcmla	z4.d, p0/m, z27.d, z29.d, #90
	.loc 66 337 0
..LDL680:
	ld1d	{z29.d}, p0/z, [x23, 0, mul vl]	//  (*)
	add	x23, x30, 320
	.loc 66 336 0
..LDL681:
	fcmla	z6.d, p0/m, z10.d, z22.d, #90
	fcmla	z2.d, p0/m, z25.d, z22.d, #90
	fadd	z19.d, z19.d, z5.d
	.loc 66 337 0
..LDL682:
	prfd	1, p0, [x14, 0, mul vl]	//  (*)
	.loc 66 336 0
..LDL683:
	fadd	z27.d, z8.d, z3.d
	.loc 66 337 0
..LDL684:
	ld1d	{z8.d}, p0/z, [x23, 0, mul vl]	//  (*)
	add	x23, x30, 384
	prfd	1, p0, [x18, 0, mul vl]	//  (*)
	prfd	1, p0, [x22, 0, mul vl]	//  (*)
	.loc 66 336 0
..LDL685:
	fcmla	z4.d, p0/m, z26.d, z22.d, #0
	fadd	z25.d, z20.d, z6.d
	fsub	z20.d, z23.d, z6.d
	ldr	z6, [x29, 5, mul vl]	//  (*)
	fsub	z23.d, z28.d, z2.d
	.loc 66 337 0
..LDL686:
	ld1d	{z28.d}, p0/z, [x25, 0, mul vl]	//  (*)
	add	x25, x30, 128
	ld1d	{z30.d}, p0/z, [x25, 0, mul vl]	//  (*)
	add	x25, x30, 192
	.loc 66 336 0
..LDL687:
	fcmla	z4.d, p0/m, z26.d, z22.d, #90
	fadd	z26.d, z7.d, z3.d
	fadd	z7.d, z21.d, z1.d
	.loc 66 337 0
..LDL688:
	ld1d	{z21.d}, p0/z, [x30, 0, mul vl]	//  (*)
	.loc 66 336 0
..LDL689:
	fadd	z6.d, z6.d, z4.d
	fsub	z22.d, z24.d, z4.d
	fadd	z4.d, z31.d, z2.d
	fadd	z2.d, z9.d, z5.d
	fadd	z24.d, z16.d, z1.d
	.loc 66 337 0
..LDL690:
	ld1d	{z16.d}, p0/z, [x25, 0, mul vl]	//  (*)
	.loc 66 336 0
..LDL691:
	str	z6, [x29, 1, mul vl]	//  (*)
	.loc 66 337 0
..LDL692:
	ld1d	{z6.d}, p0/z, [x23, 0, mul vl]	//  (*)
	add	x23, x30, 448
	ld1d	{z5.d}, p0/z, [x23, 0, mul vl]	//  (*)
	add	x23, x30, 576
	ld1d	{z1.d}, p0/z, [x23, 0, mul vl]	//  (*)
	add	x23, x30, 640
	add	x30, x30, 704
	.loc 66 336 0
..LDL693:
	str	z4, [x29, 2, mul vl]	//  (*)
	str	z2, [x29, 3, mul vl]	//  (*)
	.loc 66 337 0
..LDL694:
	ld1d	{z2.d}, p0/z, [x24, 0, mul vl]	//  (*)
	ld1d	{z4.d}, p0/z, [x23, 0, mul vl]	//  (*)
	ld1d	{z3.d}, p0/z, [x30, 0, mul vl]	//  (*)
	fcadd	z21.d, p0/m, z21.d, z6.d, 90
	fcadd	z28.d, p0/m, z28.d, z5.d, 90
	fcadd	z16.d, p0/m, z16.d, z1.d, 270
	fcadd	z30.d, p0/m, z30.d, z2.d, 90
	fcadd	z29.d, p0/m, z29.d, z4.d, 270
	fcadd	z8.d, p0/m, z8.d, z3.d, 270
	cbz	w16, .L7479
	tbl	z21.d, {z21.d}, z18.d
	tbl	z28.d, {z28.d}, z18.d
	tbl	z30.d, {z30.d}, z18.d
	tbl	z16.d, {z16.d}, z18.d
	tbl	z29.d, {z29.d}, z18.d
	tbl	z8.d, {z8.d}, z18.d
.L7479:
	ldrb	w15, [x7, x15]	//  (*)
	add	x7, x5, 3456
	mov	z6.d, z0.d
	mov	z5.d, z0.d
	mov	z4.d, z0.d
	mov	z2.d, z0.d
	add	x7, x7, x0
	mov	z3.d, z0.d
	mov	z1.d, z0.d
	ld1d	{z12.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x16, x7, 192
	ld1d	{z10.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x7, 384
	ld1d	{z9.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x7, 64
	ld1d	{z31.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x7, 256
	ld1d	{z11.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x7, 448
	ld1d	{z18.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x7, 128
	prfd	3, p0, [x17, 0, mul vl]	//  (*)
	.loc 66 338 0
..LDL695:
	prfd	1, p0, [x11, 0, mul vl]	//  (*)
	prfd	1, p0, [x12, 0, mul vl]	//  (*)
	prfd	1, p0, [x13, 0, mul vl]	//  (*)
	.loc 66 337 0
..LDL696:
	fcmla	z6.d, p0/m, z12.d, z21.d, #0
	fcmla	z5.d, p0/m, z12.d, z16.d, #0
	fcmla	z4.d, p0/m, z10.d, z21.d, #0
	fcmla	z2.d, p0/m, z9.d, z21.d, #0
	fcmla	z1.d, p0/m, z9.d, z16.d, #0
	fcmla	z6.d, p0/m, z12.d, z21.d, #90
	fcmla	z5.d, p0/m, z12.d, z16.d, #90
	fcmla	z4.d, p0/m, z10.d, z21.d, #90
	fcmla	z2.d, p0/m, z9.d, z21.d, #90
	ld1d	{z21.d}, p0/z, [x16, 0, mul vl]	//  (*)
	add	x16, x7, 320
	add	x7, x7, 512
	fcmla	z1.d, p0/m, z9.d, z16.d, #90
	ld1d	{z9.d}, p0/z, [x16, 0, mul vl]	//  (*)
	fcmla	z6.d, p0/m, z31.d, z28.d, #0
	fcmla	z5.d, p0/m, z31.d, z29.d, #0
	fcmla	z4.d, p0/m, z11.d, z28.d, #0
	fcmla	z3.d, p0/m, z10.d, z16.d, #0
	fcmla	z2.d, p0/m, z18.d, z28.d, #0
	fcmla	z6.d, p0/m, z31.d, z28.d, #90
	fcmla	z5.d, p0/m, z31.d, z29.d, #90
	fcmla	z4.d, p0/m, z11.d, z28.d, #90
	fcmla	z3.d, p0/m, z10.d, z16.d, #90
	ld1d	{z16.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x17, 256
	fcmla	z2.d, p0/m, z18.d, z28.d, #90
	prfd	3, p0, [x7, 0, mul vl]	//  (*)
	add	x7, x17, 512
	fcmla	z6.d, p0/m, z21.d, z30.d, #0
	fcmla	z5.d, p0/m, z21.d, z8.d, #0
	fcmla	z4.d, p0/m, z9.d, z30.d, #0
	fcmla	z1.d, p0/m, z18.d, z29.d, #0
	fcmla	z2.d, p0/m, z16.d, z30.d, #0
	prfd	3, p0, [x7, 0, mul vl]	//  (*)
	.loc 66 338 0
..LDL697:
	add	x7, x8, 7
	.loc 66 337 0
..LDL698:
	fcmla	z6.d, p0/m, z21.d, z30.d, #90
	.loc 66 338 0
..LDL699:
	ldr	x7, [x9, x7, lsl #3]	//  (*)
	.loc 66 337 0
..LDL700:
	fcmla	z5.d, p0/m, z21.d, z8.d, #90
	fcmla	z4.d, p0/m, z9.d, z30.d, #90
	.loc 66 338 0
..LDL701:
	sxtw	x8, w7
	add	x7, x8, x8
	add	x7, x7, x8
	.loc 66 337 0
..LDL702:
	fcmla	z3.d, p0/m, z11.d, z29.d, #0
	.loc 66 338 0
..LDL703:
	lsl	x7, x7, 8
	add	x7, x7, x10
	.loc 66 337 0
..LDL704:
	fcmla	z2.d, p0/m, z16.d, z30.d, #90
	.loc 66 338 0
..LDL705:
	sub	x8, x7, 768
	add	x7, x14, 64
	ld1d	{z30.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 128
	.loc 66 337 0
..LDL706:
	fcadd	z19.d, p0/m, z19.d, z6.d, 270
	fadd	z21.d, z25.d, z6.d
	ldr	z6, [x29, 1, mul vl]	//  (*)
	fcmla	z1.d, p0/m, z18.d, z29.d, #90
	fcadd	z20.d, p0/m, z20.d, z5.d, 90
	fcadd	z26.d, p0/m, z26.d, z4.d, 270
	fcmla	z3.d, p0/m, z11.d, z29.d, #90
	fadd	z25.d, z6.d, z4.d
	ldr	z4, [x29, 2, mul vl]	//  (*)
	fcadd	z7.d, p0/m, z7.d, z2.d, 270
	.loc 66 338 0
..LDL707:
	ld1d	{z6.d}, p0/z, [x22, 0, mul vl]	//  (*)
	.loc 66 337 0
..LDL708:
	fcmla	z1.d, p0/m, z16.d, z8.d, #0
	fadd	z18.d, z4.d, z2.d
	.loc 66 338 0
..LDL709:
	ld1d	{z4.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 192
	.loc 66 337 0
..LDL710:
	ldr	z2, [x29, 3, mul vl]	//  (*)
	.loc 66 338 0
..LDL711:
	ld1d	{z31.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 320
	.loc 66 337 0
..LDL712:
	fcmla	z3.d, p0/m, z9.d, z8.d, #0
	fcmla	z1.d, p0/m, z16.d, z8.d, #90
	fadd	z16.d, z2.d, z5.d
	fcmla	z3.d, p0/m, z9.d, z8.d, #90
	.loc 66 338 0
..LDL713:
	ld1d	{z8.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 384
	ld1d	{z9.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 448
	.loc 66 337 0
..LDL714:
	fadd	z29.d, z24.d, z1.d
	.loc 66 338 0
..LDL715:
	ld1d	{z24.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 576
	.loc 66 337 0
..LDL716:
	fcadd	z23.d, p0/m, z23.d, z1.d, 90
	.loc 66 338 0
..LDL717:
	ld1d	{z5.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 640
	ld1d	{z1.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x14, 704
	ld1d	{z2.d}, p0/z, [x7, 0, mul vl]	//  (*)
	.loc 66 337 0
..LDL718:
	fcadd	z22.d, p0/m, z22.d, z3.d, 90
	fadd	z28.d, z27.d, z3.d
	.loc 66 338 0
..LDL719:
	ld1d	{z27.d}, p0/z, [x14, 0, mul vl]	//  (*)
	ld1d	{z3.d}, p0/z, [x18, 0, mul vl]	//  (*)
	fadd	z30.d, z30.d, z24.d
	fadd	z24.d, z4.d, z6.d
	fadd	z31.d, z31.d, z5.d
	fadd	z8.d, z8.d, z2.d
	fadd	z27.d, z27.d, z9.d
	fadd	z6.d, z3.d, z1.d
	cbz	w15, .L7481
	tbl	z27.d, {z27.d}, z17.d
	tbl	z30.d, {z30.d}, z17.d
	tbl	z24.d, {z24.d}, z17.d
	tbl	z31.d, {z31.d}, z17.d
	tbl	z6.d, {z6.d}, z17.d
	tbl	z8.d, {z8.d}, z17.d
.L7481:					// :term
	add	x7, x5, 4032
	mov	z5.d, z0.d
	mov	z3.d, z0.d
	.loc 66 340 0
..LDL720:
	sxtw	x4, w4
	.loc 66 338 0
..LDL721:
	mov	z2.d, z0.d
	mov	z1.d, z0.d
	.loc 66 348 0
..LDL722:
	add	x2, x2, 1
	.loc 66 338 0
..LDL723:
	add	x0, x7, x0
	mov	z4.d, z0.d
	.loc 66 348 0
..LDL724:
	add	x3, x3, 1
	.loc 66 338 0
..LDL725:
	ld1d	{z12.d}, p0/z, [x0, 0, mul vl]	//  (*)
	add	x7, x0, 192
	.loc 66 348 0
..LDL726:
	add	x6, x6, 1
	.loc 66 338 0
..LDL727:
	ld1d	{z10.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x0, 384
	ld1d	{z11.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x0, 64
	ld1d	{z13.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x0, 256
	ld1d	{z17.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x0, 448
	ld1d	{z9.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x0, 128
	prfd	3, p0, [x8, 0, mul vl]	//  (*)
	fcmla	z5.d, p0/m, z12.d, z27.d, #0
	fcmla	z3.d, p0/m, z10.d, z27.d, #0
	fcmla	z2.d, p0/m, z10.d, z31.d, #0
	fcmla	z1.d, p0/m, z11.d, z27.d, #0
	fcmla	z4.d, p0/m, z12.d, z31.d, #0
	fcmla	z5.d, p0/m, z12.d, z27.d, #90
	fcmla	z0.d, p0/m, z11.d, z31.d, #0
	fcmla	z3.d, p0/m, z10.d, z27.d, #90
	fcmla	z2.d, p0/m, z10.d, z31.d, #90
	ld1d	{z10.d}, p0/z, [x7, 0, mul vl]	//  (*)
	add	x7, x0, 320
	add	x0, x0, 512
	fcmla	z1.d, p0/m, z11.d, z27.d, #90
	ld1d	{z27.d}, p0/z, [x0, 0, mul vl]	//  (*)
	add	x0, x8, 256
	prfd	3, p0, [x0, 0, mul vl]	//  (*)
	add	x0, x8, 512
	fcmla	z5.d, p0/m, z13.d, z30.d, #0
	fcmla	z4.d, p0/m, z12.d, z31.d, #90
	fcmla	z0.d, p0/m, z11.d, z31.d, #90
	ld1d	{z31.d}, p0/z, [x7, 0, mul vl]	//  (*)
	fcmla	z3.d, p0/m, z17.d, z30.d, #0
	fcmla	z1.d, p0/m, z9.d, z30.d, #0
	prfd	3, p0, [x0, 0, mul vl]	//  (*)
	.loc 66 340 0
..LDL728:
	add	x0, x4, x4
	.loc 66 338 0
..LDL729:
	fcmla	z5.d, p0/m, z13.d, z30.d, #90
	.loc 66 340 0
..LDL730:
	add	x0, x0, x4
	ldr	x4, [x1, -32]	//  "out"
	lsl	x0, x0, 8
	.loc 66 338 0
..LDL731:
	fcmla	z4.d, p0/m, z13.d, z6.d, #0
	.loc 66 340 0
..LDL732:
	add	x0, x4, x0
	.loc 66 338 0
..LDL733:
	fcmla	z2.d, p0/m, z17.d, z6.d, #0
	.loc 66 343 0
..LDL734:
	add	x4, x0, 64
	.loc 66 338 0
..LDL735:
	fcmla	z0.d, p0/m, z9.d, z6.d, #0
	fcmla	z3.d, p0/m, z17.d, z30.d, #90
	fcmla	z5.d, p0/m, z10.d, z24.d, #0
	fcmla	z1.d, p0/m, z9.d, z30.d, #90
	fcmla	z4.d, p0/m, z13.d, z6.d, #90
	fcmla	z2.d, p0/m, z17.d, z6.d, #90
	fcmla	z0.d, p0/m, z9.d, z6.d, #90
	fcmla	z5.d, p0/m, z10.d, z24.d, #90
	fcmla	z3.d, p0/m, z31.d, z24.d, #0
	fcmla	z1.d, p0/m, z27.d, z24.d, #0
	fcmla	z4.d, p0/m, z10.d, z8.d, #0
	fcmla	z2.d, p0/m, z31.d, z8.d, #0
	fadd	z6.d, z5.d, z21.d
	fadd	z5.d, z5.d, z19.d
	fcmla	z0.d, p0/m, z27.d, z8.d, #0
	fcmla	z3.d, p0/m, z31.d, z24.d, #90
	fcmla	z1.d, p0/m, z27.d, z24.d, #90
	fcmla	z4.d, p0/m, z10.d, z8.d, #90
	.loc 66 343 0
..LDL736:
	st1d	{z6.d}, p0, [x0, 0, mul vl]	//  (*)
	.loc 66 338 0
..LDL737:
	fcmla	z2.d, p0/m, z31.d, z8.d, #90
	fadd	z19.d, z3.d, z25.d
	fadd	z17.d, z3.d, z26.d
	fadd	z3.d, z1.d, z18.d
	fadd	z7.d, z1.d, z7.d
	fcmla	z0.d, p0/m, z27.d, z8.d, #90
	fadd	z1.d, z4.d, z16.d
	fadd	z4.d, z4.d, z20.d
	.loc 66 343 0
..LDL738:
	st1d	{z19.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 128
	.loc 66 338 0
..LDL739:
	fadd	z16.d, z2.d, z28.d
	fadd	z2.d, z2.d, z22.d
	.loc 66 343 0
..LDL740:
	st1d	{z3.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 192
	st1d	{z1.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 256
	st1d	{z16.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 320
	.loc 66 338 0
..LDL741:
	fadd	z18.d, z0.d, z29.d
	fadd	z0.d, z0.d, z23.d
	.loc 66 343 0
..LDL742:
	st1d	{z18.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 384
	st1d	{z5.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 448
	st1d	{z17.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 512
	st1d	{z7.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 576
	st1d	{z4.d}, p0, [x4, 0, mul vl]	//  (*)
	add	x4, x0, 640
	add	x0, x0, 704
	st1d	{z2.d}, p0, [x4, 0, mul vl]	//  (*)
	st1d	{z0.d}, p0, [x0, 0, mul vl]	//  (*)
	.loc 66 348 0
..LDL743:
	ldr	x0, [x1, -16]	//  "Ls"
	cmp	x2, x0
	bcc	.L7469
