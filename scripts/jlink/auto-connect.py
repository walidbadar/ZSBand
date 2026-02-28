#!/usr/bin/env python3

import platform
import subprocess
import time

def beep(freq=1000, duration_ms=100):
    """Cross-platform beep."""
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(freq, duration_ms)
        else:
            subprocess.run(
                ["play", "-n", "synth", str(duration_ms / 1000), "sine", str(freq)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
    except Exception:
        pass

while True:
    try:
        proc = subprocess.run(
            ["JLinkExe", "-Device", "CORTEX-M33", "-CommandFile", "config.jlink"],
            # ["ezFlashCLI", "probe"],
            input=b"r\nexit\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        # Decode output safely
        output = proc.stdout.decode("windows-1252") + proc.stderr.decode("windows-1252")
        print(output)

        if "Failed to attach to CPU" in output:
            print("Target Not found!")
            beep(500, 100)
        else:
            print("Target Found!")
            for _ in range(4):
                beep(4000, 100)
                beep(1000, 100)
        
        time.sleep(1)

    except subprocess.TimeoutExpired:
        print("Command timed out.")
        beep(300, 200)

    except Exception as e:
        print(f"Unexpected error: {e}")
        beep(200, 300)
