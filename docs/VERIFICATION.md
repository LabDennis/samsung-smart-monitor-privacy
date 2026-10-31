# Verification

## Hardware records — 25 October 2026

Device: M7 LS32BM700UUXEN, firmware T-NKLBWWC-1720.7.

| Operation | Result |
| --- | --- |
| Archive the 17 application directories | Completed |
| Remove the 17 packages | Each returned `key[end] val[ok]` |
| Set firmware autoupdate to 0 with `vconftool set -f` | Read back 0 |
| Stop the two context-aware services | Inactive after cleanup |
| Network and Bluetooth services | Active after cleanup |
| Earlier privacy apply script | Timed out, exit 124; not included here |

The runtime-mask procedure in [PRIVACY.md](PRIVACY.md) is separate from the
package removals and persistent suppression markers. Raw device logs and
backups are not distributed.

## Local tests — 31 October 2026

Six tests passed using temporary directories and mocked device commands:
preview, successful backup/removal and rerun refusal, missing package,
archive failure, uninstall failure, and missing success callback.
Shell syntax and secret scans passed.

The packaged script has not been rerun on hardware. Complete package
restoration and compatibility with other devices remain untested.
