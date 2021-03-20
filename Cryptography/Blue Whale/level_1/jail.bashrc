case $- in
    *i*) ;;
    *) return;;
esac

if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

docker() {
    deny='rbash: docker: restricted'
    restrict='rbash: docker: user can execute only a shell'
    if [ $# -gt 0 ]; then
        case "$1" in
            "ps")
                karate /usr/bin/docker "$@"
                return $?;;
            "container")
                shift
                case "$1" in
                    "ls" | "ps" | "list")
                        karate /usr/bin/docker container "$@"
                        return $?;;
                    "exec")
                        shift
                        case "$1" in
                            "-it" | "-ti")
                                shift
                                if [ $# -eq 2 ]; then
                                    case "${@: -1}" in
                                        "bash" | "/bin/bash")
                                            karate /usr/bin/docker exec -u cobb -it "$@"
                                            return $?;;
                                        "sh" | "/bin/sh" | "rbash" | "/bin/rbash")
                                            set -- ${@:1:$#-1} "/bin/bash"
                                            karate /usr/bin/docker exec -u cobb -it "$@"
                                            return $?;;
                                        *)
                                            showonscreen $restrict 1>&2
                                            return 1;;
                                    esac
                                else
                                    showonscreen $deny 1>&2
                                    return 1
                                fi;;
                            "-i")
                                shift
                                if [ "$1" == "-t" ] && [ $# -eq 3 ]; then
                                    case "${@: -1}" in
                                        "bash" | "/bin/bash")
                                            karate /usr/bin/docker exec -u cobb -it "$@"
                                            return $?;;
                                        "sh" | "/bin/sh" | "rbash" | "/bin/rbash")
                                            set -- ${@:1:$#-1} "/bin/bash"
                                            karate /usr/bin/docker exec -u cobb -it "$@"
                                            return $?;;
                                        *)
                                            showonscreen $restrict 1>&2
                                            return 1;;
                                    esac
                                else
                                    showonscreen $deny 1>&2
                                    return 1
                                fi;;
                            "-t")
                                shift
                                if [ "$1" == "-i" ] && [ $# -eq 3 ]; then
                                    case "${@: -1}" in
                                        "bash" | "/bin/bash")
                                            karate /usr/bin/docker exec -u cobb -it "$@"
                                            return $?;;
                                        "sh" | "/bin/sh" | "rbash" | "/bin/rbash")
                                            set -- ${@:1:$#-1} "/bin/bash"
                                            karate /usr/bin/docker exec -u cobb -it "$@"
                                            return $?;;
                                        *)
                                            showonscreen $restrict 1>&2
                                            return 1;;
                                    esac
                                else
                                    showonscreen $deny 1>&2
                                    return 1
                                fi;;
                            *)
                                showonscreen $deny 1>&2
                                return 1;;
                        esac;;
                    *)
                        showonscreen $deny 1>&2
                        return 1;;
                esac;;
            "exec")
                shift
                case "$1" in
                    "-it" | "-ti")
                        shift
                        if [ $# -eq 2 ]; then
                            case "${@: -1}" in
                                "bash" | "/bin/bash")
                                    karate /usr/bin/docker exec -u cobb -it "$@"
                                    return $?;;
                                "sh" | "/bin/sh" | "rbash" | "/bin/rbash")
                                    set -- ${@:1:$#-1} "/bin/bash"
                                    karate /usr/bin/docker exec -u cobb -it "$@"
                                    return $?;;
                                *)
                                    showonscreen $restrict 1>&2
                                    return 1;;
                            esac
                        else
                            showonscreen $deny 1>&2
                            return 1
                        fi;;
                    "-i")
                        shift
                        if [ "$1" == "-t" ] && [ $# -eq 3 ]; then
                            case "${@: -1}" in
                                "bash" | "/bin/bash")
                                    karate /usr/bin/docker exec -u cobb -it "$@"
                                    return $?;;
                                "sh" | "/bin/sh" | "rbash" | "/bin/rbash")
                                    set -- ${@:1:$#-1} "/bin/bash"
                                    karate /usr/bin/docker exec -u cobb -it "$@"
                                    return $?;;
                                *)
                                    showonscreen $restrict 1>&2
                                    return 1;;
                            esac
                        else
                            showonscreen $deny 1>&2
                            return 1
                        fi;;
                    "-t")
                        shift
                        if [ "$1" == "-i" ] && [ $# -eq 3 ]; then
                            case "${@: -1}" in
                                "bash" | "/bin/bash")
                                    karate /usr/bin/docker exec -u cobb -it "$@"
                                    return $?;;
                                "sh" | "/bin/sh" | "rbash" | "/bin/rbash")
                                    set -- ${@:1:$#-1} "/bin/bash"
                                    karate /usr/bin/docker exec -u cobb -it "$@"
                                    return $?;;
                                *)
                                    showonscreen $restrict 1>&2
                                    return 1;;
                            esac
                        else
                            showonscreen $deny 1>&2
                            return 1
                        fi;;
                    *)
                        showonscreen $deny 1>&2
                        return 1;;
                esac;;
            *)
                showonscreen $deny 1>&2
                return 1;;
        esac
    else
        karate /usr/bin/docker
        return $?
    fi
}

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
alias pwd='showonscreen "/home/cobb/jail"'
alias bash='startshell'
alias sh='startshell'

startshell

if [ -z "$RBASH_ACTIVE" ]; then
    exit 0
fi
