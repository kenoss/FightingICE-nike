RED=$(tput setaf 1);
GREEN=$(tput setaf 2);
RESET=$(tput sgr0);


function check_requirements {
    for r in $(echo "$1" | tr ' ' "\n"); do
        if type $r 2>&1 > /dev/null; then
            :
        else
            echo "${RED}error: requirements:${RESET} $1"
            exit 1
        fi
    done
}
