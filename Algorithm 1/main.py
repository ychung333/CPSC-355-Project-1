"""
CPSC 335 — Project 1
Algorithm 1: ALTERNATING_DISKS_BIDIRECTIONAL
Authors: Yu-Chen Chung, Rene Acosta, Sheikh Sabah Ali
Emails:  ychung30@csu.fullerton.edu, reneacosta98@csu.fullerton.edu,sheiksabah@csu.fullerton.edu

"""

import disks


def main():
    """ to demonstrate the Alternating Disks Problem with an example """

    # n = 4 -> 8 disks alternating L, D
    disks_list = ['L', 'D', 'L', 'D', 'L', 'D', 'L', 'D']

    # Running the algorithm
    final_arrangement, total_swaps = disks.alternating_disks_bidirectional(disks_list)

    # Displaying the results
    print("Final arrangement:", final_arrangement)
    print("Total swaps:", total_swaps)

if __name__ == "__main__":
    main()
