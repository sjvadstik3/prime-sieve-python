#!/usr/bin/env python3
"""half-optimised prime sieve written by sjvadstik3: license on line 101"""

from time import perf_counter
from math import floor, sqrt
from sys import argv
from bitarray import bitarray


def main(length):
    """runs the functions create_array and sieve in the right
     order to sieve for primes and prints some information"""
    try:
        length = int(length)
    except ValueError:
        print(f"invalid number '{length}'")
        return 1
    start_time = perf_counter()
    print("creating array...")
    arr = create_array(length)
    print("done. \nsieving array...")
    arr = sieve(arr, length)
    print("done. \nwriting file...")

    with open("primes.txt", "w", encoding="utf8") as file:
        # more nonsense for the progress bar
        end, end_percent, percent_done = len(arr), len(arr) / 100, 0
        prime_count = 0
        # indexes of nonzero bits in arr are prime: get written to file
        for index, prime in enumerate(arr):
            if prime:
                prime_count += 1
                file.write(str(index+1) + " \n")
            elif index >= int(percent_done):
                percent_done += end_percent
                progress_bar(index, round(end), False)
        del arr  # freeing the memory asap
        file.write("by sjvadstik3")
    progress_bar(100, 100, True)  # true indicates to set a newline
    total_time = perf_counter() - start_time
    # prints time taken
    print(f"finished in {int(total_time/3600)} hours, \
{int((total_time % 3600)/60)} minutes and \
{round(total_time % 60, 6)} seconds")
    # how many primes found
    print(f"{prime_count} primes found between 0 and {length}")
    return 0


def create_array(length):
    """this fuction creates a bitarray with 1 representing possible primes"""
    # these values just apply the twin primes conjecture
    start, middle = "011010", "100010"
    return bitarray(start + middle * floor(length / 6))[:length]


def progress_bar(current, total, end, length=100):
    """this prints a progress bar in the terminal"""
    fraction = current / total
    progress = int(fraction * length) * '█'
    space = int(length - len(progress)) * ' '
    if not end:
        ending = '\r'  # \r = return (overwrites exisitng line)
    else:
        ending = "\n"
    # formatting the progress bar
    print(f'[{progress}{space}] {int(fraction*100)}%', end=ending)


def sieve(arr, end):
    """this does the sieving of primes from the array"""
    # starts the sieve at 5 hasn't been "precomputed" by the twin prime theorem
    mesh = 5
    # the sieve need only use values up to the square root of the limit
    search_end = round(sqrt(end))
    end_percent, percent_done = search_end / 100, 0  # progress bar stuff
    while mesh < search_end:  # sieve loop
        # values below mesh^2 have already been sieved
        # steps of 2*mesh avoid sieving even numbers
        for index in range(mesh * mesh, end, 2 * mesh):
            arr[index - 1] = 0
        # finds the next prime, and sets that to the sieve number
        next_prime = False
        while not next_prime:
            mesh += 2
            if mesh > search_end:
                progress_bar(100, 100, True)  # see line 35
                return arr
            next_prime = arr[mesh - 1] == 1
        if mesh >= round(percent_done):  # progress bar shenanigans
            percent_done += end_percent
            progress_bar(round(percent_done), round(search_end), False)
    progress_bar(100, 100, True)  # see line 35
    return arr


if __name__ == "__main__":
    exit(main(argv[1]))


#   Copyright (C) 2022  sjvadstik3
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
