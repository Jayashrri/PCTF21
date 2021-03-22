case $- in
    *i*) ;;
    *) return;;
esac

if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

startshell() {
    if [ -z "$RBASH_ACTIVE" ]; then
        export RBASH_ACTIVE=true
        cd $HOME/jail
        rbash --noediting
        exit_code=$?
        export RBASH_ACTIVE=
    else
        return 0
    fi
    return $exit_code
}

ls() {
    if [[ "$@" == *"/"* ]] || [[ "$@" == *".."* ]]; then
        showonscreen "rbash: ls: restricted" 1>&2
        return 1
    else
        output=$(uncoversecrets --color=always "$@" 2>&1)
        exit_code=$?
        if [ $exit_code -eq 0 ]; then
            showonscreen "${output//uncoversecrets/ls}"
        else
            showonscreen "${output//uncoversecrets/ls}" 1>&2
        fi
    fi
    return $exit_code
}

cat() {
    if [[ "$@" == *"/"* ]] || [[ "$@" == *".."* ]]; then
        showonscreen "rbash: cat: restricted" 1>&2
        return 1
    else
        output=$(meowmeow "$@" 2>&1)
        exit_code=$?
        if [ $exit_code -eq 0 ]; then
            showonscreen "${output//meowmeow/cat}"
        else
            showonscreen "${output//meowmeow/cat}" 1>&2
        fi
    fi
    return $exit_code
}

file() {
    output=$(whatareyou "$@" 2>&1)
    exit_code=$?
    if [ $# -eq 0 ]; then
        showonscreen "${output//whatareyou/file}" 1>&2
    elif [ $# -eq 1 ]; then
        if [[ "$@" == "-"* ]] || [[ "$@" == *"/"* ]] || [[ "$@" == *".."* ]]; then
            showonscreen "rbash: file: restricted" 1>&2
            return 1
        else
            if [ $exit_code -eq 0 ]; then
                showonscreen "${output//whatareyou/file}"
            else
                showonscreen "${output//whatareyou/file}" 1>&2
            fi
        fi
    else
        showonscreen "rbash: file: restricted" 1>&2
        return 1
    fi
    return $exit_code
}

refuse() {
    showonscreen "rbash: $1: restricted" 1>&2
    return 1
}

export PATH=$HOME/commands
export PS1='${debian_chroot:+($debian_chroot)}\[\e[1;32m\]cobb@\h\[\e[1;00m\]:\[\e[1;36m\]\w\[\e[1;00m\]:\[\e[1;31m\]\$\[\e[00m\] '

readonly PATH
readonly PS1
readonly USER
readonly HOME
readonly SHELL

alias sudo='refuse sudo'
alias shopt='refuse shopt'
alias export='refuse export'
alias set='refuse set'
alias unset='refuse unset'
alias command='refuse command'
alias eval='refuse eval'
alias echo='refuse echo'
alias printf='refuse printf'
alias unalias='refuse unalias'
alias pwd='showonscreen "/home/cobb/jail"'
alias bash='startshell'
alias sh='startshell'

startshell

if [ -z "$RBASH_ACTIVE" ]; then
    exit 0
fi
