/*
 * .relay-agent — background sync daemon
 * Author: 7ankalis — Securinets ENIT
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <sys/stat.h>
#include <fcntl.h>

#define AGENT_VERSION "2.4.0"
#define CONFIG_PATH "/etc/relay.conf"

static void write_pid(const char *path) {
    FILE *f = fopen(path, "w");
    if (f) {
        fprintf(f, "%d\n", getpid());
        fclose(f);
    }
}

static void read_config(void) {
    FILE *f = fopen(CONFIG_PATH, "r");
    if (!f) return;

    char line[256];
    while (fgets(line, sizeof(line), f)) {
        line[strcspn(line, "\r\n")] = 0;
        if (line[0] == '#' || line[0] == 0) continue;
        fprintf(stderr, "[agent] config: %s\n", line);
    }
    fclose(f);
}

int main(int argc, char **argv) {
    fprintf(stderr, "[agent] starting, version %s\n", AGENT_VERSION);

    write_pid("/var/run/.relay-agent.pid");
    read_config();

    fprintf(stderr, "[agent] c2 host: metrics-collect.xyz:443\n");
    fprintf(stderr, "[agent] uplink: /v1/relay\n");

    while (1) {
        sleep(60);
    }

    return 0;
}
