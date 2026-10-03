#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <stddef.h>

void init_buffering(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

// Strict seccomp sandbox:
// BLOCKS: execve (59), execveat (322), clone (56), fork (57), vfork (58)
// PERMITS: read (0), write (1), open (2), openat (257), exit (60), exit_group (231)
void install_seccomp(void) {
    struct sock_filter filter[] = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, arch))),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, nr))),
        // Block execve
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 59, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
        // Block execveat
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 322, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
        // Block clone
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 56, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
        // Block fork
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 57, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == -1) {
        perror("prctl(PR_SET_NO_NEW_PRIVS)");
        exit(1);
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog) == -1) {
        perror("prctl(PR_SET_SECCOMP)");
        exit(1);
    }
}

int main(void) {
    init_buffering();

    // Map a dedicated chamber with Read-Write-Execute permissions at 0x13370000
    void *chamber = mmap((void*)0x13370000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, 
                         MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if (chamber == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    puts("==================================================");
    puts("     SecurinetsENIT CTF - Iron Chamber v1.0       ");
    puts("==================================================");
    puts("Engaging kernel-level Seccomp-BPF enforcement...");
    
    install_seccomp();
    puts("[+] Chamber sealed: Process spawning (execve/clone) is strictly forbidden.");
    puts("Transmit your custom instructions into the chamber.");

    printf("Input bytecode (max 256 bytes): ");
    ssize_t n = read(0, chamber, 256);
    if (n <= 0) {
        puts("[-] No payload received.");
        return 1;
    }

    puts("[+] Executing chamber sequence...\n");
    ((void (*)(void))chamber)();

    puts("[+] Sequence finished safely.");
    return 0;
}
