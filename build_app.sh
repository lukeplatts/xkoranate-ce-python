#!/bin/sh
# Build the frozen app: dist/xkoranate.app (macOS) or dist/xkoranate/ (Linux).
set -e
cd "$(dirname "$0")"
.venv/bin/pyinstaller --noconfirm xkoranate.spec

# Wrap the real executable in a launcher script that tees its output to a
# persistent log file. This is the only way to capture a crash that happens
# before Python itself starts (e.g. the OS's glibc being too old to load the
# bundled Python — see xkoranate/crashlog.py for crashes after that point):
# nothing in the app's own code can run yet, so nothing but the wrapper can
# record what went wrong. Renaming the real binary is safe — PyInstaller's
# onedir bootloader locates its bundled data by the directory it's running
# from, not by its own filename.
writeWrapper() {
    binDir="$1"
    realBin="$2"
    wrapperPath="$binDir/xkoranate"
    mv "$binDir/$realBin" "$binDir/xkoranate-bin"
    cat > "$wrapperPath" <<'WRAPPER'
#!/bin/bash
# xkoranate launcher — see xkoranate/crashlog.py for why this exists.
dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "$(uname -s)" in
    Darwin) logDir="$HOME/Library/Logs/xkoranate/logs" ;;
    *)      logDir="${XDG_STATE_HOME:-$HOME/.local/state}/xkoranate/logs" ;;
esac
mkdir -p "$logDir" 2>/dev/null || logDir="/tmp"
logFile="$logDir/launch.log"
set -o pipefail
"$dir/xkoranate-bin" "$@" 2>&1 | tee "$logFile"
status=$?
if [ $status -ne 0 ]; then
    echo "" >&2
    echo "xkoranate exited with an error (code $status)." >&2
    echo "Details were saved to: $logFile" >&2
    echo "Please attach that file if you report this issue." >&2
fi
exit $status
WRAPPER
    chmod +x "$wrapperPath"
}

case "$(uname -s)" in
    Darwin)
        writeWrapper "dist/xkoranate.app/Contents/MacOS" "xkoranate"
        echo "Built: $(pwd)/dist/xkoranate.app"
        ;;
    *)
        writeWrapper "dist/xkoranate" "xkoranate"
        echo "Built: $(pwd)/dist/xkoranate/xkoranate"
        ;;
esac
