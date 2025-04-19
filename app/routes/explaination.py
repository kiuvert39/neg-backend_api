from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.explaination import ExplainationService

explaination_ns = Namespace("explaination", description="Hero Section Content")

explaination_model = explaination_ns.model("Explaination", {
    "title": fields.String(required=True),
    "description1": fields.String(required=True),
    "description2": fields.String(required=True),
    "buttonText": fields.String(required=True),
    "buttonLink": fields.String(required=True),
})


@explaination_ns.route('/create')
class ExplainationCreate(Resource):
    @explaination_ns.expect(explaination_model)
    @explaination_ns.response(201, "Created")
    def post(self):
        """Create new explaination"""
        data = request.get_json()
        explaination = ExplainationService.create_explaination(data)
        return explaination.to_dict(), 201
    

@explaination_ns.route('/')
class ExplainationLatest(Resource):
    @explaination_ns.response(200, "Success")
    @explaination_ns.response(404, "Not Found")
    def get(self):
        """Get the latest explaination"""
        explaination = ExplainationService.get_latest_explaination()
        if explaination:
            return explaination.to_dict(), 200
        return {"message": "No explaination found"}, 404


@explaination_ns.route('/<string:explaination_id>')
class ExplainationUpdate(Resource):
    @explaination_ns.expect(explaination_model)
    @explaination_ns.response(200, "Updated")
    @explaination_ns.response(404, "Not Found")
    def put(self, explaination_id):
        """Update existing explaination"""
        data = request.get_json()
        updated = ExplainationService.update_explaination(explaination_id, data)
        if updated:
            return updated.to_dict(), 200
        return {"message": "Explaination not found or not updated"}, 404