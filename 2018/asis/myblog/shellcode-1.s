	section .text
	global _start
_start:
	xchg eax, ebx
	mov rsi, [rbp]
	syscall
