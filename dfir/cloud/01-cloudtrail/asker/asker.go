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
		// Phase 1 — Identification
		{"What is the AWS account ID in the logs?", "379113716218"},
		{"What is the username of the compromised IAM user?", "samir.benali"},
		{"What is the access key ID used by the attacker?", "AKIAVQRHQHH5BBB7WXZ6"},

		// Phase 2 — Attribution
		{"What is the source IP of the attacker's requests?", "196.203.130.8"},
		{"At what UTC time did the first malicious API call occur? Format: YYYY-MM-DDTHH:MM:SSZ", "2026-10-07T10:27:22Z"},
		{"What is the first API call made by the attacker?", "GetCallerIdentity"},

		// Phase 3 — Enumeration and escalation
		{"What role did the attacker assume? (name only)", "OrganizationAccountAccessRole"},
		{"What is the ARN of the assumed role session?", "arn:aws:sts::379113716218:assumed-role/OrganizationAccountAccessRole/attacker-session-2026"},
		{"What role session name did the attacker use?", "attacker-session-2026"},
		{"What role did the attacker use to escalate privileges? (full ARN)", "arn:aws:iam::379113716218:role/OrganizationAccountAccessRole"},

		// Phase 4 — Cover-up and persistence
		{"What API call did the attacker use to attempt to hide their tracks?", "StopLogging"},
		{"What is the name of the trail the attacker tried to disable?", "management-events"},
		{"What API call did the attacker use to create a backdoor key?", "CreateAccessKey"},
		{"What is the name of the user the attacker backdoored?", "backup-service"},
		{"What is the access key ID created for the backdoor user?", "AKIAVQRHQHH5G2ZCYGFC"},

		// Phase 5 — Timeline
		{"How many seconds elapsed between the first and last attack event? (integer)", "56"},
		{"What is the last event timestamp of the attack? Format: YYYY-MM-DDTHH:MM:SSZ", "2026-10-07T10:28:18Z"},
	}

	reader := bufio.NewReader(os.Stdin)

	fmt.Print(bannerHeader)
	fmt.Println("Hello future Threat Hunter. This is a cloud forensics challenge.")
	fmt.Println("You have a CloudTrail log from a compromised AWS account.")
	fmt.Println("Read it, then answer the questions.")
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

const bannerHeader = "\n\u001b[1m\u001b[31m   ▄▄▄    ▄▄  ▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄ ▄    ▄ ▄▄▄▄▄▄\u001b[0m   \u001b[36m  |~~~~~~~~~|\u001b[0m\n\u001b[1m\u001b[31m ▄▀   ▀   ██     █             █    █    █ █     \u001b[0m   \u001b[36m  |  ENIT   |\u001b[0m\n\u001b[1m\u001b[31m █       █  █    █             █    █▄▄▄▄█ █▄▄▄▄▄\u001b[0m   \u001b[36m  |~~~~~~~~~|\u001b[0m\n\u001b[1m\u001b[31m █       █▄▄█    █             █    █    █ █     \u001b[0m   \u001b[36m  |\u001b[0m\n\u001b[1m\u001b[31m  ▀▄▄▄▀ █    █   █             █    █    █ █▄▄▄▄▄\u001b[0m   \u001b[36m  |   /\\_/\\\u001b[0m\n\u001b[1m\u001b[31m ▄▄▄▄▄▄ ▄        ▄▄     ▄▄▄                 ▄▄▄▄ \u001b[0m   \u001b[36m  |__( o.o )\u001b[0m\n\u001b[1m\u001b[31m █      █        ██   ▄▀   ▀        ▄   ▄  ▀   ▀█\u001b[0m   \u001b[36m  |    > ^ <\u001b[0m\n\u001b[1m\u001b[31m █▄▄▄▄▄ █       █  █  █   ▄▄        ▀▄ ▄▀    ▄▄▄▀\u001b[0m   \u001b[36m  |   /     \\\u001b[0m\n\u001b[1m\u001b[31m █      █       █▄▄█  █    █         █▄█       ▀█\u001b[0m   \u001b[36m  |  (_|   |_)\u001b[0m\n\u001b[1m\u001b[31m █      █▄▄▄▄▄ █    █  ▀▄▄▄▀          █    ▀▄▄▄█▀\u001b[0m   \u001b[36m~~^~~~~~~~~~~~~~\u001b[0m\n\n\u001b[32m╔════════════════════════════════════════════════════════════════════════╗\u001b[0m\n\u001b[32m║\u001b[0m\u001b[35m\u001b[1m                  Securinets ENIT  //  DFIR  //  Cloud                  \u001b[0m\u001b[32m║\u001b[0m\n\u001b[32m╠════════════════════════════════════════════════════════════════════════╣\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mChallenge  \u001b[0m\u001b[33m\u001b[1mLeaked AWS Key\u001b[0m                                             \u001b[32m║\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mDifficulty \u001b[0m\u001b[33m\u001b[1mMedium\u001b[0m                                                     \u001b[32m║\u001b[0m\n\u001b[32m║\u001b[0m  \u001b[2mAuthor     \u001b[0m\u001b[36m\u001b[1mTaha\u001b[0m                                                       \u001b[32m║\u001b[0m\n\u001b[32m╚════════════════════════════════════════════════════════════════════════╝\u001b[0m\n\n"

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
