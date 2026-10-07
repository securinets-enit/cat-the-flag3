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
	fmt.Println("\nHere is your flag:")
	fmt.Println(string(flagContent))
}
