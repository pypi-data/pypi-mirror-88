# =============================================================================
# Utility functions to analyze the results of elections
#
# Based on
# --------
#   Kohler, U., and Zeh, J. (2012). “Apportionment methods”. 
#   The Stata Journal, Vol. 12, No. 3, pp. 375–392. 
#   URL: https://journals.sagepub.com/doi/pdf/10.1177/1536867X1201200303
# 
# Contents
# --------
#   0. No Class
#       ideal_share
#
#       seat_to_share_ratio
#       sqr_seat_to_share_error
#       total_seat_to_share_error
#
#       representative_weight
#       sqr_rep_weight_error
#       total_rep_weight_error
#
#       effective_number_of_parties
#       diversity_index
#       disproportionality_index
# =============================================================================

def ideal_share(share, total_shares, total_seats):
    """
    Calculate the ideal share to be allocated to a region or party
        
    Parameters
    ----------   
        share : int
            The preportion of the population or votes for a region or party
        
        total_shares : int 
            The total population or votes

        total_seats : int
            The number of seats to apportion

    Returns
    -------
        ideal : float
            The ideal share that the region or party would receive given fractional allocation
    """
    ideal = 1.0 * share / total_shares * total_seats

    return ideal


def seat_to_share_ratio(share, total_shares, seats, total_seats):
    """
    Calculate the seat to share (advantage) ratio allocated to a region or party
        
    Parameters
    ----------   
        share : int
            The preportion of the population or votes for a region or party
        
        total_shares : int 
            The total population or votes

        seats : int
            The share of seats given to the region or party

        total_seats : int
            The number of seats to apportion

    Returns
    -------
        ssr : float
            The ratio of the seats the region or party received to their preportion of the population or votes
    """
    ssr = 1.0 * (seats / total_seats) / (share / total_shares)
    
    return ssr


def sqr_seat_to_share_error(share, total_shares, seats, total_seats):
    """
    Calculate the squared error of an assignment's seat to share ratio for a population or party
        
    Parameters
    ----------   
        share : int
            The preportion of the population or votes for a region or party
        
        total_shares : int 
            The total population or votes

        seats : int
            The share of seats given to the region or party

        total_seats : int
            The number of seats to apportion

    Returns
    -------
        sqr_ssr_err : float
            The squared of the error of the seat to share ratio 
    """
    ssr = seat_to_share_ratio(share=share, total_shares=total_shares, 
                              seats=seats, total_seats=total_seats)
    sqr_ssr_err = (ssr - 1) ** 2

    return sqr_ssr_err


def total_seat_to_share_error(all_shares, all_seats, preportional=True):
    """
    Calculate the total squared error of an assignment's seat to share ratio
        
    Parameters
    ----------   
        all_shares : list
            The preportion of the population or votes for the regions or parties

        all_seats : list
            The share of seats given to the regions or parties

        preportional : bool (default=False)
            Whether the assignment's error is calculated as preportional to the region or party shares

    Returns
    -------
        total_ssr_err : float
            The summation of the seat to share ratio error for all populations or parties
    """
    assert len(all_shares) == len(all_seats), 'The total different shares of a population or vote must equal that of the allocated seats.'
    
    sum_share = sum(all_shares)
    sum_seats = sum(all_seats)

    sqr_ssr_errors = [sqr_seat_to_share_error(share=all_shares[i], total_shares=sum_share, 
                                              seats=all_seats[i], total_seats=sum_seats) for i in range(len(all_shares))]

    if preportional:
        preportional_errors = [all_shares[i] / sum_share * sqr_ssr_errors[i] for i in range(len(all_shares))]
        total_ssr_err = sum(preportional_errors)

    else:
        total_ssr_err = sum(sqr_ssr_errors)
    
    return total_ssr_err


def representative_weight(share, seats):
    """
    Calculate the representative weight of an allocation to a region or party
        
    Parameters
    ----------   
        share : int
            The preportion of the population or votes for a region or party

        seats : int
            The share of seats given to the region or party

    Returns
    -------
        rep_weight : float
            The number of people per seat for a population or party
    """
    rep_weight = share / seats
    
    return rep_weight


def sqr_rep_weight_error(share, total_shares, seats, total_seats):
    """
    Calculate the squared error of an assignment's representative weight for a population or party
        
    Parameters
    ----------   
        share : int
            The preportion of the population or votes for a region or party
        
        total_shares : int 
            The total population or votes

        seats : int
            The share of seats given to the region or party

        total_seats : int
            The number of seats to apportion

    Returns
    -------
        sqr_rw_err : float
            The squared of the error of the seat to share ratio 
    """
    rep_weight = representative_weight(share=share, seats=seats)
    
    sqr_rw_err = (rep_weight - total_shares / total_seats) ** 2
    
    return sqr_rw_err


def total_rep_weight_error(all_shares, all_seats, preportional=True):
    """
    Calculate the total squared error of an assignment's representative weight error
        
    Parameters
    ----------   
        all_shares : list
            The preportion of the population or votes for the regions or parties

        all_seats : list
            The share of seats given to the regions or parties

        preportional : bool (default=False)
            Whether the assignment's error is calculated as preportional to the region or party shares

    Returns
    -------
        total_rw_err : float
            The summation of the representative weight error for all populations or parties
    """
    assert len(all_shares) == len(all_seats), 'The total different shares of a population or vote must equal that of the allocated seats.'
    
    sum_share = sum(all_shares)
    sum_seats = sum(all_seats)

    sqr_rw_errors = [sqr_rep_weight_error(share=all_shares[i], total_shares=sum_share, 
                                          seats=all_seats[i], total_seats=sum_seats) for i in range(len(all_shares))]

    if preportional:
        preportional_errors = [all_shares[i] / sum_share * sqr_rw_errors[i] for i in range(len(all_shares))]
        total_rw_err = sum(preportional_errors)

    else:
        total_rw_err = sum(sqr_rw_errors)
    
    return total_rw_err