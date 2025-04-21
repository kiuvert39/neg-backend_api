from flask_restx import Namespace, Resource, fields
from app.services.footer import FooterService

api = Namespace('footer', description='Footer related operations')

social_links_model = api.model('SocialLinks', {
    'linkedin': fields.String,
    'instagram': fields.String,
    'facebook': fields.String
})

footer_model = api.model('Footer', {
    'brandName': fields.String(required=True),
    'address': fields.String(required=True),
    'email': fields.String(required=True),
    'phone': fields.String(required=True),
    'legalNoticeLink': fields.String(required=True),
    'socialLinks': fields.Nested(social_links_model)
})

@api.route('/create')
class FooterResource(Resource):
    @api.expect(footer_model)
    def post(self):
        """Create or update footer"""
        data = api.payload
        FooterService.save_footer(data)
        return {"message": "Footer saved successfully"}, 201
    
@api.route('/')
class FooterResource(Resource):
    @api.marshal_with(footer_model)
    def get(self):
        """Get footer data"""
        return FooterService.get_footer()