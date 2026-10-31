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

This packaged version has not been reapplied to a monitor. Backups can contain
private data and Samsung files; keep them out of public repositories.

## Logs and checks

The no-change invocation prints the exact package list. Every directory is
checked before backup. Archive hashes are saved in `SHA256SUMS`; each uninstall
has its own private log and must report the expected successful callback.
An exit code alone is insufficient. Newly created suppression markers are
recorded in `created-markers.txt`. They persist across reboot; removing one
does not reinstall its package. Review [the verification record](VERIFICATION.md)
and [package list](PACKAGES.md). Never rerun by deleting the original backup.

Service stops are queued with `--no-block`.
The final state output can still show a transition; inspect the two
context-aware units again until inactive. Script completion confirms the
package callbacks, not completion of asynchronous systemd stop jobs.
