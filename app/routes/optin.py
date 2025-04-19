import traceback
from flask import json, jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_pydantic import validate

from app.schema.dashboard_schema import DashboardSchema
from app.services.optin_service import DashboardService

dashboard_ns = Namespace('dashboard', description='Dashboard related operations')


# Optional: Swagger model for request example (simplified)
dashboard_input = dashboard_ns.model('DashboardInput', {
    'heroTitle': fields.String(required=True),
    'heroHighlight': fields.String(required=True),
    'heroDescription': fields.String(required=True),
    'testimonials': fields.List(fields.Raw),
    'teamMembers': fields.List(fields.Raw),
    'galleryImages': fields.List(fields.String)  # Only used if sending base64 or URLs (not files)
})


@dashboard_ns.route('/create')
class DashboardCreate(Resource):

    @dashboard_ns.doc('create_dashboard')
    def post(self):
        try:
            # Extract the JSON string from the 'data' field
            data_str = request.form.get('data')
            if not data_str:
                return {"error": "Missing 'data' field"}, 400

            # Try to parse the JSON string
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON format in 'data'"}, 400

            # Get uploaded files
            team_images = []
            gallery_images = []

            for key in request.files:
                if key.startswith('teamMembersImages['):
                    team_images.append(request.files[key])
                elif key.startswith('galleryImages['):
                    gallery_images.append(request.files[key])

            if not team_images or not gallery_images:
                return {"error": "Missing required image uploads"}, 400

            # Delegate to service layer
            result = DashboardService.create_dashboard(data, team_images, gallery_images)

            if isinstance(result, tuple):
                return result[0], result[1]

            return result, 201

        except Exception as e:
            traceback.print_exc()
            print("Error creating dashboard:", e)
            return {"error": "Internal server error"}, 500
        


@dashboard_ns.route('/')
class LatestDashboardResource(Resource):
    def get(self):
        return DashboardService.get_dashboard()