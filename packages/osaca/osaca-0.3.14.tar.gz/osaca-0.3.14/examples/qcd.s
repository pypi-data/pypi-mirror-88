	.arch armv8-a+sve
	.file	"bench.cc"
	.text
	.global	__aarch64_ldadd4_relax
	.align	2
	.p2align 4,,11
	.type	_Z16omp_thread_countv._omp_fn.0, %function
_Z16omp_thread_countv._omp_fn.0:
.LFB3693:
	.cfi_startproc
	stp	x29, x30, [sp, -16]!
	.cfi_def_cfa_offset 16
	.cfi_offset 29, -16
	.cfi_offset 30, -8
	mov	x1, x0
	mov	w0, 1
	mov	x29, sp
	bl	__aarch64_ldadd4_relax
	ldp	x29, x30, [sp], 16
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE3693:
	.size	_Z16omp_thread_countv._omp_fn.0, .-_Z16omp_thread_countv._omp_fn.0
	.section	.rodata.str1.8,"aMS",@progbits,1
	.align	3
.LC1:
	.string	"dslash_kernel"
	.text
	.align	2
	.p2align 4,,11
	.type	main._omp_fn.2, %function
main._omp_fn.2:
.LFB3696:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA3696
	stp	x29, x30, [sp, -16]!
	.cfi_def_cfa_offset 16
	.cfi_offset 29, -16
	.cfi_offset 30, -8
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	mov	x29, sp
	bl	likwid_markerStopRegion
	ldp	x29, x30, [sp], 16
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE3696:
	.global	__gxx_personality_v0
	.section	.gcc_except_table,"a",@progbits
.LLSDA3696:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3696-.LLSDACSB3696
.LLSDACSB3696:
.LLSDACSE3696:
	.text
	.size	main._omp_fn.2, .-main._omp_fn.2
	.align	2
	.p2align 4,,11
	.type	main._omp_fn.1, %function
main._omp_fn.1:
.LFB3695:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA3695
	stp	x29, x30, [sp, -16]!
	.cfi_def_cfa_offset 16
	.cfi_offset 29, -16
	.cfi_offset 30, -8
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	mov	x29, sp
	bl	likwid_markerStartRegion
	ldp	x29, x30, [sp], 16
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE3695:
	.section	.gcc_except_table
.LLSDA3695:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3695-.LLSDACSB3695
.LLSDACSB3695:
.LLSDACSE3695:
	.text
	.size	main._omp_fn.1, .-main._omp_fn.1
	.align	2
	.p2align 4,,11
	.type	main._omp_fn.0, %function
main._omp_fn.0:
.LFB3694:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA3694
	stp	x29, x30, [sp, -16]!
	.cfi_def_cfa_offset 16
	.cfi_offset 29, -16
	.cfi_offset 30, -8
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	mov	x29, sp
	bl	likwid_markerRegisterRegion
	ldp	x29, x30, [sp], 16
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE3694:
	.section	.gcc_except_table
.LLSDA3694:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE3694-.LLSDACSB3694
.LLSDACSB3694:
.LLSDACSE3694:
	.text
	.size	main._omp_fn.0, .-main._omp_fn.0
	.align	2
	.p2align 4,,11
	.type	_Z17dslash_kernel_cpuI4SimdISt7complexIdE3vecIdEEEdiPT_S7_S7_PmmmPhi._omp_fn.0, %function
_Z17dslash_kernel_cpuI4SimdISt7complexIdE3vecIdEEEdiPT_S7_S7_PmmmPhi._omp_fn.0:
.LFB3697:
	.cfi_startproc
	addvl	sp, sp, #-14
	.cfi_escape 0xf,0x9,0x8f,0,0x92,0x2e,0,0x8,0x70,0x1e,0x22
	sub	sp, sp, #976
	.cfi_escape 0xf,0xc,0x8f,0,0x92,0x2e,0,0x8,0x70,0x1e,0x23,0xd0,0x7,0x22
	stp	x29, x30, [sp]
	.cfi_escape 0x10,0x1d,0x2,0x8f,0
	.cfi_escape 0x10,0x1e,0x2,0x8f,0x8
	mov	x29, sp
	stp	x19, x20, [sp, 16]
	.cfi_escape 0x10,0x13,0x2,0x8f,0x10
	.cfi_escape 0x10,0x14,0x2,0x8f,0x18
	ldr	x19, [x0, 8]
	cbz	x19, .L10
	stp	x21, x22, [sp, 32]
	.cfi_escape 0x10,0x16,0x2,0x8f,0x28
	.cfi_escape 0x10,0x15,0x2,0x8f,0x20
	mov	x21, x0
	bl	omp_get_num_threads
	sxtw	x20, w0
	bl	omp_get_thread_num
	sxtw	x2, w0
	udiv	x1, x19, x20
	msub	x3, x1, x20, x19
	cmp	x2, x3
	bcc	.L12
.L25:
	madd	x2, x1, x2, x3
	add	x0, x1, x2
	str	x0, [sp, 688]
	cmp	x2, x0
	bcs	.L47
	add	x0, x2, 1
	str	x0, [sp, 672]
	adrp	x0, .LANCHOR0
	add	x0, x0, :lo12:.LANCHOR0
	str	x0, [sp, 704]
	ldr	x0, [x21, 16]
	str	x0, [sp, 680]
	str	w19, [sp, 700]
	ldr	x22, [x21]
	stp	x23, x24, [sp, 48]
	.cfi_escape 0x10,0x18,0x2,0x8f,0x38
	.cfi_escape 0x10,0x17,0x2,0x8f,0x30
	ldr	x20, [x21, 24]
	stp	x25, x26, [sp, 64]
	.cfi_escape 0x10,0x1a,0x3,0x8f,0xc8,0
	.cfi_escape 0x10,0x19,0x3,0x8f,0xc0,0
	ldr	x0, [x21, 32]
	str	x0, [sp, 664]
	ldr	x19, [x21, 40]
	stp	x27, x28, [sp, 80]
	.cfi_escape 0x10,0x1c,0x3,0x8f,0xd8,0
	.cfi_escape 0x10,0x1b,0x3,0x8f,0xd0,0
	ldr	x0, [x21, 48]
	str	x0, [sp, 712]
	stp	d8, d9, [sp, 96]
	.cfi_escape 0x10,0x49,0x3,0x8f,0xe8,0
	.cfi_escape 0x10,0x48,0x3,0x8f,0xe0,0
	stp	d10, d11, [sp, 112]
	.cfi_escape 0x10,0x4b,0x3,0x8f,0xf8,0
	.cfi_escape 0x10,0x4a,0x3,0x8f,0xf0,0
	stp	d12, d13, [sp, 128]
	.cfi_escape 0x10,0x4d,0x3,0x8f,0x88,0x1
	.cfi_escape 0x10,0x4c,0x3,0x8f,0x80,0x1
	stp	d14, d15, [sp, 144]
	.cfi_escape 0x10,0x4f,0x3,0x8f,0x98,0x1
	.cfi_escape 0x10,0x4e,0x3,0x8f,0x90,0x1
	.p2align 3,,7
.L16:
	addvl	x0, sp, #14
	ldr	x1, [sp, 704]
	add	x0, x0, 720
	mov	x2, 256
	bl	memcpy
	ldr	x0, [sp, 672]
	ldr	w1, [sp, 700]
	sub	w6, w0, #1
	cmp	w1, w0
	csel	w15, w0, wzr, gt
	ldr	x0, [sp, 680]
	cbz	x0, .L23
	ldr	x3, [sp, 712]
	ptrue	p0.b, all
	mov	w1, 4608
	mov	z31.d, #0
	mul	w16, w0, w6
	mov	x2, x0
	mul	w15, w15, w0
	mov	w0, 768
	smaddl	x6, w6, w1, x3
	mov	w9, w16
	sub	w15, w15, w16
	add	w16, w16, w2
	add	x14, x6, 4032
	add	x26, x6, 192
	add	x1, x14, 512
	str	x1, [sp, 608]
	add	x1, x6, 384
	str	x1, [sp, 160]
	add	x1, x6, 64
	str	x1, [sp, 168]
	add	x1, x6, 256
	str	x1, [sp, 176]
	add	x1, x6, 448
	str	x1, [sp, 184]
	add	x1, x6, 128
	str	x1, [sp, 192]
	add	x1, x6, 320
	str	x1, [sp, 200]
	add	x1, x6, 512
	str	x1, [sp, 208]
	add	x1, x6, 768
	str	x1, [sp, 216]
	add	x1, x6, 960
	str	x1, [sp, 224]
	add	x1, x6, 640
	str	x1, [sp, 232]
	add	x1, x6, 832
	str	x1, [sp, 240]
	add	x1, x6, 1024
	str	x1, [sp, 248]
	add	x1, x6, 704
	str	x1, [sp, 256]
	add	x1, x6, 896
	str	x1, [sp, 264]
	add	x1, x6, 1088
	str	x1, [sp, 272]
	add	x1, x6, 1344
	str	x1, [sp, 280]
	add	x1, x6, 1536
	str	x1, [sp, 288]
	add	x1, x6, 1216
	str	x1, [sp, 296]
	add	x1, x6, 1408
	str	x1, [sp, 304]
	add	x1, x6, 1600
	str	x1, [sp, 312]
	add	x1, x6, 1280
	str	x1, [sp, 320]
	add	x1, x6, 1472
	str	x1, [sp, 328]
	add	x1, x6, 1664
	str	x1, [sp, 336]
	add	x1, x6, 1920
	str	x1, [sp, 344]
	add	x1, x6, 2112
	str	x1, [sp, 352]
	add	x1, x6, 1792
	str	x1, [sp, 360]
	add	x1, x6, 1984
	str	x1, [sp, 368]
	add	x1, x6, 2176
	str	x1, [sp, 376]
	add	x1, x6, 1856
	str	x1, [sp, 384]
	add	x1, x6, 2048
	str	x1, [sp, 392]
	add	x1, x6, 2240
	str	x1, [sp, 400]
	add	x1, x6, 2496
	str	x1, [sp, 408]
	add	x1, x6, 2688
	str	x1, [sp, 416]
	add	x1, x6, 2368
	str	x1, [sp, 424]
	add	x1, x6, 2560
	str	x1, [sp, 432]
	add	x1, x6, 2752
	str	x1, [sp, 440]
	add	x1, x6, 2432
	str	x1, [sp, 448]
	add	x1, x6, 2624
	str	x1, [sp, 456]
	add	x1, x6, 2816
	str	x1, [sp, 464]
	add	x1, x6, 3072
	str	x1, [sp, 472]
	add	x1, x6, 3264
	str	x1, [sp, 480]
	add	x1, x6, 2944
	str	x1, [sp, 488]
	add	x1, x6, 3136
	str	x1, [sp, 496]
	add	x1, x6, 3328
	str	x1, [sp, 504]
	add	x1, x6, 3008
	str	x1, [sp, 512]
	add	x1, x6, 3200
	str	x1, [sp, 520]
	add	x1, x6, 3392
	str	x1, [sp, 528]
	add	x1, x6, 3648
	str	x1, [sp, 536]
	add	x1, x6, 3840
	str	x1, [sp, 544]
	add	x1, x6, 3520
	str	x1, [sp, 552]
	add	x1, x6, 3712
	str	x1, [sp, 560]
	add	x1, x6, 3904
	str	x1, [sp, 568]
	add	x1, x6, 3584
	str	x1, [sp, 576]
	add	x1, x6, 3776
	str	x1, [sp, 584]
	add	x1, x6, 3968
	str	x1, [sp, 592]
	add	x1, x6, 4096
	str	x1, [sp, 600]
	add	x1, x6, 576
	str	x1, [sp, 616]
	add	x1, x6, 1152
	str	x1, [sp, 656]
	add	x1, x6, 1728
	str	x1, [sp, 648]
	add	x1, x6, 2304
	str	x1, [sp, 640]
	add	x1, x6, 2880
	str	x1, [sp, 632]
	add	x1, x6, 3456
	str	x1, [sp, 624]
	addvl	x1, sp, #14
	add	x25, x14, 192
	add	x1, x1, 848
	add	x24, x14, 384
	ld1d	z5.d, p0/z, [x1]
	add	x23, x14, 256
	addvl	x1, sp, #14
	add	x21, x14, 448
	add	x18, x14, 128
	add	x17, x14, 320
	add	x1, x1, 784
	ld1d	z6.d, p0/z, [x1]
	addvl	x1, sp, #14
	add	x1, x1, 720
	ld1d	z7.d, p0/z, [x1]
	.p2align 3,,7
// OSACA-BEGIN
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
// OSACA-END
.L23:
	ldr	x1, [sp, 672]
	ldr	x2, [sp, 688]
	add	x0, x1, 1
	cmp	x2, x1
	beq	.L48
	str	x0, [sp, 672]
	b	.L16
	.p2align 2,,3
.L47:
	.cfi_restore 23
	.cfi_restore 24
	.cfi_restore 25
	.cfi_restore 26
	.cfi_restore 27
	.cfi_restore 28
	.cfi_restore 72
	.cfi_restore 73
	.cfi_restore 74
	.cfi_restore 75
	.cfi_restore 76
	.cfi_restore 77
	.cfi_restore 78
	.cfi_restore 79
	ldp	x21, x22, [sp, 32]
	.cfi_restore 22
	.cfi_restore 21
.L10:
	ldp	x29, x30, [sp]
	ldp	x19, x20, [sp, 16]
	.cfi_restore 29
	.cfi_restore 30
	.cfi_restore 19
	.cfi_restore 20
	addvl	sp, sp, #14
	.cfi_def_cfa_offset 976
	add	sp, sp, 976
	.cfi_def_cfa_offset 0
	ret
	.p2align 2,,3
.L48:
	.cfi_escape 0xf,0xc,0x8f,0,0x92,0x2e,0,0x8,0x70,0x1e,0x23,0xd0,0x7,0x22
	.cfi_escape 0x10,0x13,0x2,0x8f,0x10
	.cfi_escape 0x10,0x14,0x2,0x8f,0x18
	.cfi_escape 0x10,0x15,0x2,0x8f,0x20
	.cfi_escape 0x10,0x16,0x2,0x8f,0x28
	.cfi_escape 0x10,0x17,0x2,0x8f,0x30
	.cfi_escape 0x10,0x18,0x2,0x8f,0x38
	.cfi_escape 0x10,0x19,0x3,0x8f,0xc0,0
	.cfi_escape 0x10,0x1a,0x3,0x8f,0xc8,0
	.cfi_escape 0x10,0x1b,0x3,0x8f,0xd0,0
	.cfi_escape 0x10,0x1c,0x3,0x8f,0xd8,0
	.cfi_escape 0x10,0x1d,0x2,0x8f,0
	.cfi_escape 0x10,0x1e,0x2,0x8f,0x8
	.cfi_escape 0x10,0x48,0x3,0x8f,0xe0,0
	.cfi_escape 0x10,0x49,0x3,0x8f,0xe8,0
	.cfi_escape 0x10,0x4a,0x3,0x8f,0xf0,0
	.cfi_escape 0x10,0x4b,0x3,0x8f,0xf8,0
	.cfi_escape 0x10,0x4c,0x3,0x8f,0x80,0x1
	.cfi_escape 0x10,0x4d,0x3,0x8f,0x88,0x1
	.cfi_escape 0x10,0x4e,0x3,0x8f,0x90,0x1
	.cfi_escape 0x10,0x4f,0x3,0x8f,0x98,0x1
	ldp	x29, x30, [sp]
	ldp	x19, x20, [sp, 16]
	ldp	x21, x22, [sp, 32]
	.cfi_restore 22
	.cfi_restore 21
	ldp	x23, x24, [sp, 48]
	.cfi_restore 24
	.cfi_restore 23
	ldp	x25, x26, [sp, 64]
	.cfi_restore 26
	.cfi_restore 25
	ldp	x27, x28, [sp, 80]
	.cfi_restore 28
	.cfi_restore 27
	ldp	d8, d9, [sp, 96]
	.cfi_restore 73
	.cfi_restore 72
	ldp	d10, d11, [sp, 112]
	.cfi_restore 75
	.cfi_restore 74
	ldp	d12, d13, [sp, 128]
	.cfi_restore 77
	.cfi_restore 76
	ldp	d14, d15, [sp, 144]
	.cfi_restore 79
	.cfi_restore 78
	.cfi_restore 29
	.cfi_restore 30
	.cfi_restore 19
	.cfi_restore 20
	addvl	sp, sp, #14
	.cfi_def_cfa_offset 976
	add	sp, sp, 976
	.cfi_def_cfa_offset 0
	ret
.L12:
	.cfi_escape 0xf,0xc,0x8f,0,0x92,0x2e,0,0x8,0x70,0x1e,0x23,0xd0,0x7,0x22
	.cfi_escape 0x10,0x13,0x2,0x8f,0x10
	.cfi_escape 0x10,0x14,0x2,0x8f,0x18
	.cfi_escape 0x10,0x15,0x2,0x8f,0x20
	.cfi_escape 0x10,0x16,0x2,0x8f,0x28
	.cfi_escape 0x10,0x1d,0x2,0x8f,0
	.cfi_escape 0x10,0x1e,0x2,0x8f,0x8
	add	x1, x1, 1
	mov	x3, 0
	b	.L25
	.cfi_endproc
.LFE3697:
	.size	_Z17dslash_kernel_cpuI4SimdISt7complexIdE3vecIdEEEdiPT_S7_S7_PmmmPhi._omp_fn.0, .-_Z17dslash_kernel_cpuI4SimdISt7complexIdE3vecIdEEEdiPT_S7_S7_PmmmPhi._omp_fn.0
	.align	2
	.p2align 4,,11
	.type	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0, %function
_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0:
.LFB3704:
	.cfi_startproc
	stp	x29, x30, [sp, -32]!
	.cfi_def_cfa_offset 32
	.cfi_offset 29, -32
	.cfi_offset 30, -24
	mov	x29, sp
	stp	x19, x20, [sp, 16]
	.cfi_offset 19, -16
	.cfi_offset 20, -8
	mov	x19, x0
	ldr	x0, [x0]
	ldr	x0, [x0, -24]
	add	x0, x19, x0
	ldr	x20, [x0, 240]
	cbz	x20, .L54
	ldrb	w0, [x20, 56]
	cbz	w0, .L51
	ldrb	w1, [x20, 67]
.L52:
	mov	x0, x19
	bl	_ZNSo3putEc
	ldp	x19, x20, [sp, 16]
	ldp	x29, x30, [sp], 32
	.cfi_remember_state
	.cfi_restore 30
	.cfi_restore 29
	.cfi_restore 19
	.cfi_restore 20
	.cfi_def_cfa_offset 0
	b	_ZNSo5flushEv
.L51:
	.cfi_restore_state
	mov	x0, x20
	bl	_ZNKSt5ctypeIcE13_M_widen_initEv
	ldr	x2, [x20]
	mov	w1, 10
	mov	x0, x20
	ldr	x2, [x2, 48]
	blr	x2
	and	w1, w0, 255
	b	.L52
.L54:
	bl	_ZSt16__throw_bad_castv
	.cfi_endproc
.LFE3704:
	.size	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0, .-_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	.align	2
	.p2align 4,,11
	.global	_Z16omp_thread_countv
	.type	_Z16omp_thread_countv, %function
_Z16omp_thread_countv:
.LFB2996:
	.cfi_startproc
	stp	x29, x30, [sp, -32]!
	.cfi_def_cfa_offset 32
	.cfi_offset 29, -32
	.cfi_offset 30, -24
	mov	w3, 0
	mov	w2, 0
	mov	x29, sp
	add	x1, sp, 24
	adrp	x0, _Z16omp_thread_countv._omp_fn.0
	add	x0, x0, :lo12:_Z16omp_thread_countv._omp_fn.0
	str	wzr, [sp, 24]
	bl	GOMP_parallel
	ldr	w0, [sp, 24]
	ldp	x29, x30, [sp], 32
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE2996:
	.size	_Z16omp_thread_countv, .-_Z16omp_thread_countv
	.section	.rodata._ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_.str1.8,"aMS",@progbits,1
	.align	3
.LC2:
	.string	"cannot create std::vector larger than max_size()"
	.section	.text._ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_,"axG",@progbits,_ZNSt6vectorIf16alignedAllocatorIfEEC5EmRKS1_,comdat
	.align	2
	.p2align 4,,11
	.weak	_ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_
	.type	_ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_, %function
_ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_:
.LFB3244:
	.cfi_startproc
	stp	x29, x30, [sp, -48]!
	.cfi_def_cfa_offset 48
	.cfi_offset 29, -48
	.cfi_offset 30, -40
	mov	x29, sp
	stp	x19, x20, [sp, 16]
	.cfi_offset 19, -32
	.cfi_offset 20, -24
	mov	x19, x0
	mov	x0, 2305843009213693951
	cmp	x1, x0
	bhi	.L65
	stp	xzr, xzr, [x19]
	lsl	x20, x1, 2
	str	xzr, [x19, 16]
	cbz	x1, .L59
	mov	x2, x20
	add	x0, sp, 40
	mov	x1, 2097152
	bl	posix_memalign
	ldr	x1, [sp, 40]
	cmp	w0, 0
	csel	x0, x1, xzr, eq
	str	x0, [x19]
	add	x2, x0, x20
	str	x2, [x19, 8]
	str	x2, [x19, 16]
	ldp	x19, x20, [sp, 16]
	ldp	x29, x30, [sp], 48
	.cfi_remember_state
	.cfi_restore 30
	.cfi_restore 29
	.cfi_restore 19
	.cfi_restore 20
	.cfi_def_cfa_offset 0
	ret
	.p2align 2,,3
.L59:
	.cfi_restore_state
	mov	x2, 0
	str	xzr, [x19]
	str	x2, [x19, 8]
	str	xzr, [x19, 16]
	ldp	x19, x20, [sp, 16]
	ldp	x29, x30, [sp], 48
	.cfi_remember_state
	.cfi_restore 30
	.cfi_restore 29
	.cfi_restore 19
	.cfi_restore 20
	.cfi_def_cfa_offset 0
	ret
.L65:
	.cfi_restore_state
	adrp	x0, .LC2
	add	x0, x0, :lo12:.LC2
	bl	_ZSt20__throw_length_errorPKc
	.cfi_endproc
.LFE3244:
	.size	_ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_, .-_ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_
	.weak	_ZNSt6vectorIf16alignedAllocatorIfEEC1EmRKS1_
	.set	_ZNSt6vectorIf16alignedAllocatorIfEEC1EmRKS1_,_ZNSt6vectorIf16alignedAllocatorIfEEC2EmRKS1_
	.section	.text._ZNSt6vectorId16alignedAllocatorIdEEC2EmRKS1_,"axG",@progbits,_ZNSt6vectorId16alignedAllocatorIdEEC5EmRKS1_,comdat
	.align	2
	.p2align 4,,11
	.weak	_ZNSt6vectorId16alignedAllocatorIdEEC2EmRKS1_
	.type	_ZNSt6vectorId16alignedAllocatorIdEEC2EmRKS1_, %function
_ZNSt6vectorId16alignedAllocatorIdEEC2EmRKS1_:
.LFB3259:
	.cfi_startproc
	stp	x29, x30, [sp, -48]!
	.cfi_def_cfa_offset 48
	.cfi_offset 29, -48
	.cfi_offset 30, -40
	mov	x29, sp
	stp	x19, x20, [sp, 16]
	.cfi_offset 19, -32
	.cfi_offset 20, -24
	mov	x19, x0
	mov	x0, 1152921504606846975
	cmp	x1, x0
	bhi	.L74
	stp	xzr, xzr, [x19]
	lsl	x20, x1, 3
	str	xzr, [x19, 16]
	cbz	x1, .L68
	mov	x2, x20
	add	x0, sp, 40
	mov	x1, 2097152
	bl	posix_memalign
	ldr	x1, [sp, 40]
	cmp	w0, 0
	csel	x0, x1, xzr, eq
	str	x0, [x19]
	add	x2, x0, x20
	str	x2, [x19, 8]
	str	x2, [x19, 16]
	ldp	x19, x20, [sp, 16]
	ldp	x29, x30, [sp], 48
	.cfi_remember_state
	.cfi_restore 30
	.cfi_restore 29
	.cfi_restore 19
	.cfi_restore 20
	.cfi_def_cfa_offset 0
	ret
	.p2align 2,,3
.L68:
	.cfi_restore_state
	mov	x2, 0
	str	xzr, [x19]
	str	x2, [x19, 8]
	str	xzr, [x19, 16]
	ldp	x19, x20, [sp, 16]
	ldp	x29, x30, [sp], 48
	.cfi_remember_state
	.cfi_restore 30
	.cfi_restore 29
	.cfi_restore 19
	.cfi_restore 20
	.cfi_def_cfa_offset 0
	ret
.L74:
	.cfi_restore_state
	adrp	x0, .LC2
	add	x0, x0, :lo12:.LC2
	bl	_ZSt20__throw_length_errorPKc
	.cfi_endproc
.LFE3259:
	.size	_ZNSt6vectorId16alignedAllocatorIdEEC2EmRKS1_, .-_ZNSt6vectorId16alignedAllocatorIdEEC2EmRKS1_
	.weak	_ZNSt6vectorId16alignedAllocatorIdEEC1EmRKS1_
	.set	_ZNSt6vectorId16alignedAllocatorIdEEC1EmRKS1_,_ZNSt6vectorId16alignedAllocatorIdEEC2EmRKS1_
	.section	.rodata.str1.8
	.align	3
.LC3:
	.string	"DW w/ dslash kernel, usage: <binary> <iterations> <in cache = 1, in memory = 0>"
	.align	3
.LC4:
	.string	"DATA IN MEMORY\n"
	.align	3
.LC5:
	.string	"DATA IN CACHE\n"
	.align	3
.LC6:
	.string	"Clock %f\n"
	.align	3
.LC7:
	.string	"Nsimd %d\n"
	.align	3
.LC8:
	.string	"Getting thread number, max = %d\n"
	.align	3
.LC9:
	.string	"Threads %d\n"
	.align	3
.LC10:
	.string	"&U   = "
	.align	3
.LC11:
	.string	"&Psi = "
	.align	3
.LC12:
	.string	"&Phi = "
	.align	3
.LC13:
	.string	"Calling dslash_kernel "
	.align	3
.LC14:
	.string	"  Ls     = "
	.align	3
.LC15:
	.string	"  nsite  = "
	.align	3
.LC16:
	.string	"  umax   = "
	.align	3
.LC17:
	.string	" / "
	.align	3
.LC18:
	.string	" MiB"
	.align	3
.LC19:
	.string	"  fmax   = "
	.align	3
.LC20:
	.string	"  nbrmax = "
	.align	3
.LC21:
	.string	"  vol    = "
	.align	3
.LC22:
	.string	"  iterations    = "
	.align	3
.LC23:
	.string	"XX\t"
	.align	3
.LC24:
	.string	" GFlops/s DP; kernel per Ls "
	.align	3
.LC25:
	.string	" usec / "
	.align	3
.LC26:
	.string	" cycles"
	.align	3
.LC27:
	.string	"YY\t"
	.align	3
.LC28:
	.string	" Flops/cycle DP; kernel per Ls "
	.align	3
.LC29:
	.string	"ZZ\t"
	.align	3
.LC30:
	.string	" Flops/cycle DP per thread; kernel per Ls "
	.align	3
.LC31:
	.string	"\t"
	.align	3
.LC32:
	.string	" % peak"
	.align	3
.LC33:
	.string	" GB/s  RF throughput (base 10)"
	.align	3
.LC34:
	.string	" GiB/s RF throughput (base  2)"
	.align	3
.LC35:
	.string	"\ttotal data transfer RF = "
	.align	3
.LC36:
	.string	"normdiff "
	.align	3
.LC37:
	.string	" ref "
	.align	3
.LC38:
	.string	" result "
	.align	3
.LC39:
	.string	"int main(int, char**)"
	.align	3
.LC40:
	.string	"bench.cc"
	.align	3
.LC41:
	.string	"err <= 1.0e-6"
	.section	.text.startup,"ax",@progbits
	.align	2
	.p2align 4,,11
	.global	main
	.type	main, %function
main:
.LFB2997:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA2997
	stp	x29, x30, [sp, -448]!
	.cfi_def_cfa_offset 448
	.cfi_offset 29, -448
	.cfi_offset 30, -440
	mov	x29, sp
	stp	x19, x20, [sp, 16]
	.cfi_offset 19, -432
	.cfi_offset 20, -424
	adrp	x19, _ZSt4cout
	add	x19, x19, :lo12:_ZSt4cout
	stp	x21, x22, [sp, 32]
	.cfi_offset 21, -416
	.cfi_offset 22, -408
	mov	w21, w0
	mov	x22, x1
	stp	x23, x24, [sp, 48]
	mov	w20, 1000
	stp	x25, x26, [sp, 64]
	stp	x27, x28, [sp, 80]
	stp	d8, d9, [sp, 96]
	stp	d10, d11, [sp, 112]
	stp	d12, d13, [sp, 128]
	stp	d14, d15, [sp, 144]
	.cfi_offset 23, -400
	.cfi_offset 24, -392
	.cfi_offset 25, -384
	.cfi_offset 26, -376
	.cfi_offset 27, -368
	.cfi_offset 28, -360
	.cfi_offset 72, -352
	.cfi_offset 73, -344
	.cfi_offset 74, -336
	.cfi_offset 75, -328
	.cfi_offset 76, -320
	.cfi_offset 77, -312
	.cfi_offset 78, -304
	.cfi_offset 79, -296
.LEHB0:
	bl	likwid_markerInit
	adrp	x1, .LC3
	add	x1, x1, :lo12:.LC3
	mov	x2, 79
	mov	x0, x19
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	cmp	w21, 1
	bgt	.L174
.L76:
	adrp	x1, .LC4
	add	x1, x1, :lo12:.LC4
	mov	x2, 15
	mov	x0, x19
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	w23, 0
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
.L78:
	adrp	x0, .LC42
	ldr	d0, [x0, #:lo12:.LC42]
	adrp	x0, .LC6
	add	x0, x0, :lo12:.LC6
	bl	printf
	mov	w1, 4
	adrp	x0, .LC7
	add	x0, x0, :lo12:.LC7
	bl	printf
	bl	omp_get_max_threads
	mov	w1, w0
	adrp	x0, .LC8
	add	x0, x0, :lo12:.LC8
	bl	printf
	str	wzr, [sp, 384]
	mov	w3, 0
	mov	w2, 0
	add	x1, sp, 384
	adrp	x0, _Z16omp_thread_countv._omp_fn.0
	add	x0, x0, :lo12:_Z16omp_thread_countv._omp_fn.0
	bl	GOMP_parallel
	ldr	w0, [sp, 384]
	mov	w1, w0
	adrp	x0, .LC9
	add	x0, x0, :lo12:.LC9
	str	w1, [sp, 180]
	bl	printf
	add	x2, sp, 384
	add	x0, sp, 192
	mov	x1, 589824
	bl	_ZNSt6vectorId16alignedAllocatorIdEEC1EmRKS1_
.LEHE0:
	ldr	x1, [sp, 192]
	mov	x2, 4718592
	adrp	x0, U_static
	add	x0, x0, :lo12:U_static
	bl	bcopy
	add	x2, sp, 384
	add	x0, sp, 216
	mov	x1, 786432
.LEHB1:
	bl	_ZNSt6vectorId16alignedAllocatorIdEEC1EmRKS1_
.LEHE1:
	ldr	x0, [sp, 216]
	mov	x1, 6291456
	bl	bzero
	add	x2, sp, 384
	add	x0, sp, 240
	mov	x1, 786432
.LEHB2:
	bl	_ZNSt6vectorId16alignedAllocatorIdEEC1EmRKS1_
.LEHE2:
	ldr	x1, [sp, 240]
	mov	x2, 6291456
	adrp	x0, Phi_static
	add	x0, x0, :lo12:Phi_static
	bl	bcopy
	add	x2, sp, 384
	add	x0, sp, 264
	mov	x1, 786432
.LEHB3:
	bl	_ZNSt6vectorId16alignedAllocatorIdEEC1EmRKS1_
.LEHE3:
	ldr	x1, [sp, 264]
	mov	x2, 6291456
	adrp	x0, Psi_cpp_static
	add	x0, x0, :lo12:Psi_cpp_static
	bl	bcopy
	mov	x2, 524288
	mov	x1, 2097152
	add	x0, sp, 384
	bl	posix_memalign
	ldr	x21, [sp, 384]
	cmp	w0, 0
	adrp	x1, nbr_static
	mov	x2, 524288
	csel	x21, x21, xzr, eq
	add	x0, x1, :lo12:nbr_static
	mov	x1, x21
	bl	bcopy
	mov	x2, 65536
	mov	x1, 2097152
	add	x0, sp, 384
	bl	posix_memalign
	ldr	x22, [sp, 384]
	cmp	w0, 0
	adrp	x1, prm_static
	mov	x2, 65536
	csel	x22, x22, xzr, eq
	add	x0, x1, :lo12:prm_static
	mov	x1, x22
	bl	bcopy
	add	x2, sp, 384
	add	x0, sp, 288
	mov	x1, 589824
.LEHB4:
	bl	_ZNSt6vectorIf16alignedAllocatorIfEEC1EmRKS1_
.LEHE4:
	add	x2, sp, 384
	add	x0, sp, 312
	mov	x1, 786432
.LEHB5:
	bl	_ZNSt6vectorIf16alignedAllocatorIfEEC1EmRKS1_
.LEHE5:
	add	x2, sp, 384
	add	x0, sp, 336
	mov	x1, 786432
.LEHB6:
	bl	_ZNSt6vectorIf16alignedAllocatorIfEEC1EmRKS1_
.LEHE6:
	add	x2, sp, 384
	add	x0, sp, 360
	mov	x1, 786432
.LEHB7:
	bl	_ZNSt6vectorIf16alignedAllocatorIfEEC1EmRKS1_
.LEHE7:
	adrp	x1, .LC10
	mov	x0, x19
	add	x1, x1, :lo12:.LC10
	mov	x2, 7
.LEHB8:
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	ldr	x1, [sp, 192]
	mov	x0, x19
	bl	_ZNSo9_M_insertIPKvEERSoT_
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC11
	mov	x0, x19
	add	x1, x1, :lo12:.LC11
	mov	x2, 7
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	ldr	x1, [sp, 216]
	mov	x0, x19
	bl	_ZNSo9_M_insertIPKvEERSoT_
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC12
	mov	x0, x19
	add	x1, x1, :lo12:.LC12
	mov	x2, 7
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	ldr	x1, [sp, 240]
	mov	x0, x19
	bl	_ZNSo9_M_insertIPKvEERSoT_
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC13
	mov	x0, x19
	add	x1, x1, :lo12:.LC13
	mov	x2, 22
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	w3, 0
	mov	w2, 0
	mov	x1, 0
	adrp	x0, main._omp_fn.0
	add	x0, x0, :lo12:main._omp_fn.0
	bl	GOMP_parallel
	mov	w3, 0
	mov	w2, 0
	mov	x1, 0
	adrp	x0, main._omp_fn.1
	add	x0, x0, :lo12:main._omp_fn.1
	bl	GOMP_parallel
	ldr	x26, [sp, 192]
	ldr	x25, [sp, 216]
	ldr	x24, [sp, 240]
#APP
// 211 "my_wilson_grid.h" 1
	isb; mrs x0, cntfrq_el0
// 0 "" 2
#NO_APP
	str	x0, [sp, 184]
	tbnz	w20, #31, .L81
	adrp	x0, _Z17dslash_kernel_cpuI4SimdISt7complexIdE3vecIdEEEdiPT_S7_S7_PmmmPhi._omp_fn.0
	add	x28, x0, :lo12:_Z17dslash_kernel_cpuI4SimdISt7complexIdE3vecIdEEEdiPT_S7_S7_PmmmPhi._omp_fn.0
	mov	w27, 0
	.p2align 3,,7
.L82:
	adrp	x5, .LC43
	add	x4, sp, 544
	str	x21, [sp, 384]
	add	w27, w27, 1
	ldr	q0, [x5, #:lo12:.LC43]
	add	x1, sp, 384
	mov	x0, x28
	mov	w3, 0
	mov	w2, 0
	str	q0, [x4, -152]
	stp	x22, x25, [sp, 408]
	stp	x24, x26, [sp, 424]
	str	w23, [sp, 440]
	bl	GOMP_parallel
	cmp	w27, w20
	bgt	.L81
	cmp	w27, 1
	bne	.L82
#APP
// 284 "my_wilson_grid.h" 1
	isb; mrs x0, cntvct_el0
// 0 "" 2
#NO_APP
	str	x0, [sp, 168]
	b	.L82
.L81:
#APP
// 357 "my_wilson_grid.h" 1
	isb; mrs x0, cntvct_el0
// 0 "" 2
#NO_APP
	ldr	x1, [sp, 168]
	mov	w3, 0
	ldr	d0, [sp, 184]
	sub	x28, x0, x1
	mov	x0, 145685290680320
	mov	w2, 0
	ucvtf	d8, x28
	movk	x0, 0x412e, lsl 48
	fmov	d10, x0
	ucvtf	d0, d0
	adrp	x0, main._omp_fn.2
	mov	x1, 0
	add	x0, x0, :lo12:main._omp_fn.2
	fmul	d8, d8, d10
	fdiv	d8, d8, d0
	bl	GOMP_parallel
	scvtf	d14, w20
	mov	x0, 175921860444160
	fdiv	d10, d8, d10
	movk	x0, 0x4184, lsl 48
	fmov	d9, x0
	mov	x0, 70368744177664
	movk	x0, 0x408f, lsl 48
	fmov	d1, x0
	fmul	d9, d14, d9
	adrp	x0, .LC42
	ldr	d12, [x0, #:lo12:.LC42]
	ldr	w0, [sp, 180]
	fdiv	d9, d9, d8
	scvtf	d13, w0
	mov	x0, 4636737291354636288
	fmov	d11, x0
	mov	x0, 4584664420663164928
	fmov	d0, x0
	mov	x0, x19
	fdiv	d9, d9, d1
	fdiv	d12, d9, d12
	fdiv	d15, d12, d13
	fmul	d11, d15, d11
	fmul	d11, d11, d0
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC14
	mov	x0, x19
	add	x1, x1, :lo12:.LC14
	mov	x2, 11
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	mov	w1, 8
	bl	_ZNSolsEi
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC15
	mov	x0, x19
	add	x1, x1, :lo12:.LC15
	mov	x2, 11
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	mov	x1, 1024
	bl	_ZNSo9_M_insertImEERSoT_
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC16
	mov	x0, x19
	add	x1, x1, :lo12:.LC16
	mov	x2, 11
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	mov	x1, 589824
	bl	_ZNSo9_M_insertImEERSoT_
	adrp	x25, .LC17
	add	x25, x25, :lo12:.LC17
	mov	x24, x0
	mov	x1, x25
	mov	x2, 3
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, 4.5e+0
	mov	x0, x24
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x24, .LC18
	add	x24, x24, :lo12:.LC18
	mov	x26, x0
	mov	x1, x24
	mov	x2, 4
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x26
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC19
	mov	x0, x19
	add	x1, x1, :lo12:.LC19
	mov	x2, 11
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	mov	x1, 786432
	bl	_ZNSo9_M_insertImEERSoT_
	mov	x1, x25
	mov	x2, 3
	mov	x25, x0
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, 6.0e+0
	mov	x0, x25
	bl	_ZNSo9_M_insertIdEERSoT_
	mov	x25, x0
	mov	x1, x24
	mov	x2, 4
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x25
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC20
	mov	x0, x19
	add	x1, x1, :lo12:.LC20
	mov	x2, 11
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	mov	x1, 65536
	bl	_ZNSo9_M_insertImEERSoT_
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC21
	mov	x0, x19
	add	x1, x1, :lo12:.LC21
	mov	x2, 11
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x19
	mov	x1, 32768
	bl	_ZNSo9_M_insertImEERSoT_
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC22
	mov	x0, x19
	add	x1, x1, :lo12:.LC22
	mov	x2, 18
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	w1, w20
	mov	x0, x19
	bl	_ZNSolsEi
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x0, .LC42
	adrp	x1, .LC23
	mov	x2, 3
	add	x1, x1, :lo12:.LC23
	ldr	d0, [x0, #:lo12:.LC42]
	mov	x0, 70368744177664
	movk	x0, 0x408f, lsl 48
	fmov	d1, x0
	mov	x0, x19
	fmul	d0, d10, d0
	fmul	d0, d0, d1
	fmul	d0, d0, d1
	fmul	d0, d0, d1
	str	d0, [sp, 168]
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d9
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC24
	mov	x25, x0
	add	x1, x1, :lo12:.LC24
	mov	x2, 28
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fdiv	d8, d8, d14
	mov	x1, 4562146422526312448
	fmov	d0, x1
	fmov	d1, 1.25e-1
	mov	x0, x25
	fmul	d8, d8, d0
	fmul	d8, d8, d1
	fmov	d0, d8
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x26, .LC25
	add	x26, x26, :lo12:.LC25
	mov	x25, x0
	mov	x1, x26
	mov	x2, 8
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	ldr	d0, [sp, 168]
	mov	x1, 4562146422526312448
	fmov	d1, 1.25e-1
	mov	x0, x25
	fdiv	d9, d0, d14
	fmov	d0, x1
	fmul	d9, d9, d0
	fmul	d9, d9, d1
	fmov	d0, d9
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x25, .LC26
	add	x25, x25, :lo12:.LC26
	mov	x27, x0
	mov	x1, x25
	mov	x2, 7
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x27
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC27
	mov	x0, x19
	add	x1, x1, :lo12:.LC27
	mov	x2, 3
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d12
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC28
	mov	x27, x0
	add	x1, x1, :lo12:.LC28
	mov	x2, 31
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d8
	mov	x0, x27
	bl	_ZNSo9_M_insertIdEERSoT_
	mov	x27, x0
	mov	x1, x26
	mov	x2, 8
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d9
	mov	x0, x27
	bl	_ZNSo9_M_insertIdEERSoT_
	mov	x27, x0
	mov	x1, x25
	mov	x2, 7
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x27
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC29
	mov	x0, x19
	add	x1, x1, :lo12:.LC29
	mov	x2, 3
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d15
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC30
	mov	x27, x0
	add	x1, x1, :lo12:.LC30
	mov	x2, 42
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmul	d0, d13, d8
	mov	x0, x27
	bl	_ZNSo9_M_insertIdEERSoT_
	mov	x1, x26
	mov	x2, 8
	mov	x26, x0
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmul	d0, d13, d9
	mov	x0, x26
	bl	_ZNSo9_M_insertIdEERSoT_
	mov	x1, x25
	mov	x2, 7
	mov	x25, x0
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x25
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x25, .LC31
	add	x25, x25, :lo12:.LC31
	mov	x1, x25
	mov	x0, x19
	mov	x2, 1
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d11
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC32
	mov	x26, x0
	add	x1, x1, :lo12:.LC32
	mov	x2, 7
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x26
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	w2, 94371840
	mov	x0, 225833675390976
	movk	x0, 0x41cd, lsl 48
	fmov	d8, x0
	smull	x20, w20, w2
	mov	x1, 4472074429978902528
	fmov	d1, x1
	mov	x0, x19
	mov	x1, x25
	mov	x2, 1
	ucvtf	d0, x20
	fdiv	d10, d0, d10
	fdiv	d8, d10, d8
	fmul	d10, d10, d1
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d8
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC33
	mov	x20, x0
	add	x1, x1, :lo12:.LC33
	mov	x2, 30
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x20
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	mov	x1, x25
	mov	x0, x19
	mov	x2, 1
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d10
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC34
	mov	x20, x0
	add	x1, x1, :lo12:.LC34
	mov	x2, 30
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x20
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x1, .LC35
	mov	x0, x19
	add	x1, x1, :lo12:.LC35
	mov	x2, 26
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, 140737488355328
	movk	x0, 0x4056, lsl 48
	fmov	d0, x0
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	mov	x1, x24
	mov	x20, x0
	mov	x2, 4
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	x0, x20
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	movi	d8, #0
	mov	x0, 0
	ldr	x3, [sp, 216]
	mov	w1, 786432
	whilelo	p0.d, wzr, w1
	ldr	x2, [sp, 264]
	fmov	d10, d8
	fmov	d9, d8
	.p2align 3,,7
.L85:
	ld1d	z0.d, p0/z, [x2, x0, lsl 3]
	ld1d	z1.d, p0/z, [x3, x0, lsl 3]
	fmul	z2.d, z0.d, z0.d
	incd	x0
	fsub	z0.d, z0.d, z1.d
	fadda	d10, p0, d10, z2.d
	fmul	z1.d, z1.d, z1.d
	fmul	z0.d, z0.d, z0.d
	fadda	d8, p0, d8, z1.d
	fadda	d9, p0, d9, z0.d
	whilelo	p0.d, w0, w1
	b.any	.L85
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	cbz	w23, .L86
.L90:
	ldr	x0, [sp, 360]
	cbz	x0, .L88
	bl	free
.L88:
	ldr	x0, [sp, 336]
	cbz	x0, .L91
	bl	free
.L91:
	ldr	x0, [sp, 312]
	cbz	x0, .L92
	bl	free
.L92:
	ldr	x0, [sp, 288]
	cbz	x0, .L93
	bl	free
.L93:
	mov	x0, x22
	bl	free
	mov	x0, x21
	bl	free
	ldr	x0, [sp, 264]
	cbz	x0, .L114
	bl	free
.L114:
	ldr	x0, [sp, 240]
	cbz	x0, .L94
	bl	free
.L94:
	ldr	x0, [sp, 216]
	cbz	x0, .L95
	bl	free
.L95:
	ldr	x0, [sp, 192]
	cbz	x0, .L141
	bl	free
.L141:
	mov	w0, 0
	ldp	x19, x20, [sp, 16]
	ldp	x21, x22, [sp, 32]
	ldp	x23, x24, [sp, 48]
	ldp	x25, x26, [sp, 64]
	ldp	x27, x28, [sp, 80]
	ldp	d8, d9, [sp, 96]
	ldp	d10, d11, [sp, 112]
	ldp	d12, d13, [sp, 128]
	ldp	d14, d15, [sp, 144]
	ldp	x29, x30, [sp], 448
	.cfi_remember_state
	.cfi_restore 30
	.cfi_restore 29
	.cfi_restore 27
	.cfi_restore 28
	.cfi_restore 25
	.cfi_restore 26
	.cfi_restore 23
	.cfi_restore 24
	.cfi_restore 21
	.cfi_restore 22
	.cfi_restore 19
	.cfi_restore 20
	.cfi_restore 78
	.cfi_restore 79
	.cfi_restore 76
	.cfi_restore 77
	.cfi_restore 74
	.cfi_restore 75
	.cfi_restore 72
	.cfi_restore 73
	.cfi_def_cfa_offset 0
	ret
.L86:
	.cfi_restore_state
	adrp	x1, .LC36
	mov	x0, x19
	add	x1, x1, :lo12:.LC36
	mov	x2, 9
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d9
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC37
	mov	x19, x0
	add	x1, x1, :lo12:.LC37
	mov	x2, 5
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d10
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	adrp	x1, .LC38
	mov	x19, x0
	add	x1, x1, :lo12:.LC38
	mov	x2, 8
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	fmov	d0, d8
	mov	x0, x19
	bl	_ZNSo9_M_insertIdEERSoT_
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	adrp	x0, .LC44
	ldr	d0, [x0, #:lo12:.LC44]
	fcmpe	d9, d0
	bls	.L89
	adrp	x3, .LC39
	adrp	x1, .LC40
	adrp	x0, .LC41
	add	x3, x3, :lo12:.LC39
	add	x1, x1, :lo12:.LC40
	add	x0, x0, :lo12:.LC41
	mov	w2, 346
	bl	__assert_fail
.L89:
	bl	likwid_markerClose
.LEHE8:
	b	.L90
.L174:
	ldr	x0, [x22, 8]
	mov	w2, 10
	mov	x1, 0
	bl	strtol
	mov	w20, w0
	cmp	w21, 2
	beq	.L76
	ldr	x0, [x22, 16]
	mov	w2, 10
	mov	x1, 0
	bl	strtol
	cbz	w0, .L76
	adrp	x1, .LC5
	add	x1, x1, :lo12:.LC5
	mov	x2, 14
	mov	x0, x19
.LEHB9:
	bl	_ZSt16__ostream_insertIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_PKS3_l
	mov	w23, 1
	mov	x0, x19
	bl	_ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_.isra.0
	b	.L78
.L125:
	ldr	x1, [sp, 360]
	mov	x19, x0
	cbz	x1, .L99
	mov	x0, x1
	bl	free
.L99:
	ldr	x0, [sp, 336]
	cbz	x0, .L101
	bl	free
.L101:
	ldr	x0, [sp, 312]
	cbz	x0, .L103
	bl	free
.L103:
	ldr	x0, [sp, 288]
	cbz	x0, .L105
	bl	free
.L105:
	mov	x0, x22
	bl	free
	mov	x0, x21
	bl	free
	ldr	x0, [sp, 264]
	cbz	x0, .L107
	bl	free
.L107:
	ldr	x0, [sp, 240]
	cbz	x0, .L109
	bl	free
.L109:
	ldr	x0, [sp, 216]
	cbz	x0, .L111
	bl	free
.L111:
	ldr	x0, [sp, 192]
	cbz	x0, .L112
	bl	free
.L112:
	mov	x0, x19
	bl	_Unwind_Resume
.LEHE9:
.L118:
	mov	x19, x0
	b	.L111
.L124:
	mov	x19, x0
	b	.L99
.L123:
	mov	x19, x0
	b	.L101
.L120:
	mov	x19, x0
	b	.L107
.L119:
	mov	x19, x0
	b	.L109
.L122:
	mov	x19, x0
	b	.L103
.L121:
	mov	x19, x0
	b	.L105
	.cfi_endproc
.LFE2997:
	.section	.gcc_except_table
.LLSDA2997:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE2997-.LLSDACSB2997
.LLSDACSB2997:
	.uleb128 .LEHB0-.LFB2997
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB2997
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L118-.LFB2997
	.uleb128 0
	.uleb128 .LEHB2-.LFB2997
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L119-.LFB2997
	.uleb128 0
	.uleb128 .LEHB3-.LFB2997
	.uleb128 .LEHE3-.LEHB3
	.uleb128 .L120-.LFB2997
	.uleb128 0
	.uleb128 .LEHB4-.LFB2997
	.uleb128 .LEHE4-.LEHB4
	.uleb128 .L121-.LFB2997
	.uleb128 0
	.uleb128 .LEHB5-.LFB2997
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L122-.LFB2997
	.uleb128 0
	.uleb128 .LEHB6-.LFB2997
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L123-.LFB2997
	.uleb128 0
	.uleb128 .LEHB7-.LFB2997
	.uleb128 .LEHE7-.LEHB7
	.uleb128 .L124-.LFB2997
	.uleb128 0
	.uleb128 .LEHB8-.LFB2997
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L125-.LFB2997
	.uleb128 0
	.uleb128 .LEHB9-.LFB2997
	.uleb128 .LEHE9-.LEHB9
	.uleb128 0
	.uleb128 0
.LLSDACSE2997:
	.section	.text.startup
	.size	main, .-main
	.align	2
	.p2align 4,,11
	.type	_GLOBAL__sub_I__Z16omp_thread_countv, %function
_GLOBAL__sub_I__Z16omp_thread_countv:
.LFB3692:
	.cfi_startproc
	stp	x29, x30, [sp, -32]!
	.cfi_def_cfa_offset 32
	.cfi_offset 29, -32
	.cfi_offset 30, -24
	mov	x29, sp
	str	x19, [sp, 16]
	.cfi_offset 19, -16
	adrp	x19, .LANCHOR1
	add	x19, x19, :lo12:.LANCHOR1
	mov	x0, x19
	bl	_ZNSt8ios_base4InitC1Ev
	mov	x1, x19
	adrp	x2, __dso_handle
	ldr	x19, [sp, 16]
	add	x2, x2, :lo12:__dso_handle
	ldp	x29, x30, [sp], 32
	.cfi_restore 30
	.cfi_restore 29
	.cfi_restore 19
	.cfi_def_cfa_offset 0
	adrp	x0, _ZNSt8ios_base4InitD1Ev
	add	x0, x0, :lo12:_ZNSt8ios_base4InitD1Ev
	b	__cxa_atexit
	.cfi_endproc
.LFE3692:
	.size	_GLOBAL__sub_I__Z16omp_thread_countv, .-_GLOBAL__sub_I__Z16omp_thread_countv
	.section	.init_array,"aw"
	.align	3
	.xword	_GLOBAL__sub_I__Z16omp_thread_countv
	.section	.rodata.cst8,"aM",@progbits,8
	.align	3
.LC42:
	.word	-858993459
	.word	1073532108
	.section	.rodata.cst16,"aM",@progbits,16
	.align	4
.LC43:
	.xword	1024
	.xword	8
	.section	.rodata.cst8
	.align	3
.LC44:
	.word	-1598689907
	.word	1051772663
	.section	.rodata
	.align	3
	.set	.LANCHOR0,. + 0
.LC0:
	.xword	4
	.xword	5
	.xword	6
	.xword	7
	.xword	0
	.xword	1
	.xword	2
	.xword	3
	.xword	2
	.xword	3
	.xword	0
	.xword	1
	.xword	6
	.xword	7
	.xword	4
	.xword	5
	.xword	1
	.xword	0
	.xword	3
	.xword	2
	.xword	5
	.xword	4
	.xword	7
	.xword	6
	.xword	0
	.xword	1
	.xword	2
	.xword	4
	.xword	5
	.xword	6
	.xword	7
	.xword	8
	.bss
	.align	3
	.set	.LANCHOR1,. + 0
	.type	_ZStL8__ioinit, %object
	.size	_ZStL8__ioinit, 1
_ZStL8__ioinit:
	.zero	1
	.hidden	DW.ref.__gxx_personality_v0
	.weak	DW.ref.__gxx_personality_v0
	.section	.data.DW.ref.__gxx_personality_v0,"awG",@progbits,DW.ref.__gxx_personality_v0,comdat
	.align	3
	.type	DW.ref.__gxx_personality_v0, %object
	.size	DW.ref.__gxx_personality_v0, 8
DW.ref.__gxx_personality_v0:
	.xword	__gxx_personality_v0
	.hidden	__dso_handle
	.ident	"GCC: (GNU) 10.1.1 20200507 (Red Hat 10.1.1-1)"
	.section	.note.GNU-stack,"",@progbits
