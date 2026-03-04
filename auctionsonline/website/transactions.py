from website.models import UserDetails, Auction, Bid
from django.utils import timezone
from datetime import datetime

from decimal import Decimal


def increase_bid(user, auction, bid_cost):
    """
    Removes the current bid cost from user.
    Creates a Bid record
    Increases the auction's number of bids

    Parameters
    ----------
    user : User object
    auction : class 'website.models.Auction'
    bid_cost : Decimal - current cost of the bid
    """
    # Fetch the UserDetails associated with the user
    userDetails = UserDetails.objects.get(user_id=user.id)
    # Deduct the current bid cost from the user's balance
    userDetails.balance -= bid_cost
    userDetails.save()  # Save the updated balance to the database

    # Create a new Bid record
    bid = Bid.objects.create(user_id=user, auction_id=auction, bid_time=timezone.now())

    # Increase the auction's number of bids
    auction.number_of_bids += 1
    auction.save()


def remaining_time(auction):
    """
    Calculates the auction's remaining time
    in minutes and seconds and converts them 
    into a string.
    
    Parameters
    ----------
    auction : class 'website.models.Auction
    
    Returns
    -------
    
    time_left : str
        string representation of remaining time in
        days, hours, minutes and seconds.
    expired : int
        if the value is less than zero then the auction ended.
    
    """
    time_left = auction.time_ending - timezone.now()
    days, seconds = time_left.days, time_left.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    # Format time string based on remaining time
    if days > 0:
        time_left = f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        time_left = f"{hours}h {minutes}m {seconds}s"
    else:
        time_left = f"{minutes}m {seconds}s"
    
    expired = days

    return time_left, expired
