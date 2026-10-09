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
	fmt.Println("\nHere is your flag:")
	fmt.Println(string(flagContent))
}
