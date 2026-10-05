# Runtime Forensics — Walkthrough

**Author:** 7ankalis — Securinets ENIT
**Flags:** 5

## Run the container

    docker pull sitaha/webhook-relay:2.4.0
    docker run -d --name suspect -p 8080:8080 sitaha/webhook-relay:2.4.0

The -d flag runs the container detached so it stays alive while you
analyze it.

## Flag 1 — Environment variables

Container config is visible from the host:

    docker inspect suspect --format '{{json .Config.Env}}' | jq

Output includes:

    "RELAY_API_KEY=SecurinetsENIT{3nv_1n5p3c7_5h0w5_4ll}"

Flag 1:

    SecurinetsENIT{3nv_1n5p3c7_5h0w5_4ll}

## Flag 2 — Container logs

Docker captures stdout and stderr from the entrypoint process:

    docker logs suspect

Output includes:

    [info] init complete — agent id: SecurinetsENIT{l0g5_n3v3r_l13}

Flag 2:

    SecurinetsENIT{l0g5_n3v3r_l13}

## Enter the container

    docker exec -it suspect sh

You are now inside the running container's namespace.

## Flag 3 — Hidden config

Look at the filesystem:

    ls -la /etc/
    cat /etc/relay.conf

Output:

    c2_host=metrics-collect.xyz
    c2_port=443
    upload_path=/v1/relay
    api_token=SecurinetsENIT{c2_c0nf1g_3xp053d}
    sync_interval=300

Flag 3:

    SecurinetsENIT{c2_c0nf1g_3xp053d}

## Flag 4 — Cron persistence

Check cron directories:

    ls -la /etc/cron.d/
    cat /etc/cron.d/webhook-sync

Output:

    # Webhook Relay — periodic sync
    # Author: 7ankalis — Securinets ENIT
    # SecurinetsENIT{cr0n_p3r51573nc3_f0und}

    */5 * * * * root /usr/local/bin/.relay-agent --sync

Flag 4:

    SecurinetsENIT{cr0n_p3r51573nc3_f0und}

## Flag 5 — Process arguments

List processes:

    ps aux

Output:

    USER   PID   COMMAND
    root   1     /bin/bash /usr/local/bin/start.sh
    root   7     python3 /app/server.py
    root   8     /usr/local/bin/.relay-agent --id=SecurinetsENIT{pr0c_n3t_w0rk5}

Flag 5 is in the agent's command-line arguments:

    SecurinetsENIT{pr0c_n3t_w0rk5}

If ps isn't installed, enumerate /proc manually:

    ls /proc/ | grep -E '^[0-9]+$'
    cat /proc/8/cmdline | tr '\0' ' '

## What the container is actually doing

- The entrypoint runs two processes in parallel: the legitimate
  Python server and a hidden `.relay-agent` C binary
- The agent reads `/etc/relay.conf` on startup and beacons to
  `metrics-collect.xyz:443`
- A cron file at `/etc/cron.d/webhook-sync` re-executes the agent
  every 5 minutes
- The environment variable `RELAY_API_KEY` holds an authentication
  token to the C2

## Summary

| # | Flag | Where |
|---|---|---|
| 1 | SecurinetsENIT{3nv_1n5p3c7_5h0w5_4ll} | docker inspect env |
| 2 | SecurinetsENIT{l0g5_n3v3r_l13} | docker logs |
| 3 | SecurinetsENIT{c2_c0nf1g_3xp053d} | /etc/relay.conf |
| 4 | SecurinetsENIT{cr0n_p3r51573nc3_f0und} | /etc/cron.d/webhook-sync |
| 5 | SecurinetsENIT{pr0c_n3t_w0rk5} | ps aux inside container |

## What the player learns

- docker inspect exposes runtime config, env, and metadata
- docker logs captures output from PID 1 and its children
- docker exec drops you into a running container's namespace
- Cron files in /etc/cron.d are a common persistence location
- Process arguments can leak credentials and identifiers
- Runtime forensics requires the container to be alive
- Static and runtime analysis are complementary — Task 2 taught the
  static side, Task 3 teaches the runtime side
