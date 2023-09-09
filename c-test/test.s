	.file	"test.c"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	leal	4(%esp), %ecx
	.cfi_def_cfa 1, 0
	andl	$-16, %esp
	pushl	-4(%ecx)
	pushl	%ebp
	movl	%esp, %ebp
	.cfi_escape 0x10,0x5,0x2,0x75,0
	pushl	%ebx
	pushl	%ecx
	.cfi_escape 0xf,0x3,0x75,0x78,0x6
	.cfi_escape 0x10,0x3,0x2,0x75,0x7c
	subl	$112, %esp
	call	__x86.get_pc_thunk.bx
	addl	$_GLOBAL_OFFSET_TABLE_, %ebx
	movl	%gs:20, %eax
	movl	%eax, -12(%ebp)
	xorl	%eax, %eax
	movdqa	.LC0@GOTOFF(%ebx), %xmm0
	movups	%xmm0, -112(%ebp)
	movdqa	.LC1@GOTOFF(%ebx), %xmm0
	movups	%xmm0, -96(%ebp)
	movdqa	.LC1@GOTOFF(%ebx), %xmm0
	movups	%xmm0, -80(%ebp)
	movdqa	.LC1@GOTOFF(%ebx), %xmm0
	movups	%xmm0, -64(%ebp)
	movdqa	.LC1@GOTOFF(%ebx), %xmm0
	movups	%xmm0, -48(%ebp)
	movdqa	.LC1@GOTOFF(%ebx), %xmm0
	movups	%xmm0, -32(%ebp)
	movl	$0, -16(%ebp)
	movl	$1819438935, -118(%ebp)
	movw	$100, -114(%ebp)
	subl	$8, %esp
	leal	-118(%ebp), %eax
	pushl	%eax
	leal	-112(%ebp), %eax
	pushl	%eax
	call	strcat@PLT
	addl	$16, %esp
	subl	$12, %esp
	leal	-112(%ebp), %eax
	pushl	%eax
	call	puts@PLT
	addl	$16, %esp
	movl	$0, %eax
	movl	-12(%ebp), %edx
	subl	%gs:20, %edx
	je	.L3
	call	__stack_chk_fail_local
.L3:
	leal	-8(%ebp), %esp
	popl	%ecx
	.cfi_restore 1
	.cfi_def_cfa 1, 0
	popl	%ebx
	.cfi_restore 3
	popl	%ebp
	.cfi_restore 5
	leal	-4(%ecx), %esp
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.section	.rodata
	.align 16
.LC0:
	.long	1819043144
	.long	111
	.long	0
	.long	0
	.align 16
.LC1:
	.long	0
	.long	0
	.long	0
	.long	0
	.section	.text.__x86.get_pc_thunk.bx,"axG",@progbits,__x86.get_pc_thunk.bx,comdat
	.globl	__x86.get_pc_thunk.bx
	.hidden	__x86.get_pc_thunk.bx
	.type	__x86.get_pc_thunk.bx, @function
__x86.get_pc_thunk.bx:
.LFB1:
	.cfi_startproc
	movl	(%esp), %ebx
	ret
	.cfi_endproc
.LFE1:
	.hidden	__stack_chk_fail_local
	.ident	"GCC: (GNU) 13.2.1 20230801"
	.section	.note.GNU-stack,"",@progbits
