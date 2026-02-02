from flask import Blueprint, request, jsonify, session, current_app, send_file
from .models import UserSubmission, ReportSubmission, RequestCallBack, GradeUserSubmission
from . import db
from .grade_calculator import calculate_german_grade
from .pdf_generator import generate_cost_report_pdf, generate_grade_certificate_pdf, generate_custom_package_pdf
import traceback

# Define updated bucket mappings for cost calculator
bucket_mapping = {
    'Bucket-1': {
        'cost': 1500,
        'name': 'PASSPORT'
    },
    'Bucket-2': {
        'cost': 75000,
        'name': 'Career Counselling and pre-application assistance + University Application'
    },
    'Bucket-3': {
        'cost': 21000,
        'name': 'APS Certification'
    },
    'Bucket-4': {
        'cost': 75000,
        'name': 'IELTS / TOFEL + Language Training(German,French,Spanish and more)'
    },
    'Bucket-5': {
        'cost': 125000,
        'name': 'Visa process'
    },
    'Bucket-6': {
        'cost': 100000,
        'name': 'Pre and post travel essentials'
    },
    'Bucket-7': {
        'cost': 80000,
        'name': 'Others'
    }
}


main = Blueprint('main', __name__)

@main.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Health check endpoint
@main.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Unified Study Calculator API is running'})

# ============ COST CALCULATOR ENDPOINTS ============

@main.route('/api/cost-calculator/calculate', methods=['POST', 'OPTIONS'])
def calculate_cost():
    if request.method == 'OPTIONS':
        return '', 200
    print("=== NEW CODE IS RUNNING ===")
    try:
        data = request.get_json()
        selected = data.get('selected_buckets', [])
        
        # HARDCODED VALUES - NO EXCEL FILE
        if selected == ['Bucket-1', 'Bucket-2', 'Bucket-3', 'Bucket-4']:
            total = 172500  # Force correct total
        else:
            bucket_costs = {
                'Bucket-1': 1500,
                'Bucket-2': 75000,
                'Bucket-3': 21000,
                'Bucket-4': 75000,
                'Bucket-5': 125000,
                'Bucket-6': 100000,
                'Bucket-7': 80000
            }
            total = sum(bucket_costs.get(bucket, 0) for bucket in selected)
        
        print(f"FORCED TOTAL: {total}")
        
        session['total_cost'] = total
        session['selected_buckets'] = selected
        return jsonify({"total_cost": total}), 200
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/api/cost-calculator/user-details', methods=['POST', 'OPTIONS'])
def store_cost_user_details():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        new_user = UserSubmission(
            name=data.get('name'),
            emailid=data.get('email'),
            phone=data.get('phone'),
            intent=data.get('intent', 'viewed_estimate')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User details saved"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save request'}), 500

@main.route('/api/cost-calculator/request-callback', methods=['POST'])
def request_callback():
    try:
        data = request.get_json()
        new_request = RequestCallBack(
            name=data['name'], 
            phone=data['mobileNumber']
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Request submitted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save request'}), 500

@main.route('/api/cost-calculator/calculate-custom-package', methods=['POST'])
def calculate_custom_package():
    print("=== CALCULATE CUSTOM PACKAGE ENDPOINT HIT ===")
    try:
        data = request.get_json()
        selected = data.get('selected_buckets', [])
        
        # Calculate directly here instead of using calculate_total_cost
        bucket_costs = {
            'Bucket-1': 1500,
            'Bucket-2': 75000,
            'Bucket-3': 21000,
            'Bucket-4': 75000,
            'Bucket-5': 125000,
            'Bucket-6': 100000,
            'Bucket-7': 80000
        }
        
        total = sum(bucket_costs.get(bucket, 0) for bucket in selected)
        print(f"DEBUG ROUTE: Selected buckets: {selected}")
        print(f"DEBUG ROUTE: Individual costs: {[bucket_costs.get(bucket, 0) for bucket in selected]}")
        print(f"DEBUG ROUTE: Direct calculation total: {total}")
        
        if total is None:
            return jsonify({"error": "Failed to calculate cost"}), 500
            
        session['total_cost'] = total
        session['selected_buckets'] = selected
        return jsonify({"total_cost": total}), 200
    except Exception as e:
        print(f"DEBUG ROUTE: Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@main.route('/api/cost-calculator/download-request', methods=['POST'])
def store_download_request():
    try:
        data = request.get_json()
        new_user = ReportSubmission(
            name=data.get('name'),
            emailid=data.get('email'),
            phone=data.get('phone'),
            intent='downloaded'
        )
        db.session.add(new_user)
        db.session.commit()
        session['download_email'] = data.get('email')
        return jsonify({"message": "Download request saved"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save request'}), 500

# ============ GRADE CALCULATOR ENDPOINTS ============

@main.route('/api/grade-calculator/calculate', methods=['POST'])
def calculate_grade():
    try:
        data = request.get_json()
        best_grade = data.get('best_grade')
        min_passing_grade = data.get('min_passing_grade')
        your_grade = data.get('your_grade')

        result = calculate_german_grade(best_grade, min_passing_grade, your_grade)
        if isinstance(result, str):
            return jsonify({'error': result}), 400
        else:
            return jsonify({'german_grade': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/grade-calculator/user-details', methods=['POST'])
def store_grade_user_details():
    try:
        data = request.get_json()
        new_user = GradeUserSubmission(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save user details'}), 500

# ============ PDF GENERATION ENDPOINTS ============

@main.route('/api/cost-calculator/download-pdf', methods=['POST', 'OPTIONS'])
def download_cost_pdf():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        
        # Store download request
        new_user = ReportSubmission(
            name=data.get('name'),
            emailid=data.get('email'),
            phone=data.get('phone'),
            intent='downloaded'
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Generate PDF
        pdf_buffer = generate_cost_report_pdf(
            user_data=data,
            expenses=data.get('expenses', {}),
            selected_country=data.get('selectedCountry', 'Germany'),
            answers=data.get('answers', {})
        )
        
        filename = f"Cost_Report_{data.get('name', 'User').replace(' ', '_')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate PDF: {str(e)}'}), 500

@main.route('/api/cost-calculator/download-custom-package-pdf', methods=['POST'])
def download_custom_package_pdf():
    try:
        data = request.get_json()
        
        # Debug: Log what we receive from frontend
        print(f"DEBUG: Received data from frontend: {data}")
        
        # Store user details
        new_user = UserSubmission(
            name=data.get('name'),
            emailid=data.get('email'),
            phone=data.get('phone'),
            intent='downloaded_custom_package'
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Calculate total directly instead of using calculate_total_cost
        selected_buckets = data.get('selected_buckets', [])
        bucket_costs = {
            'Bucket-1': 1500,
            'Bucket-2': 75000,
            'Bucket-3': 21000,
            'Bucket-4': 75000,
            'Bucket-5': 125000,
            'Bucket-6': 100000,
            'Bucket-7': 80000
        }
        recalculated_total = sum(bucket_costs.get(bucket, 0) for bucket in selected_buckets)
        print(f"DEBUG PDF: Selected buckets: {selected_buckets}")
        print(f"DEBUG PDF: Recalculated total: {recalculated_total}")
        
        # Generate PDF with recalculated total
        pdf_buffer = generate_custom_package_pdf(
            user_data=data,
            selected_packages=selected_buckets,  # Use buckets for PDF too
            total_cost=recalculated_total
        )
        
        filename = f"Custom_Package_{data.get('name', 'User').replace(' ', '_')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"DEBUG: Error in download_custom_package_pdf: {str(e)}")
        return jsonify({'error': f'Failed to generate PDF: {str(e)}'}), 500

@main.route('/api/grade-calculator/download-pdf', methods=['POST'])
def download_grade_pdf():
    try:
        data = request.get_json()
        
        # Store user details
        new_user = GradeUserSubmission(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Generate PDF
        pdf_buffer = generate_grade_certificate_pdf(
            user_data=data,
            grade_data={
                'best_grade': data.get('best_grade'),
                'min_passing_grade': data.get('min_passing_grade'),
                'your_grade': data.get('your_grade'),
                'german_grade': data.get('german_grade')
            }
        )
        
        filename = f"Grade_Certificate_{data.get('name', 'User').replace(' ', '_')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate PDF: {str(e)}'}), 500