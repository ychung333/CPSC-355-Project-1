"""
CPSC 335 — Project 1
Algorithm 2: Matching Group Schedules
Author(s): Yu-Chen Chung
Email(s):  ychung30@csu.fullerton.edu

Implements exactly the provided pseudocode structure.
Complexity: O(k log k), where k is total intervals (busy + sentinels).
"""

from typing import List, Tuple

# -----------------------------
# --- Helpers (as specified) ---
# -----------------------------

def TO_MIN(t: str) -> int:
    # "HH:MM" -> minutes since 00:00
    t = t.strip().replace(" ", "")  # tolerate accidental spaces like "18: 30"
    H_str, M_str = t.split(":")
    H, M = int(H_str), int(M_str)
    return 60 * H + M

def TO_HHMM(m: int) -> str:
    # minutes -> "HH:MM"
    H = m // 60
    M = m % 60
    return f"{H:02d}:{M:02d}"

def MERGE_OVERLAPS(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    # intervals: list of [s, e) in minutes
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: (x[0], x[1]))  # start asc, then end asc
    out = [intervals[0]]
    for s, e in intervals[1:]:
        ps, pe = out[-1]
        if s <= pe:
            # extend last
            out[-1] = (ps, max(pe, e))
        else:
            out.append((s, e))
    return out

# ------------------------------------------------
# MATCHING_GROUP_SCHEDULES (exact pseudocode flow)
# ------------------------------------------------

def MATCHING_GROUP_SCHEDULES(
    Schedules: List[List[Tuple[str, str]]],
    Actives:   List[Tuple[str, str]],
    dur:       int
) -> List[Tuple[str, str]]:
    """
    Schedules: list of persons; each has Busy = list of (start_time, end_time) as "HH:MM" strings
    Actives:   list of (active_start, active_end) strings, one per person
    dur:       integer minutes
    Returns:   list of (start, end) "HH:MM" where ALL members are available
    """

    # --- 1) Compute group active window (intersection across persons) ---
    group_active_start = max(TO_MIN(a[0]) for a in Actives)
    group_active_end   = min(TO_MIN(a[1]) for a in Actives)
    if group_active_start >= group_active_end:
        return []  # no overlapping active time across the group

    # --- 2) Build per-person "effective busy" within the day ---
    all_busy: List[Tuple[int, int]] = []
    for i in range(len(Schedules)):
        aS = TO_MIN(Actives[i][0])
        aE = TO_MIN(Actives[i][1])

        # Block time outside the person’s active window (so they can't meet then)
        # (Clamp to the global day range [0, 1440) to be safe)
        if aS > 0:
            all_busy.append((0, aS))
        if aE < 1440:
            all_busy.append((aE, 1440))

        # Add that person's busy intervals, clamped to [aS, aE]
        for (bs, be) in Schedules[i]:
            s = max(TO_MIN(bs), aS)
            e = min(TO_MIN(be), aE)
            if s < e:
                all_busy.append((s, e))

    # --- 3) Union all busy intervals across the group ---
    group_busy = MERGE_OVERLAPS(all_busy)

    # --- 4) Intersect with the group active window (optional but precise) ---
    # Clamp group_busy to [group_active_start, group_active_end]
    clamped_busy: List[Tuple[int, int]] = []
    for (s, e) in group_busy:
        cs = max(s, group_active_start)
        ce = min(e, group_active_end)
        if cs < ce:
            clamped_busy.append((cs, ce))
    clamped_busy = MERGE_OVERLAPS(clamped_busy)

    # --- 5) Take complement inside group active window to get free intervals ---
    free: List[Tuple[int, int]] = []
    cur = group_active_start
    for (s, e) in clamped_busy:
        if cur < s:
            free.append((cur, s))
        cur = max(cur, e)
    if cur < group_active_end:
        free.append((cur, group_active_end))

    # --- 6) Filter by duration and format ---
    result: List[Tuple[str, str]] = []
    for (s, e) in free:
        if (e - s) >= dur:
            result.append((TO_HHMM(s), TO_HHMM(e)))

    # Already in ascending order due to construction; sort if desired
    return result

# -----------------
# Sample standalone
# -----------------
if __name__ == "__main__":
    # Handout example
    person1_Schedule = [("07:00", "08:30"), ("12:00", "13:00"), ("16:00", "18:00")]
    person1_DailyAct = ("09:00", "19:00")

    person2_Schedule = [("09:00", "10:30"), ("12:20", "14:00"),
                        ("14:30", "15:00"), ("16:00", "17:00")]
    person2_DailyAct = ("09:00", "18:30")

    schedules = [person1_Schedule, person2_Schedule]
    actives   = [person1_DailyAct, person2_DailyAct]
    duration  = 30

    print(MATCHING_GROUP_SCHEDULES(schedules, actives, duration))
    # Expected: [('10:30', '12:00'), ('15:00', '16:00'), ('18:00', '18:30')]
