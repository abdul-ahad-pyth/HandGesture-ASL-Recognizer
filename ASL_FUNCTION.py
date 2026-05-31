import numpy as np


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_angle(a, b, c):
    """Teen landmarks ke beech ka angle nikalta hai (degrees mein)."""
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))


def get_distance(a, b):
    """Do landmarks ke beech ki distance nikalta hai."""
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


# ─────────────────────────────────────────────
#  LEVEL 1 — UPGRADED get_hand_state
#  Purana: sirf up/down check karta tha
#  Naya : angles use karta hai — zyada accurate
# ─────────────────────────────────────────────

def get_hand_state(hand_landmarks):
    lm = hand_landmarks.landmark

    STRAIGHT = 150  # angle > 150 matlab finger straight/upar hai

    # Har finger ka angle nikalo (MCP → PIP → TIP)
    thumb_angle  = get_angle(lm[1],  lm[2],  lm[4])
    index_angle  = get_angle(lm[5],  lm[6],  lm[8])
    middle_angle = get_angle(lm[9],  lm[10], lm[12])
    ring_angle   = get_angle(lm[13], lm[14], lm[16])
    pinky_angle  = get_angle(lm[17], lm[18], lm[20])

    fingers = [
        thumb_angle  > STRAIGHT,   # [0] Thumb
        index_angle  > STRAIGHT,   # [1] Index
        middle_angle > STRAIGHT,   # [2] Middle
        ring_angle   > STRAIGHT,   # [3] Ring
        pinky_angle  > STRAIGHT,   # [4] Pinky
    ]

    # Extra info — recognize_asl mein use hogi
    extras = {
        "lm"                : lm,
        "thumb_index_dist"  : get_distance(lm[4], lm[8]),
        "index_middle_dist" : get_distance(lm[8], lm[12]),
        "thumb_middle_dist" : get_distance(lm[4], lm[12]),
        "thumb_ring_dist"   : get_distance(lm[4], lm[16]),
        "index_angle"       : index_angle,
        "middle_angle"      : middle_angle,
        "thumb_angle"       : thumb_angle,
        "pinky_angle"       : pinky_angle,
    }

    return fingers, extras


# ─────────────────────────────────────────────
#  LEVEL 2 — UPGRADED recognize_asl
#  Confusing letters alag kiye: A/E/S/M/N,
#  R/U, D/G, F, C, etc.
# ─────────────────────────────────────────────

def recognize_asl(fingers, extras):
    t, i, m, r, p = fingers
    lm                = extras["lm"]
    thumb_index_dist  = extras["thumb_index_dist"]
    thumb_middle_dist = extras["thumb_middle_dist"]
    thumb_ring_dist   = extras["thumb_ring_dist"]
    index_middle_dist = extras["index_middle_dist"]

    up = sum(fingers)  # kitni ungliyan upar hain

    # ── 0 fingers up: A / E / S / M / N ──────────────────
    if up == 0:
        # Thumb kitni ungliyon ke upar (y-axis) hai
        over_index  = lm[4].y > lm[8].y
        over_middle = lm[4].y > lm[12].y
        over_ring   = lm[4].y > lm[16].y

        fingers_covered = sum([over_index, over_middle, over_ring])

        if fingers_covered == 3:
            return "M"                        # thumb teeno ke upar
        elif fingers_covered == 2:
            return "N"                        # thumb do ke upar
        elif lm[4].x < lm[3].x:              # thumb side mein tucked
            return "S"
        elif lm[4].y < lm[8].y:              # thumb side pe extended
            return "A"
        else:
            return "E"

    # ── All 5 up: B ───────────────────────────────────────
    elif up == 5:
        return "B"

    # ── 4 up (no thumb): B ───────────────────────────────
    elif up == 4 and not t:
        return "B"

    # ── Index only up ─────────────────────────────────────
    elif up == 1 and i:
        # X: index tip neeche jhuka hua (hooked)
        if lm[8].y > lm[6].y:
            return "X"
        # D: thumb middle se touch kare
        if thumb_middle_dist < 0.05:
            return "D"
        return "G"                            # index side mein point kare

    # ── Pinky only up ─────────────────────────────────────
    elif up == 1 and p:
        return "I"

    # ── Index + Thumb up: L ───────────────────────────────
    elif up == 2 and i and t:
        return "L"

    # ── Pinky + Thumb up: Y ───────────────────────────────
    elif up == 2 and p and t:
        return "Y"

    # ── Index + Middle up: V / R / U / H ──────────────────
    elif up == 2 and i and m and not t:
        # R: index aur middle cross hoti hain
        fingers_crossed = abs(lm[8].x - lm[12].x) < 0.03
        if fingers_crossed:
            return "R"
        # H: fingers horizontal hain (side mein point kar rahi hain)
        horizontal = abs(lm[8].y - lm[12].y) < 0.04
        if horizontal:
            return "H"
        return "U" if index_middle_dist < 0.05 else "V"

    # ── Index + Middle + Ring + Pinky up (no thumb): B ───
    elif up == 4 and not t:
        return "B"

    # ── Index + Middle + Ring up: W ───────────────────────
    elif up == 3 and i and m and r and not p and not t:
        return "W"

    # ── Middle + Ring + Pinky up (no index, no thumb): ───
    elif up == 3 and not i and m and r and p and not t:
        # F: thumb aur index touch karte hain
        if thumb_index_dist < 0.04:
            return "F"

    # ── Thumb + Index + Middle up: K / P ─────────────────
    elif up == 3 and t and i and m and not r and not p:
        # K: index upar, middle side mein
        if lm[8].y < lm[5].y:
            return "K"
        return "P"

    # ── All curved (C shape) ──────────────────────────────
    # Jab sab fingers thodi khuli hoon — C shape
    elif not i and not m and not r and not p and not t:
        if thumb_index_dist > 0.08:
            return "C"

    # ── O shape: thumb aur index circle banayein ─────────
    elif up == 0 or (not i and not m and not r and not p):
        if thumb_index_dist < 0.04:
            return "O"

    # ── T: thumb index aur middle ke beech ───────────────
    elif up == 0:
        thumb_between = lm[6].x < lm[4].x < lm[10].x
        if thumb_between:
            return "T"

    return "?"