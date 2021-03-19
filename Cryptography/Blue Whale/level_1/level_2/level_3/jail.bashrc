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
        export RBASH_ACTIVE=
    fi
}

ls() {
    if [[ "$@" == *"/"* ]] || [[ "$@" == *".."* ]]; then
        showonscreen "rbash: ls: restricted"
    else
        output=$(uncoversecrets --color=always "$@" 2>&1)
        if [ $? -eq 0 ]; then
            showonscreen ${output//uncoversecrets/ls}
        else
            showonscreen ${output//uncoversecrets/ls} 1>&2
        fi
    fi
}

cat() {
    if [[ "$@" == *"/"* ]] || [[ "$@" == *".."* ]]; then
        showonscreen "rbash: cat: restricted"
    else
        output=$(meowmeow "$@" 2>&1)
        if [ $? -eq 0 ]; then
            showonscreen "${output//meowmeow/cat}"
        else
            showonscreen "${output//meowmeow/cat}" 1>&2
        fi
    fi
}

file() {
    output=$(whatareyou "$@" 2>&1)
    exit_code=$?
    if [ $# -eq 0 ]; then
        showonscreen "${output//whatareyou/file}" 1>&2
    elif [ $# -eq 1 ]; then
        if [[ "$@" == "-"* ]] || [[ "$@" == *"/"* ]] || [[ "$@" == *".."* ]]; then
            showonscreen "rbash: file: restricted"
        else
            if [ $exit_code -eq 0 ]; then
                showonscreen "${output//whatareyou/file}"
            else
                showonscreen "${output//whatareyou/file}" 1>&2
            fi
        fi
    else
        showonscreen "rbash: file: restricted"
    fi
}

export PATH=$HOME/commands
export PS1='${debian_chroot:+($debian_chroot)}\[\e[1;32m\]cobb@\h\[\e[1;00m\]:\[\e[1;36m\]\w\[\e[1;00m\]:\[\e[1;31m\]\$\[\e[00m\] '
alias sudo='showonscreen "rbash: sudo: restricted" 1>&2'
alias shopt='showonscreen "rbash: shopt: restricted" 1>&2'
alias export='showonscreen "rbash: export: restricted" 1>&2'
alias command='showonscreen "rbash: command: restricted" 1>&2'
alias pwd='showonscreen "/home/cobb/jail"'
alias echo='showonscreen "rbash: echo: restricted" 1>&2'
alias printf='showonscreen "rbash: printf: restricted" 1>&2'
alias bash='startshell'
alias sh='startshell'
startshell

if [ -z "$RBASH_ACTIVE" ]; then
    exit 0
fi