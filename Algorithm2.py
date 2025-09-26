"""
CPSC 335 — Project 1
Algorithm 2: Matching Group Schedules
Authors: Yu-Chen Chung, Rene Acosta, Sheikh Sabah Ali
Emails:  ychung30@csu.fullerton.edu,  ,sheiksabah@csu.fullerton.edu

Implements the provided pseudocode structure for Algorithm 2.
Complexity: O(k log k), where k is the total number of intervals
(all busy + outside-active sentinels). Sorting/merging dominates.
"""

from typing import List, Tuple

# -----------------------------
# --- Helper Functions ---
# -----------------------------

def TO_MIN(t: str) -> int:
    """
    Convert "HH:MM" string into total minutes since 00:00.
    Example: "09:30" -> 570.
    This also tolerates extra spaces (e.g., "18: 30").
    """
    t = t.strip().replace(" ", "")
    H_str, M_str = t.split(":")
    H, M = int(H_str), int(M_str)
    return 60 * H + M

def TO_HHMM(m: int) -> str:
    """
    Convert minutes back into "HH:MM" format, zero-padded.
    Example: 570 -> "09:30".
    """
    H = m // 60
    M = m % 60
    return f"{H:02d}:{M:02d}"

def MERGE_OVERLAPS(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge overlapping or touching half-open intervals [s, e).
    Input: list of (start, end) in minutes.
    Output: merged, non-overlapping intervals sorted by start time.
    """
    if not intervals:
        return []
    # Sort intervals by start time, then end time
    intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    out = [intervals[0]]
    for s, e in intervals[1:]:
        ps, pe = out[-1]
        if s <= pe:
            # Overlaps with previous → extend the last interval
            out[-1] = (ps, max(pe, e))
        else:
            out.append((s, e))
    return out

# ------------------------------------------------
# --- Main Algorithm: MATCHING_GROUP_SCHEDULES ---
# ------------------------------------------------

def MATCHING_GROUP_SCHEDULES(
    Schedules: List[List[Tuple[str, str]]],
    Actives:   List[Tuple[str, str]],
    dur:       int
) -> List[Tuple[str, str]]:
    """
    Find all time intervals where all group members are free
    for at least `dur` minutes.

    Parameters:
    - Schedules: list of people; each person has a list of busy intervals (start, end) in "HH:MM"
    - Actives:   list of daily active windows (start, end) per person
    - dur:       required meeting duration in minutes

    Returns:
    - List of available intervals (start, end) in "HH:MM"
    """

    # --- 1) Compute group active window (intersection across all people) ---
    group_active_start = max(TO_MIN(a[0]) for a in Actives)
    group_active_end   = min(TO_MIN(a[1]) for a in Actives)
    if group_active_start >= group_active_end:
        # No common active time → no possible meeting
        return []

    # --- 2) Build per-person "effective busy" list (inside their daily active period) ---
    all_busy: List[Tuple[int, int]] = []
    for i in range(len(Schedules)):
        aS = TO_MIN(Actives[i][0])
        aE = TO_MIN(Actives[i][1])

        # Outside each person's active window = unavailable
        if aS > 0:
            all_busy.append((0, aS))
        if aE < 1440:  # 1440 = total minutes in a day
            all_busy.append((aE, 1440))

        # Add that person’s busy intervals, clamped to their active window
        for (bs, be) in Schedules[i]:
            s = max(TO_MIN(bs), aS)
            e = min(TO_MIN(be), aE)
            if s < e:
                all_busy.append((s, e))

    # --- 3) Merge all busy intervals across the group ---
    group_busy = MERGE_OVERLAPS(all_busy)

    # --- 4) Clamp busy intervals to the group’s active intersection ---
    clamped_busy: List[Tuple[int, int]] = []
    for (s, e) in group_busy:
        cs = max(s, group_active_start)
        ce = min(e, group_active_end)
        if cs < ce:
            clamped_busy.append((cs, ce))
    clamped_busy = MERGE_OVERLAPS(clamped_busy)

    # --- 5) Find the complement (free slots) inside the group active window ---
    free: List[Tuple[int, int]] = []
    cur = group_active_start
    for (s, e) in clamped_busy:
        if cur < s:
            free.append((cur, s))  # gap before the busy interval
        cur = max(cur, e)
    if cur < group_active_end:
        free.append((cur, group_active_end))  # gap after the last busy

    # --- 6) Filter by duration and convert back to "HH:MM" format ---
    result: List[Tuple[str, str]] = []
    for (s, e) in free:
        if (e - s) >= dur:
            result.append((TO_HHMM(s), TO_HHMM(e)))

    return result

# -----------------
# Example Execution
# -----------------
if __name__ == "__main__":
    # Example from the project handout
    person1_Schedule = [("07:00", "08:30"), ("12:00", "13:00"), ("16:00", "18:00")]
    person1_DailyAct = ("09:00", "19:00")

    person2_Schedule = [("09:00", "10:30"), ("12:20", "14:00"),
                        ("14:30", "15:00"), ("16:00", "17:00")]
    person2_DailyAct = ("09:00", "18:30")

    schedules = [person1_Schedule, person2_Schedule]
    actives   = [person1_DailyAct, person2_DailyAct]
    duration  = 30  # minutes

    # Print all common free time slots
    print(MATCHING_GROUP_SCHEDULES(schedules, actives, duration))
    # Expected (may include 14:00–14:30): 
    # [('10:30', '12:00'), ('14:00', '14:30'), ('15:00', '16:00'), ('18:00', '18:30')]
