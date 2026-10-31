# Samsung Smart Monitor Privacy

Privacy controls, firmware autoupdate settings and optional debloat for the **Samsung Smart Monitor M7 LS32BM700UUXEN**, firmware **T-NKLBWWC-1720.7**, Tizen 6.5.

Use this project without a launcher or web administration service. It contains project-written documentation and an optional shell script; firmware, Samsung binaries and root exploits are not bundled.

## Choose what to change

| Feature | Guide | Effect |
| --- | --- | --- |
| Analytics / diagnostic services | [Privacy](docs/PRIVACY.md) | Mask selected services for the current boot |
| Firmware autoupdate | [Updates](docs/UPDATES.md) | Set the automatic firmware update preference to off |
| Optional debloat | [Debloat](docs/DEBLOAT.md) | Remove selected analytics, voice, TV Plus, SmartThings and Health packages |

Commands run **on the monitor**, in an already authorized root shell. They are not PC setup commands. Obtain root tools separately from [samsung-tv-root](https://github.com/chris-ritsen/samsung-tv-root), following that project's model/firmware compatibility guidance. Root access is not installed by this repository.

Service masks are temporary and expire after reboot. Turning off the firmware autoupdate preference does not block every update endpoint, manual updates or app-store updates. These measures reduce selected background activity; they do not establish complete telemetry removal. Disabling autoupdate also means security updates must be managed manually.

The underlying service controls and package commands come from the same M7 configuration documented in [Tizen Deck](https://github.com/LabDennis/tizen-deck). This standalone packaging has been checked locally, not reapplied to a monitor. Other models and firmware versions are unverified.

## Related projects

- [Tizen Deck](https://github.com/LabDennis/tizen-deck): monitor administration and optional native TV service.
- [Tizen Deck XMB](https://github.com/LabDennis/tizen-deck-xmb): German-language launcher.

Developed by LabDennis with OpenAI Codex. No affiliation with Samsung.
