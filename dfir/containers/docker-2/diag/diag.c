/*
 * diag — System Diagnostics Reporter
 * Version 3.1.2
 *
 * Author: 7ankalis — Securinets ENIT
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define VERSION "3.1.2"

static const char *AGENT_ENDPOINT = "https://metrics-collect.xyz/v1/agent";
static const char *UPLOAD_ENDPOINT = "https://webhook-relay.cloud/upload";
static const char *BUILD_ID = "SecurinetsENIT{5tr1ng5_1n_b1n4ry_n3v3r_l13}";
static const char *INTERNAL_TOKEN = "sysdiag-agent-3.1.2-prod";

void print_version(void) {
    printf("sysdiag %s\n", VERSION);
    printf("build: %s\n", BUILD_ID);
}

void run_checks(void) {
    printf("[*] Running system diagnostics...\n");
    printf("[*] Checking CPU load...\n");
    printf("[*] Checking memory...\n");
    printf("[*] Checking disk...\n");
    printf("[*] Checking network...\n");
    printf("[+] All checks passed.\n");
}

void print_help(const char *prog) {
    printf("Usage: %s [command]\n", prog);
    printf("\nCommands:\n");
    printf("  version    Print version information\n");
    printf("  check      Run system diagnostics\n");
    printf("  report     Send diagnostics to the agent\n");
    printf("  help       Show this message\n");
}

int main(int argc, char **argv) {
    if (argc < 2) {
        print_help(argv[0]);
        return 0;
    }

    if (strcmp(argv[1], "version") == 0) {
        print_version();
    } else if (strcmp(argv[1], "check") == 0) {
        run_checks();
    } else if (strcmp(argv[1], "report") == 0) {
        printf("[*] Connecting to agent at %s\n", AGENT_ENDPOINT);
        printf("[*] Using token %s\n", INTERNAL_TOKEN);
        printf("[*] Uploading to %s\n", UPLOAD_ENDPOINT);
        printf("[+] Report sent.\n");
    } else if (strcmp(argv[1], "help") == 0 || strcmp(argv[1], "--help") == 0) {
        print_help(argv[0]);
    } else {
        printf("Unknown command: %s\n", argv[1]);
        return 1;
    }

    return 0;
}
