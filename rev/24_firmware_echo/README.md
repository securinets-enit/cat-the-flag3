# Firmware Echo

**Category:** Reverse engineering  
**Difficulty:** Hard  
**Technique:** Firmware carving, filesystem metadata, architecture-independent emulation

Players receive `attachments/router.fw`. It is a small fictional firmware
image containing a header, a reversed filesystem table, and an encoded
configuration record. No real device, malware, network, or privileged access
is involved.

Use the supplied solver or inspect the image with a hex editor. This is
offline and does not need Docker.
