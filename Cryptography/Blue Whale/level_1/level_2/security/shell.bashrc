case $- in
    *i*) ;;
      *) return;;
esac

shell() {
    if [ -z "$PYSHELL_ACTIVE" ]; then
        export PYSHELL_ACTIVE=true
        command $HOME/shell/main.py
        export PYSHELL_ACTIVE=
    fi
}

shell

if [ -z "$PYSHELL_ACTIVE" ]; then
    exit 0
fi
