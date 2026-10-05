#!/bin/bash
# Docker Basics — interactive tutorial entrypoint
# Author: 7ankalis — Securinets ENIT

C_RESET='\033[0m'
C_BOLD='\033[1m'
C_CYAN='\033[0;36m'
C_GREEN='\033[0;32m'
C_YELLOW='\033[1;33m'
C_DIM='\033[2m'

banner() {
    echo
    echo -e "${C_CYAN}  ==============================================================${C_RESET}"
    echo -e "${C_CYAN}  |                                                            |${C_RESET}"
    echo -e "${C_CYAN}  |   ${C_BOLD}Docker Basics - Interactive Tutorial${C_RESET}${C_CYAN}                     |${C_RESET}"
    echo -e "${C_CYAN}  |                                                            |${C_RESET}"
    echo -e "${C_CYAN}  |   Securinets ENIT                                          |${C_RESET}"
    echo -e "${C_CYAN}  |   Author: 7ankalis                                         |${C_RESET}"
    echo -e "${C_CYAN}  |                                                            |${C_RESET}"
    echo -e "${C_CYAN}  |   Three flags are hidden in this container.                |${C_RESET}"
    echo -e "${C_CYAN}  |   Follow the prompts to find them.                         |${C_RESET}"
    echo -e "${C_CYAN}  |                                                            |${C_RESET}"
    echo -e "${C_CYAN}  |   Type 'hint' for a nudge, 'skip' to move on.              |${C_RESET}"
    echo -e "${C_CYAN}  |                                                            |${C_RESET}"
    echo -e "${C_CYAN}  ==============================================================${C_RESET}"
    echo
}

step_header() {
    echo
    echo -e "${C_BOLD}[$1/5] $2${C_RESET}"
    echo -e "${C_DIM}------------------------------------------------------------${C_RESET}"
    echo
}

prompt() {
    local expected="$1"
    local hint="$2"

    while true; do
        printf "${C_YELLOW}Your command:${C_RESET} "
        read -r answer || exit 0
        answer="$(echo "$answer" | tr -d '[:space:]')"

        if [ "$answer" = "hint" ]; then
            echo -e "${C_DIM}Hint: $hint${C_RESET}"
            continue
        fi
        if [ "$answer" = "skip" ]; then
            return 0
        fi
        if [ "$answer" = "exit" ]; then
            echo -e "${C_DIM}Exiting. See you in Task 2.${C_RESET}"
            exit 0
        fi
        if [ "$answer" = "$expected" ]; then
            return 0
        fi
        echo -e "${C_DIM}Not quite. Try '$expected' - or type 'hint'.${C_RESET}"
    done
}

banner

# Step 1 — list files
step_header 1 "Listing files"
echo "The current directory is /tutorial. List its contents."
echo
echo -e "${C_DIM}    ls${C_RESET}"
echo
prompt "ls" "Just type: ls"
ls
echo
echo -e "${C_GREEN}Correct.${C_RESET}"
echo "Files in a container are just files in the image's filesystem."
echo "But some files are hidden."

# Step 2 — show hidden files
step_header 2 "Hidden files"
echo "To see hidden files, add the -a flag to ls:"
echo
echo -e "${C_DIM}    ls -la${C_RESET}"
echo
prompt "ls-la" "Try: ls -la"
ls -la
echo
echo -e "${C_GREEN}Correct.${C_RESET}"
echo "Files starting with '.' are hidden by default."

# Step 3 — read the hidden file (FLAG 1)
step_header 3 "Read the hidden file"
echo "There's a file named .hidden_flag. Read it:"
echo
echo -e "${C_DIM}    cat .hidden_flag${C_RESET}"
echo
prompt "cat.hidden_flag" "Try: cat .hidden_flag"
cat /tutorial/.hidden_flag
echo
echo -e "${C_GREEN}That's your first flag.${C_RESET}"

# Step 4 — environment variables (FLAG 2)
step_header 4 "Environment variables"
echo "Containers have their own environment. Print all env vars:"
echo
echo -e "${C_DIM}    env${C_RESET}"
echo
prompt "env" "Try: env"
env | sort
echo
echo -e "${C_GREEN}Look closely - one of those values is not like the others.${C_RESET}"
echo -e "${C_GREEN}That's your second flag.${C_RESET}"

# Step 5 — exit and inspect (FLAG 3)
step_header 5 "Inside vs outside the container"
echo "The third flag is not inside the container. It's a property of"
echo "the image itself."
echo
echo "Exit this container with:"
echo
echo -e "${C_DIM}    exit${C_RESET}"
echo
echo "Then from your host, run:"
echo
echo -e "${C_DIM}    docker inspect sitaha/docker-basics:1.0${C_RESET}"
echo
echo "Look at the image's Labels."
echo
prompt "exit" "Type: exit"
echo
echo -e "${C_GREEN}Good. Now inspect the image from your host.${C_RESET}"
echo
echo "Summary of what you found:"
echo "  Flag 1 - in /tutorial/.hidden_flag"
echo "  Flag 2 - in the FLAG2 environment variable"
echo "  Flag 3 - in the image label 'flag'"
echo
echo -e "${C_BOLD}Securinets ENIT - Docker Basics${C_RESET}"
echo -e "${C_DIM}Author: 7ankalis${C_RESET}"
echo
exit 0
