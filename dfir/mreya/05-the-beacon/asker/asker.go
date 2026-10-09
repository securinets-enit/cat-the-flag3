package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type question struct {
	text   string
	answer string
}

func main() {
	questions := []question{
		// ---- Phase 0: Triage (6) ----
		{"How many IPv4 endpoints appear in the capture? (integer)", "50"},
		{"What is the IPv4 address of the workstation under investigation?", "192.168.1.141"},
		{"What is the dominant external IPv4 address the workstation communicates with?", "34.170.160.245"},
		{"Which transport protocol accounts for the most bytes in the capture? (tcp / udp)", "tcp"},
		{"Is the SSH traffic in this capture part of the compromise or admin activity? (admin / compromise)", "admin"},
		{"Which domain appears most frequently in the TLS SNI list?", "gh-actions-runner.xyz"},

		// ---- Phase 1: Identify the beacon (5) ----
		{"What is the domain name seen in the TLS SNI of the beacon traffic?", "gh-actions-runner.xyz"},
		{"What remote port does the beacon use? (integer)", "443"},
		{"Which transport-layer protocol does the beacon use? (tcp / udp)", "tcp"},
		{"How many TLS Client Hello packets does the workstation send to the beacon domain during the capture? (integer)", "9"},
		{"What is the approximate beacon interval in seconds? (integer, round to nearest whole)", "10"},

		// ---- Phase 2: Distinguish beacon from browsing (5) ----
		{"Does the interval pattern suggest automated or human activity? (automated / human)", "automated"},
		{"Is the byte-volume-per-beacon consistent with web browsing or with a heartbeat? (browsing / heartbeat)", "heartbeat"},
		{"How many distinct domains appear in the TLS SNI list across the whole capture? (integer)", "12"},
		{"Which of the SNI domains is not a well-known legitimate service?", "gh-actions-runner.xyz"},
		{"Is the beacon domain fronted by a CDN? (yes / no)", "yes"},

		// ---- Phase 3: TLS deep dive (5) ----
		{"What TLS version did the beacon negotiate? format: TLSx.X", "TLS1.3"},
		{"What is the JA3 fingerprint of the beacon's Client Hello? (32 hex chars)", "20b279993ae2e137e62b9647c6d768fb"},
		{"What is the negotiated cipher suite? (IANA name, uppercase, format TLS_AES_128_GCM_SHA256)", "TLS_AES_128_GCM_SHA256"},
		{"What is the CN (Common Name) of the leaf certificate presented by the beacon server?", "gh-actions-runner.xyz"},
		{"What is the CN (Common Name) of the intermediate CA that issued the leaf certificate?", "WE1"},

		// ---- Phase 4: Attribution (5) ----
		{"What is the top-level domain of the beacon domain? (include the leading dot)", ".xyz"},
		{"Is the beacon domain owned by GitHub? (yes / no)", "no"},
		{"Which CDN provider fronts the beacon domain? (single word, lowercase)", "cloudflare"},
		{"Which organization is the issuer of the beacon's certificate? (organization field, lowercase)", "google trust services"},
		{"Why is a valid TLS certificate NOT evidence that a server is legitimate? (short phrase, lowercase)", "anyone can get one"},

		// ---- Phase 5: Beacon timing (4) ----
		{"At what relative timestamp (seconds, integer) does the first real beacon occur?", "20"},
		{"At what relative timestamp (seconds, integer) does the last beacon occur?", "73"},
		{"What is the longest gap between consecutive beacons in seconds? (integer)", "13"},
		{"What is the shortest gap between consecutive beacons in seconds? (integer)", "9"},

		// ---- Phase 6: Noise filtering (5) ----
		{"Which file-transfer protocol is NOT present in the capture? (SMB / FTP / SCP — one word, uppercase)", "smb"},
		{"Which instant-messaging network appears in the traffic? (single word, lowercase)", "telegram"},
		{"Are any .ru domains present in the TLS SNI list? (yes / no)", "no"},
		{"How many QUIC frames are in the capture? (integer)", "320"},
		{"Which Cloudflare-owned IP in the 188.114.x.x range appears in the endpoints list? (IP address)", "188.114.96.6"},

		// ---- Phase 7: MITRE mapping (4) ----
		{"MITRE sub-technique ID for C2 over web protocols? format: T****.***", "T1071.001"},
		{"MITRE tactic ID for Command and Control? format: TA****", "TA0011"},
		{"MITRE sub-technique ID for Application Layer Protocol: DNS? format: T****.***", "T1071.004"},
		{"MITRE technique ID for Encrypted Channel? format: T****", "T1573"},
	}

	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hello future Threat Hunter. This is a network forensics challenge.")
	fmt.Println("You have a packet capture from a suspicious workstation. Filter the noise, identify the beacon, and answer the questions.")
	fmt.Println("You have 3 attempts for each question.")
	fmt.Println("-----------------------------------------------------")

	for i, q := range questions {
		incorrectAttempts := 0
		for {
			fmt.Printf("\nQuestion %d/%d: %s\n", i+1, len(questions), q.text)
			fmt.Print("Your Answer: ")
			input, _ := reader.ReadString('\n')
			input = strings.TrimSpace(input)

			if strings.EqualFold(input, q.answer) {
				fmt.Println("Correct! ✅")
				break
			} else {
				incorrectAttempts++
				if incorrectAttempts >= 3 {
					fmt.Println("Incorrect. ❌ You have exceeded the maximum number of attempts for this question. The quiz is over.")
					return
				}
				fmt.Printf("Incorrect. ❌ You have %d attempts remaining for this question.\n", 3-incorrectAttempts)
			}
		}
	}

	fmt.Println("\nExcellent work, hunter! 🕵️‍♂️")
	fmt.Println("Aw l flag")

	flagContent, err := os.ReadFile("flag.txt")
	if err != nil {
		fmt.Println("Error reading flag.txt:", err)
		return
	}
	fmt.Println("\nHere is your flag:")
	fmt.Println(string(flagContent))
}
