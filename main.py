import math
import time
import sys
import os

os.system("cls")

# =========================
# CONFIG
# =========================

WIDTH = 120
HEIGHT = 40

THETA_SPACING = 0.05
PHI_SPACING = 0.02

R1 = 1
R2 = 2

K2 = 6
K1 = 35

ASCII = ".,-~:;=!*#$@"

FPS = 120

# =========================

# ANSI escape sequences
CLEAR_SCREEN = "\x1b[2J"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"

# limpa apenas uma vez
sys.stdout.write(CLEAR_SCREEN)
sys.stdout.write(HIDE_CURSOR)
sys.stdout.flush()

A = 0
B = 0

# frame anterior
previous_output = [" "] * (WIDTH * HEIGHT)

try:

    while True:

        start = time.perf_counter()

        zbuffer = [0] * (WIDTH * HEIGHT)
        output = [" "] * (WIDTH * HEIGHT)

        cosA = math.cos(A)
        sinA = math.sin(A)

        cosB = math.cos(B)
        sinB = math.sin(B)

        theta = 0

        while theta < 2 * math.pi:

            costheta = math.cos(theta)
            sintheta = math.sin(theta)

            phi = 0

            while phi < 2 * math.pi:

                cosphi = math.cos(phi)
                sinphi = math.sin(phi)

                circlex = R2 + R1 * costheta
                circley = R1 * sintheta

                x = (
                    circlex * (cosB * cosphi + sinA * sinB * sinphi)
                    - circley * cosA * sinB
                )

                y = (
                    circlex * (sinB * cosphi - sinA * cosB * sinphi)
                    + circley * cosA * cosB
                )

                z = (
                    K2
                    + cosA * circlex * sinphi
                    + circley * sinA
                )

                ooz = 1 / z

                xp = int(WIDTH / 2 + K1 * ooz * x)
                yp = int(HEIGHT / 2 - K1 * ooz * y * 0.5)

                if 0 <= xp < WIDTH and 0 <= yp < HEIGHT:

                    idx = xp + yp * WIDTH

                    L = (
                        cosphi * costheta * sinB
                        - cosA * costheta * sinphi
                        - sinA * sintheta
                        + cosB * (
                            cosA * sintheta
                            - costheta * sinA * sinphi
                        )
                    )

                    if L > 0:

                        if ooz > zbuffer[idx]:

                            zbuffer[idx] = ooz # type: ignore

                            luminance = int(
                                L * (len(ASCII) - 1)
                            )

                            output[idx] = ASCII[
                                min(
                                    luminance,
                                    len(ASCII) - 1
                                )
                            ]

                phi += PHI_SPACING

            theta += THETA_SPACING

        # =========================
        # UPDATE DIFERENCIAL
        # =========================

        for i in range(WIDTH * HEIGHT):

            if output[i] != previous_output[i]:

                x = (i % WIDTH) + 1
                y = (i // WIDTH) + 1

                # move cursor diretamente
                sys.stdout.write(
                    f"\x1b[{y};{x}H{output[i]}"
                )

        sys.stdout.flush()

        previous_output = output.copy()

        A += 0.04
        B += 0.02

        elapsed = time.perf_counter() - start

        sleep_time = (1 / FPS) - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:

    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.write("\x1b[0m")
    sys.stdout.flush()