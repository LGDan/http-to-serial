# http-to-serial
Interact with `ttyACM` / `ttyAMA` / `ttyUSB` devices via a REST API.

## Serial Devices

- [GET] `/api/v1/devices` - *List available devices*
- [GET] `/api/v1/device/{device_name}` - *Check port/device exists*
- [GET] `/api/v1/device/{device_name}:{baud_rate}/open` - *Open device*
- [GET] `/api/v1/device/{device_name}:{baud_rate}/close` - *Close device*

## IO - Writing

- [GET] `/api/v1/write/{device_name}/{string}` - *Write to device*
- [GET] `/api/v1/writeline/{device_name}/{string}` - *Write to device, followed by newline*
- ~~[POST] `/api/v1/write/{device_name}` - *Write raw to device*~~ (Broken, will be fixed in future)

## IO - Reading

- [GET] `/api/v1/read/{device_name}/{count}` - *Read n bytes from device*
- [GET] `/api/v1/readline/{device_name}` - *Read a line from the device*
- [GET] `/api/v1/readall/{device_name}` - *Read all available data from the device*

## Cached Data

>⚠️ These endpoints currently share a cyclical buffer across all devices. This will be fixed in the future.

- [GET] `/api/v1/device/{device_name}/lastlines/{line_count}` - *Get last N lines from device*
- [GET] `/api/v1/device/{device_name}/lastchars/{char_count}` - *Get last N characters from device*

## Buffers

- [GET] `/api/v1/device/{device_name}/waiting/in` - *Get input buffer byte count*
- [GET] `/api/v1/device/{device_name}/waiting/out` - *Get output buffer byte count*