from models import Company


class CompanyServices:

    def getByID(id):
        return Company.query.get(id)

