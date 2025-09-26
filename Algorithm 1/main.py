# *************************************************
# main.py                                          *
# Main file                                        *
# Sheikh Sabah Ali                                 *
# Rene Acosta                                      *
# Yu-chen Chung                                    *
# *************************************************

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
