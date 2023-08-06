        .text
        .file   "example.3a1fbbbh-cgu.0"
        .section        .text.example::square,"ax",@progbits
        .globl  example::square
        .p2align        4, 0x90
        .type   example::square,@function
example::square:
.Lfunc_begin0:
        .file   1 "/home/ce/./example.rs"
        .loc    1 2 0
        .cfi_startproc
        pushq   %rax
        .cfi_def_cfa_offset 16
.Ltmp0:
        .loc    1 3 5 prologue_end
        imull   %edi, %edi
        seto    %al
        testb   $1, %al
        movl    %edi, 4(%rsp)
        jne     .LBB0_2
        .loc    1 0 5 is_stmt 0
        movl    4(%rsp), %eax
        .loc    1 4 2 is_stmt 1
        popq    %rcx
        .cfi_def_cfa_offset 8
        retq
.LBB0_2:
        .cfi_def_cfa_offset 16
        .loc    1 3 5
        leaq    str.0(%rip), %rdi
        leaq    .L__unnamed_1(%rip), %rdx
        movq    core::panicking::panic@GOTPCREL(%rip), %rax
        movl    $33, %esi
        callq   *%rax
        ud2
.Ltmp1:
.Lfunc_end0:
        .size   example::square, .Lfunc_end0-example::square
        .cfi_endproc

        .type   .L__unnamed_2,@object
        .section        .rodata..L__unnamed_2,"a",@progbits
.L__unnamed_2:
        .ascii  "./example.rs"
        .size   .L__unnamed_2, 12

        .type   .L__unnamed_1,@object
        .section        .data.rel.ro..L__unnamed_1,"aw",@progbits
        .p2align        3
.L__unnamed_1:
        .quad   .L__unnamed_2
        .asciz  "\f\000\000\000\000\000\000\000\003\000\000\000\005\000\000"
        .size   .L__unnamed_1, 24

        .type   str.0,@object
        .section        .rodata.str.0,"a",@progbits
        .p2align        4
str.0:
        .ascii  "attempt to multiply with overflow"
        .size   str.0, 33

        .type   __rustc_debug_gdb_scripts_section__,@object
        .section        .debug_gdb_scripts,"aMS",@progbits,1,unique,1
        .weak   __rustc_debug_gdb_scripts_section__
__rustc_debug_gdb_scripts_section__:
        .asciz  "\001gdb_load_rust_pretty_printers.py"
        .size   __rustc_debug_gdb_scripts_section__, 34

        .section        .debug_abbrev,"",@progbits
        .byte   1
        .byte   17
        .byte   1
        .byte   37
        .byte   14
        .byte   19
        .byte   5
        .byte   3
        .byte   14
        .byte   16
        .byte   23
        .byte   27
        .byte   14
        .ascii  "\264B"
        .byte   25
        .byte   17
        .byte   1
        .byte   18
        .byte   6
        .byte   0
        .byte   0
        .byte   2
        .byte   57
        .byte   1
        .byte   3
        .byte   14
        .byte   0
        .byte   0
        .byte   3
        .byte   46
        .byte   0
        .byte   17
        .byte   1
        .byte   18
        .byte   6
        .byte   64
        .byte   24
        .byte   110
        .byte   14
        .byte   3
        .byte   14
        .byte   58
        .byte   11
        .byte   59
        .byte   11
        .byte   63
        .byte   25
        .byte   0
        .byte   0
        .byte   0
        .section        .debug_info,"",@progbits
.Lcu_begin0:
        .long   .Ldebug_info_end0-.Ldebug_info_start0
.Ldebug_info_start0:
        .short  4
        .long   .debug_abbrev
        .byte   8
        .byte   1
        .long   .Linfo_string0
        .short  28
        .long   .Linfo_string1
        .long   .Lline_table_start0
        .long   .Linfo_string2

        .quad   .Lfunc_begin0
        .long   .Lfunc_end0-.Lfunc_begin0
        .byte   2
        .long   .Linfo_string3
        .byte   3
        .quad   .Lfunc_begin0
        .long   .Lfunc_end0-.Lfunc_begin0
        .byte   1
        .byte   87
        .long   .Linfo_string4
        .long   .Linfo_string5
        .byte   1
        .byte   2

        .byte   0
        .byte   0
.Ldebug_info_end0:
        .section        .text.example::square,"ax",@progbits
.Lsec_end0:
        .section        .debug_aranges,"",@progbits
        .long   44
        .short  2
        .long   .Lcu_begin0
        .byte   8
        .byte   0
        .zero   4,255
        .quad   .Lfunc_begin0
        .quad   .Lsec_end0-.Lfunc_begin0
        .quad   0
        .quad   0
        .section        .debug_str,"MS",@progbits,1
.Linfo_string0:
        .asciz  "clang LLVM (rustc version 1.48.0 (7eac88abb 2020-11-16))"
.Linfo_string1:
        .asciz  "./example.rs"
.Linfo_string2:
        .asciz  "/home/ce"
.Linfo_string3:
        .asciz  "example"
.Linfo_string4:
        .asciz  "example::square"
.Linfo_string5:
        .asciz  "square"
        .section        .debug_pubnames,"",@progbits
        .long   .LpubNames_end0-.LpubNames_begin0
.LpubNames_begin0:
        .short  2
        .long   .Lcu_begin0
        .long   74
        .long   47
        .asciz  "square"
        .long   42
        .asciz  "example"
        .long   0
.LpubNames_end0:
        .section        .debug_pubtypes,"",@progbits
        .long   .LpubTypes_end0-.LpubTypes_begin0
.LpubTypes_begin0:
        .short  2
        .long   .Lcu_begin0
        .long   74
        .long   0
.LpubTypes_end0:
        .section        ".note.GNU-stack","",@progbits
        .section        .debug_line,"",@progbits
.Lline_table_start0:
