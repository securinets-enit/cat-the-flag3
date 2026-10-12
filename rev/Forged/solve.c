/*
 * solve.c - organizer reference solver for Forge V3.
 *
 * For each of the 4 chunks, search the 2^32 space of 4 input bytes until
 * md5(chunk || suffix_i) reproduces the 3 target bytes at POS[]. Each chunk
 * is independent, so they parallelise trivially.
 *
 * Usage:
 *   solve <POS0> <POS1> <POS2> \
 *         <suffix0_hex16> <suffix1_hex16> <suffix2_hex16> <suffix3_hex16> \
 *         <target12_hex24>
 * Prints the 16-byte key as 32 hex digits.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint32_t rol32(uint32_t x,int c){return (x<<c)|(x>>(32-c));}
static const uint32_t K[64]={
0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,
0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,
0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,
0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,
0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391};
static const int S[64]={
7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21};

/* md5 of a fixed 12-byte message -> single padded block, done inline */
static void md5_12(const unsigned char m[12], unsigned char out[16]){
    unsigned char blk[64];
    memcpy(blk,m,12);
    blk[12]=0x80;
    memset(blk+13,0,64-13);
    uint64_t bits=12*8;
    for(int k=0;k<8;k++) blk[56+k]=(unsigned char)(bits>>(8*k));
    uint32_t M[16];
    for(int i=0;i<16;i++) M[i]=(uint32_t)blk[i*4]|(blk[i*4+1]<<8)|(blk[i*4+2]<<16)|((uint32_t)blk[i*4+3]<<24);
    uint32_t a=0x67452301,b=0xefcdab89,c=0x98badcfe,d=0x10325476;
    uint32_t A=a,B=b,C=c,D=d;
    for(int i=0;i<64;i++){
        uint32_t f; int g;
        if(i<16){f=(B&C)|(~B&D);g=i;}
        else if(i<32){f=(D&B)|(~D&C);g=(5*i+1)&15;}
        else if(i<48){f=B^C^D;g=(3*i+5)&15;}
        else{f=C^(B|~D);g=(7*i)&15;}
        uint32_t t=D;D=C;C=B;B=B+rol32(A+f+K[i]+M[g],S[i]);A=t;
    }
    a+=A;b+=B;c+=C;d+=D;
    uint32_t v[4]={a,b,c,d};
    for(int k=0;k<4;k++) for(int bb=0;bb<4;bb++) out[k*4+bb]=(unsigned char)(v[k]>>(8*bb));
}

static int POS[3];

static int from_hex(const char *s, unsigned char *out, int n){
    for(int i=0;i<n;i++){ unsigned v; if(sscanf(s+2*i,"%2x",&v)!=1) return -1; out[i]=(unsigned char)v; }
    return 0;
}

/* find 4 input bytes for one chunk; returns found value in *res */
static int solve_chunk(const unsigned char suffix[8], const unsigned char tgt[3], uint32_t *res){
    volatile int found = 0;
    uint32_t answer = 0;
    #pragma omp parallel for schedule(dynamic, 1<<20) shared(found, answer)
    for (long long n = 0; n < (1LL<<32); n++) {
        if (found) continue;
        unsigned char msg[12];
        msg[0]=(unsigned char)(n);
        msg[1]=(unsigned char)(n>>8);
        msg[2]=(unsigned char)(n>>16);
        msg[3]=(unsigned char)(n>>24);
        memcpy(msg+4, suffix, 8);
        unsigned char dig[16];
        md5_12(msg, dig);
        if (dig[POS[0]]==tgt[0] && dig[POS[1]]==tgt[1] && dig[POS[2]]==tgt[2]) {
            #pragma omp critical
            { if(!found){ found=1; answer=(uint32_t)n; } }
        }
    }
    *res = answer;
    return found;
}

int main(int argc, char **argv){
    if (argc != 9){ fprintf(stderr,"bad args\n"); return 2; }
    for(int i=0;i<3;i++) POS[i]=atoi(argv[1+i]);
    unsigned char suf[4][8];
    for(int i=0;i<4;i++) if(from_hex(argv[4+i], suf[i], 8)){ fprintf(stderr,"bad suffix\n"); return 2; }
    unsigned char tgt[12];
    if(from_hex(argv[8], tgt, 12)){ fprintf(stderr,"bad target\n"); return 2; }

    unsigned char key[16];
    for(int i=0;i<4;i++){
        uint32_t v;
        if(!solve_chunk(suf[i], tgt+3*i, &v)){ fprintf(stderr,"chunk %d not found\n",i); return 1; }
        key[4*i+0]=(unsigned char)(v);
        key[4*i+1]=(unsigned char)(v>>8);
        key[4*i+2]=(unsigned char)(v>>16);
        key[4*i+3]=(unsigned char)(v>>24);
        fprintf(stderr,"chunk %d: %08x\n", i, v);
    }
    for(int i=0;i<16;i++) printf("%02x", key[i]);
    printf("\n");
    return 0;
}
