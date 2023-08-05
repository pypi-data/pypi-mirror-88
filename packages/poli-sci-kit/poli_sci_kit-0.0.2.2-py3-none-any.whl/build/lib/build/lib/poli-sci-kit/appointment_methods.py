# ============================================================================= 
# Appointment methods used to derive seat allocations based on population or vote polls
# 
# Contents
# --------
#   0. No Class
#       largest_remainder (aka Hamilton, Vinton, Hare–Niemeyer)
#           Options: Hare, Droop, Hagenbach–Bischoff
#
#       highest_average
#           Options: Jefferson, Webster, Huntington-Hill
# =============================================================================

from math import ceil
from math import floor
from math import modf
from math import sqrt
from operator import itemgetter
from random import shuffle, sample

def largest_remainder(counts, total_seats, 
                      allocation_threshold=None, min_allocation=None, 
                      tie_break='majority', majority_bonus=False, quota_style='Hare'):
    """
    Apportion seats using the Largest Remainder (or Hamilton, Vinton, Hare–Niemeyer) methods

    Parameters
    ----------   
        counts : list
            A list of populations or votes for regions or parties
        
        total_seats : int 
            The number of seats to apportion

        allocation_threshold : float (default=None)
            A minimum threshhold in the poll that must be met to receive seats

        min_allocation : int (default=None)
            A minimum number of seats to be allocated to each region or party

        tie_break : str (default=majority)
            How a tie break is done (by majority or random, with a majority tie defaulting to random)

        majority_bonus : bool (default=False)
            Whether the largest group is automatically given 50% of the vote

        quota_style : str (default=Hare)
            The style of quota vote-seat quota to use

            Options:
                - Hare : total_poll / total_seats

                - Droop : int(total_poll / (total_seats+1)) + 1

                - Hagenbach–Bischoff : total_poll / (total_seats + 1)

    Returns
    -------
        allocations : list
            A list of allocated seats in the order of provided populations or votes
    """
    assert allocation_threshold == None or min_allocation == None, \
        """Appointment methods cannot be used with both an entry threshold and a minimum seat allocation. 
        Set one of allocation_threshold or min_allocation to None"""

    def get_quota(quota_style):
        if quota_style == 'Hare':
            seat_quota = 1.0 * sum(counts) / total_seats
        elif quota_style == 'Droop':
            seat_quota = int(sum(counts) / (total_seats + 1)) + 1
        elif quota_style == 'Hagenbach–Bischoff':
            seat_quota = 1.0 * sum(counts) / (total_seats + 1)
        else:
            ValueError("Invalid quota provided. Choose from Hare, Droop, or Hagenbach–Bischoff.")
        
        return seat_quota

    if allocation_threshold:
        passed_threshold = [True if 1.0 * i / sum(counts) > allocation_threshold else False for i in counts]
        counts = [counts[i] if passed_threshold[i] == True else 0 for i in range(len(counts))]

    original_remainders = None
    if min_allocation:
        assert min_allocation * len(counts) <= total_seats, "The sum of the minimum seats to be allocated cannot be more than the seats to be allocated."
        baseline_allocations = [min_allocation] * len(counts)
        
        # Save the original remainders and allocations to avoid penalization from new divisions after minimum seat allocation
        seat_quota = get_quota(quota_style)
        original_remainders, original_allocations = zip(*[modf(1.0 * v / seat_quota) for v in counts])
        
        # If possible, append the original allocations with the baseline such that the seats for remainders are used for the minimum allocation
        original_with_baseline = [original_allocations[i] if original_allocations[i] > baseline_allocations[i] else baseline_allocations[i] for i in range(len(original_allocations))]
        if sum(original_with_baseline) <= total_seats:
            original_with_baseline = [int(a) for a in original_with_baseline]
            baseline_allocations = original_with_baseline
        
        remaining_seats = total_seats - sum(baseline_allocations)
    
        if remaining_seats == 0:
            return baseline_allocations
    
    seat_quota = get_quota(quota_style)
    remainders, allocations = zip(*[modf(1.0 * v / seat_quota) for v in counts])
    if original_remainders:
        remainders = original_remainders
    allocations = [int(a) for a in allocations]
    unallocated = int(total_seats - sum(allocations))

    remainders_sorted_ids = [i[0] for i in sorted(enumerate(remainders), key=itemgetter(1))][::-1]
    last_assigned_remainder = remainders_sorted_ids[unallocated-1]
    allocatable = [i for i in remainders_sorted_ids if remainders[i] >= remainders[last_assigned_remainder]]
    equal_to_last_assigned = [i for i in allocatable if remainders[i] == remainders[last_assigned_remainder]]

    # Assign for all that are greater than the last remainder to be assigned    
    for k in [i for i in allocatable if i not in equal_to_last_assigned][:unallocated]:
        allocations[k] += 1
        unallocated -= 1

    if len(equal_to_last_assigned) == 1 and unallocated == 1:
        allocations[remainders_sorted_ids[equal_to_last_assigned[0]]] += 1

    else:
        if tie_break == 'majority':
            sorted_by_results = [i[0] for i in sorted(enumerate(allocations), key=itemgetter(1)) if i[0] in equal_to_last_assigned][::-1]
            equal_to_highest = [i for i in sorted_by_results if allocations[i] == allocations[unallocated]]
            
            if len(equal_to_highest) == 1: 
                for k in range(unallocated):
                    allocations[sorted_by_results[k]] += 1

            else:
                # Defaults to random for those with equal allocation and remainder
                sorted_by_results[sorted_by_results.index(equal_to_highest[0]) : sorted_by_results.index(equal_to_highest[-1]) + 1] = \
                    sample(sorted_by_results[sorted_by_results.index(equal_to_highest[0]) : sorted_by_results.index(equal_to_highest[-1]) + 1], len(equal_to_highest))
                for k in range(unallocated):
                    allocations[sorted_by_results[k]] += 1

        elif tie_break == 'random':
            shuffle(equal_to_last_assigned)
            for k in range(unallocated):
                allocations[equal_to_last_assigned[k]] += 1

        else:
            ValueError("A tie break is required for the last seat(s), and an invalid argument has been passed. Please choose from 'majority' or 'random'.")

    if min_allocation:
        allocations = [allocations[i] + baseline_allocations[i] for i in range(len(allocations))]

    if majority_bonus:
        # If a single majority group does not receive at least 50%, then they are given it, and assignment is redone for the rest
        if not allocations[counts.index(max(counts))] >= int(ceil(total_seats / 2)) and len([count for count in counts if count == max(counts)]) == 1:
            non_majority_counts = [count for count in counts if count != max(counts)]
            reduced_seats = total_seats - int(ceil(total_seats / 2))
            non_majority_allocations = largest_remainder(counts=non_majority_counts, total_seats=reduced_seats, 
                                                         allocation_threshold=allocation_threshold, min_allocation=min_allocation, 
                                                         tie_break=tie_break, majority_bonus=False, quota_style=quota_style)

            # Insert majority allocation
            non_majority_allocations[counts.index(max(counts)) : counts.index(max(counts))] = [int(ceil(total_seats / 2))]
            allocations = non_majority_allocations

    return allocations


def highest_average(counts, total_seats, 
                    allocation_threshold=None, min_allocation=None, 
                    tie_break = 'majority', majority_bonus=False, 
                    modifier=None, averaging_style='Jefferson'):
    """
    Apportion seats using the Highest Average (or Jefferson, Webster, Huntington-Hill) methods

    Parameters
    ----------   
        counts : list
            A list of populations or votes for regions or parties
        
        total_seats : int 
            The number of seats to apportion

        allocation_threshold : float (default=None)
            A minimum threshhold in the poll that must be met to receive seats

        min_allocation : int (default=None)
            A minimum number of seats to be allocated to each region or party

        tie_break : str (default=majority)
            How a tie break is done (by majority or random, with a majority tie defaulting to random)

        modifier : float (default=None)
            What to replace the divisor of the first quotient by to change the advantage of groups yet to receive an assignment
            Note: modifiers > 1 disadvantage smaller parties, and modifiers < 1 advantage them 

        averaging_style : str (default=Jefferson)
            The style that highest averages are computed

            Options:
                Each defines a divisor for each region or party to determines the next seat based on all previous assignments

                - Jefferson : divisor_i = share_i / (num_already_allocated_i + 1)
                    Note: an absolute majority always lead to an absolute majority in seats (favors large groups)

                - Webster : divisor_i = share_i / ((2 * num_already_allocated_i) + 1)
                    Note: generally the smallest deviation from ideal shares (favors medium groups)

                - Huntington-Hill : divisor_i = share_i / sqrt(num_already_allocated_i * (num_already_allocated_i + 1))
                    Note: assures that all regions or parties receive at least one vote (favors smalle groups)

    Returns
    -------
        allocations : list
            A list of allocated seats in the order of provided populations or votes
    """
    assert allocation_threshold == None or min_allocation == None, \
        """Appointment methods cannot be used with both an entry threshold and a minimum seat allocation. 
        Set one of allocation_threshold or min_allocation to None"""

    assert allocation_threshold == None or averaging_style != 'Huntington-Hill', \
        """The Huntington-Hill method requires all groups to receive a seat, and thus cannot be used with a threshold."""

    if allocation_threshold:
        passed_threshold = [True if 1.0 * i / sum(counts) > allocation_threshold else False for i in counts]
        counts = [counts[i] if passed_threshold[i] == True else 0 for i in range(len(counts))]

    if min_allocation:
        assert min_allocation * len(counts) <= total_seats, "The sum of the minimum seats to be allocated cannot be more than the seats to be allocated."
        allocations = [min_allocation] * len(counts)
        
        remaining_seats = total_seats - sum(allocations)
    
        if remaining_seats == 0:
            return allocations
    else:
        allocations = [0] * len(counts)
    
    while sum(allocations) < total_seats:

        if averaging_style == 'Jefferson':
            if modifier:
                quotients = [1.0 * count / (allocations[idx] + 1) if allocations[idx] + 1 > 1 else 1.0 * count / modifier \
                    for idx, count in enumerate(counts)]
            else:
                quotients = [1.0 * count / (allocations[idx] + 1) for idx, count in enumerate(counts)]

        elif averaging_style == 'Webster':
            if modifier:
                quotients = [1.0 * count / ((2 * allocations[idx]) + 1) if allocations[idx] + 1 > 1 else 1.0 * count / modifier \
                    for idx, count in enumerate(counts)]
            else:
                quotients = [1.0 * count / ((2 * allocations[idx]) + 1) for idx, count in enumerate(counts)]

        elif averaging_style == 'Huntington-Hill':
            if not min_allocation or min_allocation == 0:
                assert len(counts) <= total_seats, "There must be at least one seat per group when using the Huntington-Hill method."
                print("A minimum allocation is required for Huntington-Hill's calculations. A minimum allocation of 1 will now be applied.")
                allocations = [1] * len(counts)
                total_seats -= sum(allocations)

            if modifier:
                quotients = [1.0 * count / sqrt(allocations[idx] * (allocations[idx] + 1)) if allocations[idx] + 1 > 1 else 1.0 * count / modifier \
                    for idx, count in enumerate(counts)]
            else:
                quotients = [1.0 * count / sqrt(allocations[idx] * (allocations[idx] + 1)) for idx, count in enumerate(counts)]

        else:
            print("{} is not a supported highest average method. Please choose from 'Jefferson', 'Webster', or 'Huntington-Hill'".format(averaging_style))
            print("""Naming conventions for methods differ across regions, with US naming conventions used.

                    US assignment method name conversions:
                    Jeffersion         : D'Hondt, Hagenbach-Bischoff (includes entry quota)
                    Webster            : Sainte-Laguë, Major Fraction
                    Huntington-Hill    : Equal Preportions""")
            
            return

        max_quotient_indexes = [q[0] for q in enumerate(quotients) if q[1] == max(quotients)]
        
        # Normal assignment
        if len(max_quotient_indexes) < total_seats:
            idx_max = quotients.index(max(quotients))
            allocations[idx_max] += 1

        # Tie break conditions
        elif len(max_quotient_indexes) >= total_seats:
            if tie_break == 'majority':
                sorted_by_results = [i[0] for i in sorted(enumerate(counts), key=itemgetter(1)) if i[0] in max_quotient_indexes][::-1]
                equal_to_highest = [i for i in sorted_by_results if sorted_by_results[i] == sorted_by_results[0]]
                
                if len(equal_to_highest) == 1: 
                    allocations[sorted_by_results[0]] += 1

                else:
                    # Defaults to random for those with equal allocation and remainder
                    sorted_by_results[sorted_by_results.index(equal_to_highest[0]) : sorted_by_results.index(equal_to_highest[-1]) + 1] = \
                        sample(sorted_by_results[sorted_by_results.index(equal_to_highest[0]) : sorted_by_results.index(equal_to_highest[-1]) + 1], len(equal_to_highest))
                    
                    allocations[sorted_by_results[0]] += 1

            elif tie_break == 'random':
                shuffle(max_quotient_indexes)
                allocations[max_quotient_indexes[0]] += 1

            else:
                ValueError("A tie break is required for the last seat(s), and an invalid argument has been passed. Please choose from 'majority' or 'random'.")
        
        total_seats -= 1

    if majority_bonus:
        # If a single majority group does not receive at least 50%, then they are given it, and assignment is redone for the rest
        if not allocations[counts.index(max(counts))] >= int(ceil(total_seats / 2)) and len([count for count in counts if count == max(counts)]) == 1:
            non_majority_counts = [count for count in counts if count != max(counts)]
            reduced_seats = total_seats - int(ceil(total_seats / 2))
            non_majority_allocations = highest_average(counts=non_majority_counts, total_seats=reduced_seats, 
                                                       allocation_threshold=allocation_threshold, min_allocation=min_allocation, 
                                                       tie_break=tie_break, majority_bonus=False, 
                                                       modifier=modifier, averaging_style=averaging_style)

            # Insert majority allocation
            non_majority_allocations[counts.index(max(counts)) : counts.index(max(counts))] = [int(ceil(total_seats / 2))]
            allocations = non_majority_allocations

    return allocations