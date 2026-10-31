# Optional package removal

Target: **M7 LS32BM700UUXEN / T-NKLBWWC-1720.7**. Run only on the monitor in a root shell. Package removal is separate from service masking and firmware autoupdate control.

The script removes the listed packages for Samsung Analytics, Context Awareness, TV Plus, Bixby/Alexa and voice features, SmartThings and Samsung Health. Review the exact package names in [debloat.sh](../scripts/debloat.sh). Wi-Fi and Bluetooth packages are not in the removal list, but dependent features may still be affected.

## Preview and apply

Without the explicit arguments, no changes are made:

```sh
sh scripts/debloat.sh
```

After checking your model/firmware, reading the script and arranging a recovery path:

```sh
sh scripts/debloat.sh --apply LS32BM700UUXEN-1720.7
```

The model argument is an explicit acknowledgement, not automatic model detection. The script checks for a root shell and expected Tizen directories. It stops if its backup directory already exists, preventing an accidental rerun over the original backup.

Before removal, it records packages/services and archives the selected application directories under `/opt/usr/share/smart-monitor-privacy/phase2`. All archives are created before the first package removal. An absent package directory or failed archive aborts the operation. Keep sufficient free storage on `/opt` and copy backups to private storage.

**Directory archives are not complete reinstallable package backups.** There is no automatic package restoration. A failure partway through removal leaves already removed packages removed. Do not run this if you require a guaranteed one-command undo; use the temporary service masks instead.

The script also creates the selected service-suppression markers and stops the context-awareness services. Firmware autoupdate is configured separately using [UPDATES.md](UPDATES.md).

The commands are derived from this account's existing M7 procedure. This standalone version adds an explicit model acknowledgement and separates update control. Shell syntax and no-change invocation were checked locally; this version has not been reapplied to a monitor. Backups can contain private data and Samsung files: never upload them to GitHub.
