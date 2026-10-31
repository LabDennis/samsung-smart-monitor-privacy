#!/bin/sh
# M7 LS32BM700UUXEN / T-NKLBWWC-1720.7; run on the monitor.
set -eu
packages='com.samsung.tizen.samsung-analytics
com.samsung.tv.context-aware-agent
com.samsung.tv.context-aware-service
com.samsung.tv.tvplus
com.samsung.tv.tvPlusDeeplinker
com.samsung.tv.wakeup-engine-bixby
com.samsung.tv.wakeup-engine-alexa
com.samsung.tv.alexa-client
com.samsung.tv.bixby-prov
com.samsung.tv.mybixby
com.samsung.tv.bixbycapsuleviewer
com.samsung.tv.ondevice-voice
com.samsung.tv.farfieldvoice
com.samsung.tizen.smartthings-client
com.samsung.tv.smartthingsfind-daemon
com.samsung.tv.iot-hub-control
samsunghealth-service-tv'
if [ "$#" -ne 2 ] || [ "${1:-}" != --apply ] || [ "${2:-}" != LS32BM700UUXEN-1720.7 ]; then
 printf 'No changes. Packages selected for removal:\n%s\n' "$packages"
 echo 'Usage: sh scripts/debloat.sh --apply LS32BM700UUXEN-1720.7'
 exit 0
fi
[ "$(id -u)" = 0 ] || { echo 'Run on the rooted TV.' >&2; exit 1; }
[ -d /opt/usr/apps ] && [ -d /opt/usr/share/systemd/system ] || exit 1
umask 077
base=/opt/usr/share/smart-monitor-privacy
backup=$base/phase2
[ ! -L "$base" ] || { echo 'Refusing symlink backup directory.' >&2; exit 1; }
[ ! -e "$backup" ] && [ ! -L "$backup" ] || { echo 'Backup already exists; stopping.' >&2; exit 1; }
for package in $packages; do
 [ -d "/opt/usr/apps/$package" ] && [ ! -L "/opt/usr/apps/$package" ] || { echo "Missing or linked package directory: $package" >&2; exit 1; }
done
for package in com.samsung.tv.ondevice-voice com.samsung.tv.context-aware-agent com.samsung.tv.context-aware-service; do
 marker=/opt/usr/share/systemd/system/$package
 [ ! -L "$marker" ] || { echo "Refusing linked marker: $package" >&2; exit 1; }
done
mkdir -p "$base"
mkdir -m 700 "$backup"
pkgcmd -l > "$backup/packages-before.txt"
systemctl list-units --type=service --all --no-pager > "$backup/services-before.txt"
vconftool get db/menu/support/softwareupdate/autoupdate > "$backup/autoupdate-before.txt"
df -k /opt
# Finish and verify every archive before removing the first package.
for package in $packages; do
 tar -czf "$backup/$package.tar.gz" -C /opt/usr/apps "$package"
 tar -tzf "$backup/$package.tar.gz" >/dev/null
 sha256sum "$backup/$package.tar.gz" >> "$backup/SHA256SUMS"
done
for package in $packages; do
 log=$backup/$package-uninstall.log
 if ! pkgcmd -u -n "$package" > "$log" 2>&1; then
  cat "$log"; exit 1
 fi
 cat "$log"
 grep -F "pkgid[$package] key[end] val[ok]" "$log" >/dev/null || { echo "Unconfirmed removal: $package; stopping." >&2; exit 1; }
done
for package in com.samsung.tv.ondevice-voice com.samsung.tv.context-aware-agent com.samsung.tv.context-aware-service; do
 marker=/opt/usr/share/systemd/system/$package
 if [ ! -e "$marker" ]; then
  (set -C; : > "$marker")
  printf '%s\n' "$marker" >> "$backup/created-markers.txt"
 fi
done
systemctl stop --no-block com.samsung.tv.context-aware-agent.service com.samsung.tv.context-aware-service.service
systemctl reset-failed com.samsung.tv.ondevice-voice.service
pkgcmd -l > "$backup/packages-after.txt"
systemctl show com.samsung.tv.context-aware-agent.service com.samsung.tv.context-aware-service.service connman.service bluetooth-frwk-service.service btapp-service.service -p Id -p MainPID -p ActiveState
printf 'Package removal completed. Private backups: %s\n' "$backup"
