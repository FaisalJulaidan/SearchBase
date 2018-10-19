from config import BaseConfig


from models import db, Callback, BlockLabel

def getByCompanyID(companyID):
    try:
        result = db.session.query(BlockLabel).filter(BlockLabel.CompanyID == companyID).all()

        return Callback(True, "Labels retrieved successfully", result)

    except Exception as exc:
        print("questionLabels_services.getLabelsByCompanyID Error: ", exc)
        db.session.rollback()
        return Callback(False, "Labels could not be retrieved at this time")

def addLabel(text, colour, companyID):
    try:
        labels = BlockLabel(Text=text, Colour=colour, CompanyID=companyID)
        db.session.add(labels)
        # Save
        db.session.commit()
        return Callback(True, 'Label has ben created successfully!')
    except Exception as exc:
        print("questionLabels_services.addLabel Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Failed to create the label')

def editLabelByID(id, text, colour):
    try:
        db.session.query(BlockLabel).filter(BlockLabel.ID == id).update({'Text': text, 'Colour': colour})
        db.session.commit()
        return Callback(True, 'Label updated successfully')

    except Exception as exc:
        print("blockLabels_services.editLabelByID ERROR: ", exc)
        db.session.rollback()
        return Callback(False, "Couldn't update label ")


def deleteByID(id):
    try:
        db.session.query(BlockLabel).filter(BlockLabel.ID == id).delete()
        db.session.commit()
        return Callback(True, 'Label has been deleted.')

    except Exception as exc:
        print("questionLabels_services.deleteLabelByID Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Error in deleting label.')

def deleteAllByCompanyID(companyID):
    try:
        db.session.query(BlockLabel).filter(BlockLabel.CompanyID == companyID).delete()
        db.session.commit()
        return Callback(True, 'Labels have been deleted.')

    except Exception as exc:
        print("questionLabels_services.deleteLabelByCompanyID Error: ", exc)
        db.session.rollback()
        return Callback(False, 'Error in deleting labels.')
