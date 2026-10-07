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

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hello future Threat Hunter. This is a dropper analysis challenge.")
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
