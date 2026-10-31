# Selected analytics and diagnostic services

Target: M7 LS32BM700UUXEN / T-NKLBWWC-1720.7. Run commands in a root shell **on the monitor**.

The following units are the five services controlled by the Tizen Deck privacy feature:

```text
contents-recognition-service.service
abnormal_user_behavior.service
emergency-log-transmitter.service
media-analytics-service.service
kpi-logging.service
```

## Inspect and record

For each unit, inspect its state before making changes. Example:

```sh
systemctl show media-analytics-service.service -p LoadState -p ActiveState -p UnitFileState
```

Keep a private record of the original state and of the units you change. Skip missing units and units already masked by another tool. Do not remove someone else's existing masks.

## Block for the current boot

For each selected, existing, previously unmasked unit:

```sh
systemctl mask --runtime media-analytics-service.service
systemctl stop media-analytics-service.service
systemctl show media-analytics-service.service -p LoadState -p ActiveState
```

Replace the unit name with another name from the list. Check that it is masked and no longer active. Stop if a command fails; review the state before continuing.

## Undo

Remove only runtime masks you created:

```sh
systemctl unmask --runtime media-analytics-service.service
```

If the unit was active before the change, restart it:

```sh
systemctl start media-analytics-service.service
```

Leave previously inactive units stopped. A reboot also clears these runtime masks. This standalone procedure does not install a boot hook or automatically reapply them.

These five masks do not cover every Samsung network service. `issue_report_agent` is outside this list because `devicetracker` depends on it. Network connectivity, manual updates and other applications remain available.
