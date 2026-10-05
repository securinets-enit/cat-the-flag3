package main

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

func handleConn(conn net.Conn) {
	defer conn.Close()
	w := bufio.NewWriter(conn)
	r := bufio.NewReader(conn)
	defer w.Flush()

	fmt.Fprintln(w, "Hello future Threat Hunter. This is a domain reconnaissance challenge.")
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
	ln, err := net.Listen("tcp", "0.0.0.0:9999")
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
