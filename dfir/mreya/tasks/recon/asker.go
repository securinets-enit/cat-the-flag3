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

var questions = []question{
	{"When was cdnjs-mirror.net first registered? (YYYY-MM-DD)", "2026-04-30"},
	{"Which registrar manages cdnjs-mirror.net? (single word, lowercase)", "godaddy"},
	{"Authoritative nameservers — comma-separated, alphabetical, lowercase, no trailing dots", "carl.ns.cloudflare.com,ivy.ns.cloudflare.com"},
	{"Current A records for cdnjs-mirror.net — comma-separated, ascending", "104.21.95.116,172.67.144.188"},
	{"Which organization owns those IPs? (single word, lowercase)", "cloudflare"},
	{"TLS certificate — Common Name (CN) of the ISSUER", "ye1"},
	{"TLS certificate — Organization (O) of the ISSUER (lowercase, no spaces, no apostrophe)", "letsencrypt"},
	{"TLS certificate — date issued (YYYY-MM-DD)", "2026-09-16"},
	{"TLS certificate — date of expiry (YYYY-MM-DD)", "2026-12-15"},
	{"Approximate certificate lifetime in days (integer, round to nearest 5)", "90"},
	{"Subject Alternative Names — comma-separated, alphabetical, lowercase, strip the DNS: prefix", "*.cdnjs-mirror.net,cdnjs-mirror.net"},
	{"SHA-256 fingerprint of the certificate — lowercase hex, no colons", "a3f54b3a3cf50036d8448e6b26c6ef71f14bae603e5f7f7d6bd318f3cf89d8dd"},
	{"Palo Alto category — vertical / subcategory, lowercase", "technology / web & hosting"},
	{"Overall assessment — one of [legitimate, abandoned, suspicious, cdn]", "suspicious"},
}

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hello future Threat Hunter. This is a domain reconnaissance challenge.")
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
