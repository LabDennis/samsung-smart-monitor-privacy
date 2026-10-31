# Verification

Reviewed on 31 October 2026 against the original local command/result records
from 25 October: debloat-backup, debloat-apply2, update-final,
debloat-cleanup, privacy-apply-result and privacy-followup.
Raw records and backups are private and are not distributed.

- All 17 package backups completed and all 17 removals reported success.
- The first firmware-setting write failed because `-f` was missing. The later
  corrected write succeeded and read back 0. UPDATES.md now uses that command.
- Cleanup reported both context-aware services inactive; connman and the
  Bluetooth services remained active. This is a point-in-time result.
- The original privacy script timed out (exit 124). It used a different service
  list, persistent markers and a rollback that started all selected units.
  It is deliberately not shipped as a reliable apply/undo script. PRIVACY.md
  describes the later, separate five-service runtime-mask approach.

The current debloat script retains the original 17-package scope. It now
prints its selection without applying, validates directories before backup,
saves archive hashes and uninstall logs, requires a successful pkgcmd callback,
and records newly created suppression markers. Firmware updates remain a
separate choice. Existing backups are never reused automatically.

Tests execute a temporary copy with device paths redirected to a temporary
fixture and mocked device commands. They do not connect to a monitor. They
cover no-change invocation, successful backup/removal, missing packages,
archive failure, uninstall failure, missing success callbacks and rerun refusal.
No new hardware run or complete restoration test has been performed.
