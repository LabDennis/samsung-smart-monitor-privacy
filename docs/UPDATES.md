# Disable automatic firmware updates

On the M7 LS32BM700UUXEN / T-NKLBWWC-1720.7, the firmware autoupdate preference is:

```text
db/menu/support/softwareupdate/autoupdate
```

In a root shell **on the monitor**, first read and save its current value privately:

```sh
vconftool get db/menu/support/softwareupdate/autoupdate
```

Disable automatic firmware updates, then read back the setting:

```sh
vconftool set -t int db/menu/support/softwareupdate/autoupdate 0
vconftool get db/menu/support/softwareupdate/autoupdate
```

Confirm the returned value is 0. If a command fails, do not assume the preference changed. Check again after reboot or a firmware change.

To undo, restore the integer value recorded before the change. If it was 1:

```sh
vconftool set -t int db/menu/support/softwareupdate/autoupdate 1
vconftool get db/menu/support/softwareupdate/autoupdate
```

This controls the automatic firmware update preference. It does not block firmware servers, manual installation, application updates or every possible update mechanism. No DNS blocklist or network firewall rules are installed. With autoupdate off, review and apply security updates manually.
