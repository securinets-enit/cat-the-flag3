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
	{"What is the name of the second-stage binary that the installer downloads? format: <filename>", "gh-completion"},
	{"What tool does the installer use to fetch the second-stage payload?", "curl"},
	{"What full URL does the installer request? format: <url>", "https://cdnjs-mirror.net/assets/gh-2.42.1-shell-helper.bin?build=75efb0959defbc4b1bdcc6247381b437"},
	{"What is the value of the _BUILD variable? format: <hex>", "75efb0959defbc4b1bdcc6247381b437"},
	{"What HTTP query parameter carries the build identifier?", "build"},
	{"Where on disk does the second-stage binary get saved? format: ~/<path>", "~/.local/share/gh-cli/gh-completion"},
	{"What scheduler does the installer use for persistence?", "cron"},
	{"What cron schedule re-executes the payload? format: 5-field cron", "*/30 * * * *"},
	{"What cron keyword triggers execution at boot?", "@reboot"},
	{"What command writes the cron entries?", "crontab"},
	{"What utility detaches the payload from the parent process so it survives logout?", "nohup"},
	{"In one short phrase, what is the purpose of '2>/dev/null || true' at the end of the curl line?", "suppress errors"},
}

func handleConn(conn net.Conn) {
	defer conn.Close()
	w := bufio.NewWriter(conn)
	r := bufio.NewReader(conn)
	defer w.Flush()

	fmt.Fprintln(w, "Hello future Threat Hunter. This is a dropper analysis challenge.")
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
	ln, err := net.Listen("tcp", "0.0.0.0:9998")
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
