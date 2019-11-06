from services import assistant_services, user_services
from models import Callback, ShortenedURL, db
from utilities import helpers
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

min_key_length = 5


def createShortenedURL(url: str, length: int = min_key_length, expiry: int = None, key: str = None, subdomain: str = None, domain: str = None) -> Callback:
    """
    Creates a shortened url that points to the one supplied

    Args:
        url [str] -- The url the shortened URL will point to
        length [int] [OPTIONAL] -- The length of the alphanumeric key at the end of the URL (min-5)
        expiry [int] [OPTIONAL] -- The length of time in seconds after which the link will no longer redirect, None for no expiry (None is default)
        key [str] [OPTIONAL] -- The key (overriding the random text) that will be at the end of the URL, the length parameter will be ignored if this is supplied
        subdomain [str] [OPTIONAL] -- The subdomain to be supplied to the domain helper function
        domain [str] [OPTIONAL] -- The domain to be supplied to the domain helper function

    Returns:
        Callback with either a success or failure status, with the data object pointing to the newly created URL

    Raises:
        TODO: Write exceptions
    """

    # IF length is supplied (Default 10), check if less than min_key_length
    if(length < min_key_length):
        raise Exception("The length supplied was less than the {} minimum".format(min_key_length))

    # IF key is supplied, check if its less than min_key_length
    if(key):
        if(len(key) < min_key_length):
            raise Exception("The length supplied was less than the {} minimum".format(min_key_length))

    # Expiry parameter must be 0 at minimum
    if(expiry):
        if(expiry < 0):
            raise Exception("Expiry can not be less than 0")
    
    try:
        key = key if key else helpers.randomAlphanumeric(length)
        expiryDate = datetime.now() + timedelta(seconds=expiry) if expiry else None
        shortened_url : ShortenedURL = ShortenedURL(ID=key, URL=url, Expiry=expiryDate)

        db.session.add(shortened_url)
        db.session.commit()

        return Callback(True, "URL has been succesfully created", "{}/u/{}".format(helpers.getDomain(subdomain=subdomain, domain=domain), key))

    except IntegrityError as e:
        helpers.logError("url_services.createShortenedURL(): " + str(e))
        db.session.rollback()
        return Callback(False, "Integrity error, a key used in a different URL is being attempted to be used again")

    except Exception as e:
        helpers.logError("url_services.createShortenedURL(): " + str(e))
        db.session.rollback()
        return Callback(False, "Unknown error.")

    # Check if key exists, query database to make sure its not a duplicate

def getByKey(key: str) -> Callback:
    """
    Gets a shortened URL by key

    Args:
        key [str] -- Unique key for the shortened URL you would like

    Returns:
        Callback with either a success or failure status, with the data object pointing to the shortened URL

    Raises:
        TODO: Write exceptions
    """

    try:
        urlshortener = db.session.query(ShortenedURL).filter(ShortenedURL.ID == key).first()
        if urlshortener is None:
            raise Exception('Key {} does not exist in our database'.format(key))

        if(urlshortener.Expiry):
            if(urlshortener.Expiry < datetime.now()):
                raise Exception('Expiry date for key {} has passed'.format(key))

        return Callback(True, "URL Found", urlshortener.URL)

    except Exception as e:        
        helpers.logError("url_services.getByKey(): " + str(e))
        return Callback(False, "Unknown error.")