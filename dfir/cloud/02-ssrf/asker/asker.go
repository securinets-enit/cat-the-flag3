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
	// Phase 1 — Application (3)
	{"What is the public IP of the vulnerable web application?", "98.87.168.89"},
	{"What is the vulnerable endpoint path? (start with /)", "/preview"},
	{"What is the query parameter that carries the target URL?", "url"},

	// Phase 2 — SSRF discovery (3)
	{"What is the source IP of the attacker in the web access log?", "154.108.154.113"},
	{"What is the User-Agent of the attacker's requests?", "curl/8.5.0"},
	{"What URL scheme did the app explicitly block? (single word)", "file"},

	// Phase 3 — IMDS exploitation (4)
	{"What IP address was the SSRF target? (metadata service)", "169.254.169.254"},
	{"What is the name of the IAM role attached to the EC2 instance?", "webapp-preview-role"},
	{"What is the AccessKeyId extracted from IMDS? (starts with ASIA)", "ASIAVQRHQHH5IDT6H2UK"},
	{"What IMDS version was enabled on the instance? (v1 or v2)", "v1"},

	// Phase 4 — Credential abuse (3)
	{"What is the first AWS API call made with the stolen credentials?", "GetCallerIdentity"},
	{"What is the second AWS API call made with the stolen credentials?", "ListBuckets"},
	{"What is the ARN of the assumed-role session?", "arn:aws:sts::379113716218:assumed-role/webapp-preview-role/i-0a00ce44211fc98ae"},

	// Phase 5 — EC2 instance identification (2)
	{"What is the EC2 instance ID embedded in the role session?", "i-0a00ce44211fc98ae"},
	{"How many events did the attacker generate in CloudTrail?", "2"},
}

func main() {
	reader := bufio.NewReader(os.Stdin)

	fmt.Print(bannerHeader)
	fmt.Println("Hello future Threat Hunter. This is an SSRF-to-IMDS cloud challenge.")
	fmt.Println("You have a web access log and CloudTrail events.")
	fmt.Println("Reconstruct the attack, then answer the questions.")
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

const bannerHeader = "\n\u001b[1m\u001b[31m   ▄▄▄    ▄▄  ▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄ ▄    ▄ ▄▄▄▄▄▄\u001b[0m   \u001b[36m  |~~~~~~~~~|\u001b[0m\n\u001b[1m\u001b[31m ▄▀   ▀   ██     █             █    █    █ █     \u001b[0m   \u001b[36m  |  ENIT   |\u001b[0m\n\u001b[1m\u001b[31m █       █  █    █             █    █▄▄▄▄█ █▄▄▄▄▄\u001b[0m   \u001b[36m  |~~~~~~~~~|\u001b[0m\n\u001b[1m\u001b[31m █       █▄▄█    █             █    █    █ █     \u001b[0m   \u001b[36m  |\u001b[0m\n\u001b[1m\u001b[31m  ▀▄▄▄▀ █    █   █             █    █    █ █▄▄▄▄▄\u001b[0m   \u001b[36m  |   /\\_/\\\u001b[0m\n\u001b[1m\u001b[31m ▄▄▄▄▄▄ ▄        ▄▄     ▄▄▄                 ▄▄▄▄ \u001b[0m   \u001b[36m  |__( o.o )\u001b[0m\n\u001b[1m\u001b[31m █      █        ██   ▄▀   ▀        ▄   ▄  ▀   ▀█\u001b[0m   \u001b[36m  |    > ^ <\u001b[0m\n\u001b[1m\u001b[31m █▄▄▄▄▄ █       █  █  █   ▄▄        ▀▄ ▄▀    ▄▄▄▀\u001b[0m   \u001b[36m  |   /     \\\u001b[0m\n\u001b[1m\u001b[31m █      █       █▄▄█  █    █         █▄█       ▀█\u001b[0m   \u001b[36m  |  (_|   |_)\u001b[0m\n\u001b[1m\u001b[31m █      █▄▄▄▄▄ █    █  ▀▄▄▄▀          █    ▀▄▄▄█▀\u001b[0m   \u001b[36m~~^~~~~~~~~~~~~~\u001b[0m\n\n\u001b[32m╔════════════════════════════════════════════════════════════════════════╗\u001b[0m\n\u001b[32m║\u001b[0m\u001b[35m\u001b[1m                  Securinets ENIT  //  DFIR  //  Cloud                  \u001b[0m\u001b[32m║\u001b[0m\n\u001b[32m╠════════════════════════════════════════════════════════════════════════╣\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mChallenge  \u001b[0m\u001b[33m\u001b[1mSSRF to IMDS\u001b[0m                                               \u001b[32m║\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mDifficulty \u001b[0m\u001b[33m\u001b[1mMedium\u001b[0m                                                     \u001b[32m║\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mAuthor     \u001b[0m\u001b[36m\u001b[1mTaha\u001b[0m                                                       \u001b[32m║\u001b[0m\n\u001b[32m╚════════════════════════════════════════════════════════════════════════╝\u001b[0m\n\n"

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
