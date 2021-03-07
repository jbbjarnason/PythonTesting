# Python testing
## Upload firmware on scan

This module can help with uploading firmware onto a controller that needs a label to be assigned to it.

### Usage

Example:

```bash
$ ./Uploader
# or
$ ./Uploader --ip 127.0.0.1 --port 1337 --cmd "some flash command"
```

Todo: assign barcode label to firmware

Create local tcp server for testing environment
```bash
$ nc -l -p 1337
barcode=123abc

```