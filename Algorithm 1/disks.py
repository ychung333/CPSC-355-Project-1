"""
CPSC 335 — Project 1
Algorithm 1: ALTERNATING_DISKS_BIDIRECTIONAL
Authors: Yu-Chen Chung, Rene Acosta, Sheikh Sabah Ali
Emails:  ychung30@csu.fullerton.edu, reneacosta98@csu.fullerton.edu,sheiksabah@csu.fullerton.edu
"""


def alternating_disks_bidirectional(A):
    """ Input: a list A of length 2n, each element 'L' or 'D'
        Output: all 'D' left, all 'L' right and swap count """
    
    swaps = 0              # counter for total number of swaps done
    didSwap = True         # bool to track if any swap occured in a pass

    while didSwap:
        didSwap = False    # reset flag at the start of each round

    # Left to right pass
        for i in range(len(A) - 1):
            if A[i] == 'L' and A[i+1] == 'D':     # if a light disk is left of a dark disk
                A[i], A[i+1] = A[i+1], A[i]       # swap them
                swaps += 1                        # increment swap counter
                didSwap = True                    # to mark as swap occured

    # Right to left pass
        for i in range(len(A) - 2, -1, -1):
            if A[i] == 'L' and A[i+1] == 'D':     # if a light disk is left of a dark disk
                A[i], A[i+1] = A[i+1], A[i]       # swap them
                swaps += 1                        # increment swap counter
                didSwap = True                    # mark that a swap occured

    return A, swaps         # A is the final list showing the correct disk arragement
                            # swap is the total number of neighboring swaps done
