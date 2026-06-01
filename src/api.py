from flask import Flask, request, jsonify
from repository import LeadRepository, LeadNotFoundError, DuplicateLeadError

app = Flask(__name__)
repo = LeadRepository()

# Global Error Handlers (Requirement FR-8)
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

# 1. Retrieve a single lead (Requirement FR-3)
@app.route('/api/v1/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    try:
        lead = repo.get(lead_id)
        return jsonify(lead), 200
    except LeadNotFoundError as e:
        return jsonify({"error": str(e)}), 404

# 2. List leads with filtering and pagination (Requirements FR-1 & FR-2)
@app.route('/api/v1/leads', methods=['GET'])
def list_leads():
    # Get query parameters
    stage_filter = request.args.get('stage')
    source_filter = request.args.get('source')
    
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        if page < 1 or limit < 1:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Page and limit must be positive integers"}), 400

    leads = repo.list()
    
    # Apply filters
    if stage_filter:
        leads = [l for l in leads if l['stage'].lower() == stage_filter.lower()]
    if source_filter:
        leads = [l for l in leads if l['source'].lower() == source_filter.lower()]
        
    # Apply pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_leads = leads[start_idx:end_idx]
    
    return jsonify({
        "data": paginated_leads,
        "page": page,
        "limit": limit,
        "total": len(leads)
    }), 200

# 3. Create a lead (Requirements FR-4 & FR-7)
@app.route('/api/v1/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
        
    name = data.get('name')
    phone = data.get('phone')
    
    if not name or not phone:
        return jsonify({"error": "Name and phone are required fields"}), 400
        
    try:
        lead_id = repo.create(
            name=name,
            phone=phone,
            source=data.get('source', ''),
            stage=data.get('stage', 'New'),
            notes=data.get('notes', '')
        )
        return jsonify({"id": lead_id, "message": "Lead created successfully"}), 201
    except DuplicateLeadError as e:
        return jsonify({"error": str(e)}), 400

# 4. Update a lead's stage (Requirement FR-5)
@app.route('/api/v1/leads/<int:lead_id>/stage', methods=['PATCH'])
def update_stage(lead_id):
    data = request.get_json()
    
    if not data or 'stage' not in data:
        return jsonify({"error": "Request body must contain 'stage'"}), 400
        
    new_stage = data['stage']
    
    try:
        repo.update_stage(lead_id, new_stage)
        return jsonify({"message": f"Stage updated to {new_stage}"}), 200
    except LeadNotFoundError as e:
        return jsonify({"error": str(e)}), 404

# 5. Delete a lead (Requirement FR-6)
@app.route('/api/v1/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    try:
        repo.delete(lead_id)
        return '', 204
    except LeadNotFoundError as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)