# Removed packages

All 17 entries returned `key[end] val[ok]` in the original M7 run on
25 October 2026. Directory archives were created first. This does not
confirm compatibility with any other device.

- `com.samsung.tizen.samsung-analytics`
- `com.samsung.tv.context-aware-agent`
- `com.samsung.tv.context-aware-service`
- `com.samsung.tv.tvplus`
- `com.samsung.tv.tvPlusDeeplinker`
- `com.samsung.tv.wakeup-engine-bixby`
- `com.samsung.tv.wakeup-engine-alexa`
- `com.samsung.tv.alexa-client`
- `com.samsung.tv.bixby-prov`
- `com.samsung.tv.mybixby`
- `com.samsung.tv.bixbycapsuleviewer`
- `com.samsung.tv.ondevice-voice`
- `com.samsung.tv.farfieldvoice`
- `com.samsung.tizen.smartthings-client`
- `com.samsung.tv.smartthingsfind-daemon`
- `com.samsung.tv.iot-hub-control`
- `samsunghealth-service-tv`

The three post-removal suppression markers are for ondevice-voice and the
two context-aware packages. They live under `/opt/usr/share/systemd/system/`
and persist across reboot, unlike the runtime masks in PRIVACY.md.
