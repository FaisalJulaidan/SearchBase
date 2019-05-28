from sqlalchemy import and_
from models import db, Callback, AutoPilot, OpenTimeSlot
from datetime import time
import logging


def create(companyID: int) -> Callback:
    try:

        autoPilot= AutoPilot(CompanyID=companyID) # Create new AutoPilot

        # With default open time slots for all days of the week
        default = {"From": time(8,30), "To": time(12,0), "Duration": 30, "AutoPilot": autoPilot, "Active": True}
        openTimeSlots = [OpenTimeSlot(Day=0, **default), # Monday
                         OpenTimeSlot(Day=1, **default),
                         OpenTimeSlot(Day=2, **default),
                         OpenTimeSlot(Day=3, **default),
                         OpenTimeSlot(Day=4, **default),
                         OpenTimeSlot(Day=5, **default),
                         OpenTimeSlot(Day=6, **default), # Sunday
                         ]
        db.session.add_all(openTimeSlots)
        db.session.commit()

    except Exception as exc:
        print(exc)
        logging.error("auto_pilot.create(): " + str(exc))
        db.session.rollback()
        return Callback(False, 'Could create AutoPilot.')


def getByID(id: int, companyID: int) -> Callback:
    try:
        # Get result and check if None then raise exception
        result = db.session.query(AutoPilot) \
            .filter(and_(AutoPilot.ID == id, AutoPilot.CompanyID == companyID)).first()
        if not result: raise Exception
        return Callback(True, "Got AutoPilot successfully.", result)

    except Exception as exc:
        print(exc)
        logging.error("auto_pilot.getByID(): " + str(exc))
        return Callback(False, 'Could not get the assistant.')


def update(id, companyID, active, acceptApplications, acceptanceScore, rejectApplications,
           rejectionScore, sendCandidatesAppointments) -> Callback:
    try:

        db.session.query(AutoPilot).filter(and_(AutoPilot.ID == id, AutoPilot.CompanyID == companyID))\
            .update({
                'Active': active,
                'AcceptApplications': acceptApplications,
                'AcceptanceScore': acceptanceScore,
                'RejectApplications': rejectApplications,
                "RejectionScore": rejectionScore,
                "SendCandidatesAppointments": sendCandidatesAppointments,
                   })
        db.session.commit()
        return Callback(True, 'AutPilot updated Successfully')

    except Exception as exc:
        print(exc)
        db.session.rollback()
        logging.error("auto_pilot.update(): " + str(exc))
        return Callback(False,"Couldn't update AutPilot " + str(id))

def fetchOpenTimeSlots(autoPilotID, companyID):
    pass