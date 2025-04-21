from app.models.footer_model import FooterModel

class FooterService:
    @staticmethod
    def save_footer(data):
        return FooterModel.update(data)

    @staticmethod
    def get_footer():
        return FooterModel.get()
