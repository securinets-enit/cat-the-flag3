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
	{"What is the file format of the artifact?", "elf"},
	{"What is the target architecture? format: <arch>-<bits>", "x86-64"},
	{"Is the binary stripped of symbols?", "yes"},
	{"What is the exact byte size of the binary?", "19969992"},
	{"What is the MD5 hash of the binary?", "afad825988139b2ab9a72611d4717ce5"},
	{"What is the SHA-256 hash of the binary?", "13352c0c87c485a1616d6bde5037005cd4f68249f5061d51273a2f8af5403f93"},
	{"Which user owns the binary?", "root"},
	{"What is the file permission mode in octal? format: 0XXX", "0755"},
	{"What was the PID of the payload?", "2552"},
	{"What was the parent PID of the payload? format: <integer>", "1"},
	{"What was the working directory of the process at execution?", "/tmp/gh-extract/gh_2.42.1_linux_amd64"},
	{"What is the absolute path of the payload executable?", "/root/.local/share/gh-cli/gh-completion"},
	{"How many cron entries did the installer create? format: <integer>", "2"},
	{"What is the periodic schedule that re-executes the payload? format: 5-field cron", "*/30 * * * *"},
	{"What cron keyword triggers execution at boot?", "@reboot"},
	{"What is the delivery domain?", "cdnjs-mirror.net"},
	{"What is the C2 domain as seen in the TLS SNI?", "gh-actions-runner.xyz"},
	{"What is the C2 port?", "443"},
	{"What is the approximate beacon interval in seconds? format: <integer>", "10"},
	{"Which CDN provider fronts the C2 domain?", "cloudflare"},
	{"MITRE sub-technique ID for C2 over web protocols? format: T****.***", "T1071.001"},
	{"MITRE sub-technique ID for persistence via cron? format: T****.***", "T1053.003"},
	{"What TLS version was used for the C2 beacon traffic? format: TLSx.X", "TLS1.2"},
	{"What is the JA3 fingerprint of the TLS Client Hello sent to the C2? (32 hex chars)", "20b279993ae2e137e62b9647c6d768fb"},
	{"How many TLS Client Hello packets were sent to the C2 during the capture? format: <integer>", "11"},
	{"At what relative timestamp (seconds, rounded to integer) did the first C2 beacon occur? format: <integer>", "3"},
	{"What ALPN protocol did the beacon negotiate with Cloudflare?", "h2"},
	{"What was the average interval between consecutive C2 beacons in the capture? format: <integer> seconds", "10"},
	{"Does the binary link against the system C library? yes / no", "yes"},
	{"How many numbered file descriptors (0, 1, 2, ...) did the payload have open?", "5"},
}

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Print(bannerHeader)
	fmt.Println("Hello future Threat Hunter. This is a payload analysis challenge.")
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
	printFlag(strings.TrimSpace(string(flagContent)))
}

// --- BEGIN GENERATED BANNER (tools/banner.py) ---

const bannerHeader = "\n\u001b[1m\u001b[31m   ▄▄▄    ▄▄  ▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄ ▄    ▄ ▄▄▄▄▄▄\u001b[0m   \u001b[36m  |~~~~~~~~~|\u001b[0m\n\u001b[1m\u001b[31m ▄▀   ▀   ██     █             █    █    █ █     \u001b[0m   \u001b[36m  |  ENIT   |\u001b[0m\n\u001b[1m\u001b[31m █       █  █    █             █    █▄▄▄▄█ █▄▄▄▄▄\u001b[0m   \u001b[36m  |~~~~~~~~~|\u001b[0m\n\u001b[1m\u001b[31m █       █▄▄█    █             █    █    █ █     \u001b[0m   \u001b[36m  |\u001b[0m\n\u001b[1m\u001b[31m  ▀▄▄▄▀ █    █   █             █    █    █ █▄▄▄▄▄\u001b[0m   \u001b[36m  |   /\\_/\\\u001b[0m\n\u001b[1m\u001b[31m ▄▄▄▄▄▄ ▄        ▄▄     ▄▄▄                 ▄▄▄▄ \u001b[0m   \u001b[36m  |__( o.o )\u001b[0m\n\u001b[1m\u001b[31m █      █        ██   ▄▀   ▀        ▄   ▄  ▀   ▀█\u001b[0m   \u001b[36m  |    > ^ <\u001b[0m\n\u001b[1m\u001b[31m █▄▄▄▄▄ █       █  █  █   ▄▄        ▀▄ ▄▀    ▄▄▄▀\u001b[0m   \u001b[36m  |   /     \\\u001b[0m\n\u001b[1m\u001b[31m █      █       █▄▄█  █    █         █▄█       ▀█\u001b[0m   \u001b[36m  |  (_|   |_)\u001b[0m\n\u001b[1m\u001b[31m █      █▄▄▄▄▄ █    █  ▀▄▄▄▀          █    ▀▄▄▄█▀\u001b[0m   \u001b[36m~~^~~~~~~~~~~~~~\u001b[0m\n\n\u001b[32m╔════════════════════════════════════════════════════════════════════════╗\u001b[0m\n\u001b[32m║\u001b[0m\u001b[35m\u001b[1m                  Securinets ENIT  //  DFIR  //  Mreya                  \u001b[0m\u001b[32m║\u001b[0m\n\u001b[32m╠════════════════════════════════════════════════════════════════════════╣\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mChallenge  \u001b[0m\u001b[33m\u001b[1mThe Implant\u001b[0m                                                \u001b[32m║\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mDifficulty \u001b[0m\u001b[31m\u001b[1mHard\u001b[0m                                                       \u001b[32m║\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mAuthor     \u001b[0m\u001b[36m\u001b[1mTaha\u001b[0m                                                       \u001b[32m║\u001b[0m\n\u001b[32m╚════════════════════════════════════════════════════════════════════════╝\u001b[0m\n\n"

// printFlag shows the flag inside a box matching the header's style.
func printFlag(flag string) {
	const green, yellow, bold, reset = "\x1b[32m", "\x1b[33m", "\x1b[1m", "\x1b[0m"
	inner := len([]rune(flag)) + 6
	label := " Here is your flag "
	fill := inner - 2 - len(label)
	if fill < 0 {
		fill = 0
	}
	fmt.Println()
	fmt.Println(green + "╔══" + label + strings.Repeat("═", fill) + "╗" + reset)
	fmt.Println(green + "║" + reset + "   " + yellow + bold + flag + reset + "   " + green + "║" + reset)
	fmt.Println(green + "╚" + strings.Repeat("═", inner) + "╝" + reset)
	fmt.Println("   Securinets ENIT // Cat the Flag v3")
}

// --- END GENERATED BANNER ---
