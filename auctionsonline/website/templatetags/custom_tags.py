from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='search')
def search(value, id):
    """
    Linear search of a list

    Parameters
    ----------
    value : list
        A list with key values
    id : int
        The key we are searching
    
    Returns
    ------
    boolean
        True if the key is found, False otherwise.
    """
    for v in value:
        if v.id == id:
            return True
    
    return False

@register.filter(name="time_left")
def time_left(value):
    """
    Calculates the remaining time by
    subtracting the deadline with the 
    current time and converts it to 
    string with days, hours, minutes, seconds format. 

    Parameters
    ----------
    value : DateTime
        The deadline
    
    Returns
    ------
    string
        Remaining time in days, hours, minutes and seconds
    """
    t = value - timezone.now()
    days, seconds = t.days, t.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    # Format based on remaining time
    if days > 0:
        st = f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        st = f"{hours}h {minutes}m {secs}s"
    else:
        st = f"{minutes}m {secs}s"
    
    return st

@register.filter(name="current_price")
def current_price(value):
    """
    Calculates the current value
    of the item depending the
    number of bids and starting price.

    Parameters
    ----------
    value : Auction object
        Auction with starting_price and number_of_bids.
    
    Returns
    ------
    string
        Current value with two decimals.
    """
    current_cost = float(value.starting_price) + (value.number_of_bids * 0.20)
    current_cost = "%0.2f" % current_cost
    return current_cost

