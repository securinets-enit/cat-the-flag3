#!/usr/bin/env python3
"""fix_askers.py — write the TCP server version of each asker."""

TEMPLATE = r'''package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

type question struct {
	text   string
	answer string
}

var questions = []question{
__QUESTIONS__
}

func handleConn(conn net.Conn) {
	defer conn.Close()
	w := bufio.NewWriter(conn)
	r := bufio.NewReader(conn)
	defer w.Flush()

	fmt.Fprintln(w, "__BANNER__")
	fmt.Fprintln(w, "You have 3 attempts for each question.")
	fmt.Fprintln(w, "-----------------------------------------------------")
	w.Flush()

	for i, q := range questions {
		attempts := 0
		for {
			fmt.Fprintf(w, "\nQuestion %d/%d: %s\n", i+1, len(questions), q.text)
			fmt.Fprint(w, "Your Answer: ")
			w.Flush()

			line, err := r.ReadString('\n')
			if err != nil {
				return
			}
			line = strings.TrimSpace(line)

			if strings.EqualFold(line, q.answer) {
				fmt.Fprintln(w, "Correct! ✅")
				break
			}
			attempts++
			if attempts >= 3 {
				fmt.Fprintln(w, "Incorrect. ❌ You have exceeded the maximum number of attempts for this question. The quiz is over.")
				w.Flush()
				return
			}
			fmt.Fprintf(w, "Incorrect. ❌ You have %d attempts remaining for this question.\n", 3-attempts)
		}
	}

	fmt.Fprintln(w, "\nExcellent work, hunter! 🕵️‍♂️")
	fmt.Fprintln(w, "Aw l flag")
	w.Flush()

	flagContent, err := os.ReadFile("flag.txt")
	if err != nil {
		fmt.Fprintln(w, "Error reading flag.txt:", err)
		return
	}
	fmt.Fprintln(w, "\nHere is your flag:")
	fmt.Fprintln(w, string(flagContent))
	w.Flush()
}

func main() {
	ln, err := net.Listen("tcp", "0.0.0.0:__PORT__")
	if err != nil {
		panic(err)
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			continue
		}
		go handleConn(conn)
	}
}
'''


def fmt_questions(questions):
    return "\n".join(f'\t{{"{q}", "{a}"}},' for q, a in questions)


TASKS = {
    "task-02-the-recon/recon/main.go": {
        "port": "9999",
        "banner": "Hello future Threat Hunter. This is a domain reconnaissance challenge.",
        "questions": [
            ("When was cdnjs-mirror.net first registered? (YYYY-MM-DD)", "2026-04-30"),
            ("Which registrar manages cdnjs-mirror.net? (single word, lowercase)", "godaddy"),
            ("Authoritative nameservers — comma-separated, alphabetical, lowercase, no trailing dots", "carl.ns.cloudflare.com,ivy.ns.cloudflare.com"),
            ("Current A records for cdnjs-mirror.net — comma-separated, ascending", "104.21.95.116,172.67.144.188"),
            ("Which organization owns those IPs? (single word, lowercase)", "cloudflare"),
            ("TLS certificate — Common Name (CN) of the ISSUER", "ye1"),
            ("TLS certificate — Organization (O) of the ISSUER (lowercase, no spaces, no apostrophe)", "letsencrypt"),
            ("TLS certificate — date issued (YYYY-MM-DD)", "2026-09-16"),
            ("TLS certificate — date of expiry (YYYY-MM-DD)", "2026-12-15"),
            ("Approximate certificate lifetime in days (integer, round to nearest 5)", "90"),
            ("Subject Alternative Names — comma-separated, alphabetical, lowercase, strip the DNS: prefix", "*.cdnjs-mirror.net,cdnjs-mirror.net"),
            ("SHA-256 fingerprint of the certificate — lowercase hex, no colons", "a3f54b3a3cf50036d8448e6b26c6ef71f14bae603e5f7f7d6bd318f3cf89d8dd"),
            ("Palo Alto category — vertical / subcategory, lowercase", "technology / web & hosting"),
            ("Overall assessment — one of [legitimate, abandoned, suspicious, cdn]", "suspicious"),
        ],
    },
    "task-03-the-dropper/dropper/main.go": {
        "port": "9998",
        "banner": "Hello future Threat Hunter. This is a dropper analysis challenge.",
        "questions": [
            ("What is the name of the second-stage binary that the installer downloads? format: <filename>", "gh-completion"),
            ("What tool does the installer use to fetch the second-stage payload?", "curl"),
            ("What full URL does the installer request? format: <url>", "https://cdnjs-mirror.net/assets/gh-2.42.1-shell-helper.bin?build=75efb0959defbc4b1bdcc6247381b437"),
            ("What is the value of the _BUILD variable? format: <hex>", "75efb0959defbc4b1bdcc6247381b437"),
            ("What HTTP query parameter carries the build identifier?", "build"),
            ("Where on disk does the second-stage binary get saved? format: ~/<path>", "~/.local/share/gh-cli/gh-completion"),
            ("What scheduler does the installer use for persistence?", "cron"),
            ("What cron schedule re-executes the payload? format: 5-field cron", "*/30 * * * *"),
            ("What cron keyword triggers execution at boot?", "@reboot"),
            ("What command writes the cron entries?", "crontab"),
            ("What utility detaches the payload from the parent process so it survives logout?", "nohup"),
            ("In one short phrase, what is the purpose of '2>/dev/null || true' at the end of the curl line?", "suppress errors"),
        ],
    },
    "task-04-the-implant/implant/main.go": {
        "port": "9997",
        "banner": "Hello future Threat Hunter. This is a payload analysis challenge.",
        "questions": [
            ("What is the file format of the artifact?", "elf"),
            ("What is the target architecture? format: <arch>-<bits>", "x86-64"),
            ("Is the binary stripped of symbols?", "yes"),
            ("What is the exact byte size of the binary?", "19969992"),
            ("What is the MD5 hash of the binary?", "afad825988139b2ab9a72611d4717ce5"),
            ("What is the SHA-256 hash of the binary?", "13352c0c87c485a1616d6bde5037005cd4f68249f5061d51273a2f8af5403f93"),
            ("Which user owns the binary?", "root"),
            ("What is the file permission mode in octal? format: 0XXX", "0755"),
            ("What was the PID of the payload?", "2552"),
            ("What was the parent PID of the payload? format: <integer>", "1"),
            ("What was the working directory of the process at execution?", "/tmp/gh-extract/gh_2.42.1_linux_amd64"),
            ("What is the absolute path of the payload executable?", "/root/.local/share/gh-cli/gh-completion"),
            ("How many cron entries did the installer create? format: <integer>", "2"),
            ("What is the periodic schedule that re-executes the payload? format: 5-field cron", "*/30 * * * *"),
            ("What cron keyword triggers execution at boot?", "@reboot"),
            ("What is the delivery domain?", "cdnjs-mirror.net"),
            ("What is the C2 domain as seen in the TLS SNI?", "gh-actions-runner.xyz"),
            ("What is the C2 port?", "443"),
            ("What is the approximate beacon interval in seconds? format: <integer>", "10"),
            ("Which CDN provider fronts the C2 domain?", "cloudflare"),
            ("MITRE sub-technique ID for C2 over web protocols? format: T****.***", "T1071.001"),
            ("MITRE sub-technique ID for persistence via cron? format: T****.***", "T1053.003"),
            ("What TLS version was used for the C2 beacon traffic? format: TLSx.X", "TLS1.2"),
            ("What is the JA3 fingerprint of the TLS Client Hello sent to the C2? (32 hex chars)", "20b279993ae2e137e62b9647c6d768fb"),
            ("How many TLS Client Hello packets were sent to the C2 during the capture? format: <integer>", "11"),
            ("At what relative timestamp (seconds, rounded to integer) did the first C2 beacon occur? format: <integer>", "3"),
            ("What ALPN protocol did the beacon negotiate with Cloudflare?", "h2"),
            ("What was the average interval between consecutive C2 beacons in the capture? format: <integer> seconds", "10"),
            ("Does the binary link against the system C library? yes / no", "yes"),
            ("How many numbered file descriptors (0, 1, 2, ...) did the payload have open?", "5"),
        ],
    },
}


for path, spec in TASKS.items():
    content = TEMPLATE
    content = content.replace("__QUESTIONS__", fmt_questions(spec["questions"]))
    content = content.replace("__BANNER__", spec["banner"])
    content = content.replace("__PORT__", spec["port"])
    with open(path, "w") as f:
        f.write(content)
    print(f"[+] wrote {path}")
