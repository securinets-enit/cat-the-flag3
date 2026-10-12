/*
 * forge.c  -  "Forged": a lock that writes its own verdict
 *
 * There is NO visible key check anywhere in this program.
 *
 *   1. anti_watch() self-attaches with ptrace(PTRACE_TRACEME). If that fails
 *      (something is already tracing us) the lock refuses to run.
 *   2. The player enters a key: 32 hex digits = 16 bytes = four 4-byte chunks.
 *   3. Each chunk is glued to a fixed 8-byte suffix and MD5'd on its own.
 *   4. Three bytes of each digest (at fixed positions) are written into an
 *      executable page. The page is then CALLED as machine code.
 *   5. The only correct key is the one whose four digests happen to assemble
 *      into exactly:   mov edi, MAGIC ; mov eax, &reveal ; jmp rax
 *      i.e. a call to reveal(MAGIC). Any other key produces garbage code
 *      (and is caught by the signal handler as a plain "nope").
 *
 * The flag lives nowhere in plaintext: reveal() decodes it with a keystream
 * derived from MAGIC, and MAGIC only ever arrives in rdi from forged code.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/ptrace.h>

#include "generated.h"   /* SUFFIX[4][8], POS[3], MAGIC, FLAG_ENC[], FLAG_LEN */

/* ------------------------------------------------------------------ MD5 */
/* compact reference MD5 (public-domain style), single call md5(msg,len,out) */
typedef struct { uint32_t a,b,c,d; uint64_t len; unsigned char buf[64]; size_t n; } md5_ctx;

static uint32_t rol32(uint32_t x, int c){ return (x<<c)|(x>>(32-c)); }

static const uint32_t K[64] = {
0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,
0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,
0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,
0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,
0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391};
static const int S[64] = {
7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21};

static void md5_block(md5_ctx *x, const unsigned char *p){
    uint32_t M[16];
    for(int i=0;i<16;i++) M[i]=(uint32_t)p[i*4]|(p[i*4+1]<<8)|(p[i*4+2]<<16)|((uint32_t)p[i*4+3]<<24);
    uint32_t a=x->a,b=x->b,c=x->c,d=x->d;
    for(int i=0;i<64;i++){
        uint32_t f; int g;
        if(i<16){ f=(b&c)|(~b&d); g=i; }
        else if(i<32){ f=(d&b)|(~d&c); g=(5*i+1)&15; }
        else if(i<48){ f=b^c^d; g=(3*i+5)&15; }
        else { f=c^(b|~d); g=(7*i)&15; }
        uint32_t tmp=d; d=c; c=b;
        b=b+rol32(a+f+K[i]+M[g],S[i]);
        a=tmp;
    }
    x->a+=a; x->b+=b; x->c+=c; x->d+=d;
}

static void md5(const unsigned char *msg, size_t len, unsigned char out[16]){
    md5_ctx x={0x67452301,0xefcdab89,0x98badcfe,0x10325476,0,{0},0};
    x.len=len;
    size_t i=0;
    for(; i+64<=len; i+=64) md5_block(&x,msg+i);
    unsigned char tail[128]; size_t r=len-i;
    memcpy(tail,msg+i,r);
    tail[r++]=0x80;
    size_t pad=(r<=56)?(56-r):(120-r);
    memset(tail+r,0,pad); r+=pad;
    uint64_t bits=(uint64_t)len*8;
    for(int k=0;k<8;k++) tail[r++]=(unsigned char)(bits>>(8*k));
    for(size_t j=0;j<r;j+=64) md5_block(&x,tail+j);
    uint32_t v[4]={x.a,x.b,x.c,x.d};
    for(int k=0;k<4;k++) for(int b=0;b<4;b++) out[k*4+b]=(unsigned char)(v[k]>>(8*b));
}

/* ------------------------------------------------------- the anti-watch gate */
__attribute__((noinline)) void anti_watch(void){
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) == -1) {
        puts("Not while you're watching.");
        exit(1);
    }
}

/* -------------------------------------------------- the hidden flag printer */
/* reveal() is reached ONLY by forged code jumping to it with rdi = MAGIC. */
__attribute__((noinline, used)) void reveal(uint32_t arg){
    if (arg != (uint32_t)MAGIC) {
        puts("nope.");
        fflush(stdout);
        _exit(1);
    }
    unsigned char out[FLAG_LEN + 1];
    uint32_t s = (uint32_t)MAGIC;           /* keystream seeded by the magic */
    for (int i = 0; i < FLAG_LEN; i++) {
        s ^= s << 13; s ^= s >> 17; s ^= s << 5;   /* xorshift32 */
        out[i] = (unsigned char)(FLAG_ENC[i] ^ (s & 0xff));
    }
    out[FLAG_LEN] = '\0';
    puts("The lock forges its own key and swings open:");
    puts((char *)out);
    fflush(stdout);
    _exit(0);
}

/* ------------------------------------------- graceful failure for bad forges */
static void boom(int sig){
    (void)sig;
    static const char msg[] = "nope.\n";
    ssize_t rc = write(1, msg, sizeof msg - 1);
    (void)rc;
    _exit(1);
}

static int hexval(int c){
    if(c>='0'&&c<='9') return c-'0';
    if(c>='a'&&c<='f') return c-'a'+10;
    if(c>='A'&&c<='F') return c-'A'+10;
    return -1;
}

int main(void){
    anti_watch();

    signal(SIGSEGV, boom);
    signal(SIGILL,  boom);
    signal(SIGBUS,  boom);
    signal(SIGFPE,  boom);

    char line[64];
    printf("key: ");
    fflush(stdout);
    if (fgets(line, sizeof line, stdin) == NULL) return 1;
    line[strcspn(line, "\r\n")] = '\0';

    if (strlen(line) != 32) {
        puts("nope.");
        return 1;
    }
    unsigned char key[16];
    for (int i = 0; i < 16; i++) {
        int hi = hexval(line[2*i]), lo = hexval(line[2*i+1]);
        if (hi < 0 || lo < 0) { puts("nope."); return 1; }
        key[i] = (unsigned char)(hi*16 + lo);
    }

    /* executable page, pre-filled with ret so stray flow lands softly */
    unsigned char *page = mmap(NULL, 4096, PROT_READ|PROT_WRITE|PROT_EXEC,
                               MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    if (page == MAP_FAILED) { perror("mmap"); return 1; }
    memset(page, 0xC3, 4096);

    /* forge 12 bytes of code from the four digests */
    for (int i = 0; i < 4; i++) {
        unsigned char msg[12], dig[16];
        memcpy(msg, key + 4*i, 4);
        memcpy(msg + 4, SUFFIX[i], 8);
        md5(msg, 12, dig);
        for (int j = 0; j < 3; j++)
            page[3*i + j] = dig[POS[j]];
    }

    /* jump into whatever we just forged */
    ((void (*)(void))page)();

    /* if the forged code just fell through its own ret, it was wrong */
    puts("nope.");
    return 0;
}
