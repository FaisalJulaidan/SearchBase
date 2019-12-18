from datetime import datetime
import time
from models import Callback, ShortenedURL, db
from utilities import helpers
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

min_key_length = 5


def createShortenedURL(url: str, expiry: int = None, key: str = None, subdomain: str = None, domain: str = None,
                       autoSave=True, index=1) -> Callback:
    """
    Creates a shortened url that points to the one supplied

    Args:
        url [str] -- The url the shortened URL will point to
        length [int] [OPTIONAL] -- The length of the alphanumeric key at the end of the URL (min-5)
        expiry [int] [OPTIONAL] -- The length of time in seconds after which the link will no longer redirect, None for no expiry (None is default)
        key [str] [OPTIONAL] -- The key (overriding the random text) that will be at the end of the URL, the length parameter will be ignored if this is supplied
        subdomain [str] [OPTIONAL] -- The subdomain to be supplied to the domain helper function
        domain [str] [OPTIONAL] -- The domain to be supplied to the domain helper function
        autoSave [bool] [OPTIONAL] -- either add the records to the database and commit/save changes
        index [int] [OPTIONAL] -- used when generating big number of urls to ensure uniqueness

    Returns:
        Callback with either a success or failure status, with the data object pointing to the newly created SQLAlchemy
        URL and the url as a string

    Raises:
        TODO: Write exceptions
    """

    # Expiry parameter must be 0 at minimum
    if (expiry):
        if (expiry < 0):
            raise Exception("Expiry can not be less than 0")

    try:
        expiryDate = datetime.now() + timedelta(seconds=expiry) if expiry else None
        shortened_url: ShortenedURL = ShortenedURL(ID=helpers.encodeID((time.time_ns() + index)),
                                                   URL=url,
                                                   Expiry=expiryDate)

        if autoSave:
            db.session.add(shortened_url)
            db.session.commit()

        return Callback(True, "URL has been successfully created",
                        {
                            "url": "{}/u/{}".format(helpers.getDomain(subdomain=subdomain, domain=domain), key),
                            "object": shortened_url
                        })

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
        shortenedURL = db.session.query(ShortenedURL).filter(ShortenedURL.ID == key).first()

        if shortenedURL is None:
            raise Exception('Key {} does not exist in our database'.format(key))

        if (shortenedURL.Expiry):
            if (shortenedURL.Expiry < datetime.now()):
                raise Exception('Expiry date for key {} has passed'.format(key))

        url = shortenedURL.URL
        # redirect to tsb url
        if shortenedURL.URL.startswith("/"):
            url = helpers.getDomain() + shortenedURL.URL

        return Callback(True, "URL Found", url)

    except Exception as e:
        helpers.logError("url_services.getByKey(): " + str(e))
        return Callback(False, "Unknown error.")
