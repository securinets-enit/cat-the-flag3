#include <stdio.h>
#include <stdlib.h>

void win(void) {
	char flag[128];
	FILE *file = fopen("./flag.txt", "r");
	if (!file) {
		puts("[-] flag.txt missing on server, contact an admin.");
		exit(1);
	}

	if (fgets(flag, sizeof(flag), file)) {
		printf("[+] key accepted. Here's your flag:\n%s\n", flag);
	}

	fclose(file);
	exit(0);
}

void vuln(void) {
	char buffer[64];

	puts("=== SecurinetsENIT baby_win ===");
	puts("Tell me a story:");
	gets(buffer);
	printf("You said: %s\n", buffer);
	puts("Thanks, bye!");
}

int main(void) {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	vuln();
	return 0;
}
