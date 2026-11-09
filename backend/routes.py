from flask import Blueprint, request, jsonify
from models import db, Expense
from datetime import datetime

expense_bp = Blueprint('expense_bp', __name__)

# --- Validation Helper ---
def validate_expense_input(data, is_update=False):
    errors = []

    # Required fields for creation
    if not is_update:
        for field in ['amount', 'category', 'date']:
            if field not in data or data[field] is None or str(data[field]).strip() == "":
                errors.append(f"Field '{field}' is required.")

    # Amount validation (Must be positive float)
    if 'amount' in data and data['amount'] is not None:
        try:
            val = float(data['amount'])
            if val <= 0:
                errors.append("Amount must be a positive number greater than 0.")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number.")

    # Date validation (Format YYYY-MM-DD)
    if 'date' in data and data['date'] is not None:
        try:
            datetime.strptime(data['date'], "%Y-%m-%d")
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format.")

    return errors


# -------------------------------------------------------------------
# 1. POST /api/expenses (Add Expense)
# -------------------------------------------------------------------
@expense_bp.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON payload required"}), 400

    errors = validate_expense_input(data, is_update=False)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        # Convert date string to Python date object
        parsed_date = datetime.strptime(data['date'], "%Y-%m-%d").date()

        new_expense = Expense(
            amount=float(data['amount']),
            category=data['category'].strip(),
            date=parsed_date,
            description=data.get('description', '').strip()
        )

        db.session.add(new_expense)
        db.session.commit()

        return jsonify({
            "message": "Expense created successfully!",
            "expense": new_expense.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


# -------------------------------------------------------------------
# 2. PUT /api/expenses/<id> (Update Expense)
# -------------------------------------------------------------------
@expense_bp.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": f"Expense with ID {expense_id} not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON payload required"}), 400

    errors = validate_expense_input(data, is_update=True)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        if 'amount' in data:
            expense.amount = float(data['amount'])
        if 'category' in data:
            expense.category = data['category'].strip()
        if 'date' in data:
            expense.date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        if 'description' in data:
            expense.description = data['description'].strip()

        db.session.commit()

        return jsonify({
            "message": "Expense updated successfully!",
            "expense": expense.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database update failed", "details": str(e)}), 500


# -------------------------------------------------------------------
# 3. DELETE /api/expenses/<id> (Delete Expense)
# -------------------------------------------------------------------
@expense_bp.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"error": f"Expense with ID {expense_id} not found."}), 404

    try:
        db.session.delete(expense)
        db.session.commit()

        return jsonify({"message": f"Expense ID {expense_id} deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database deletion failed", "details": str(e)}), 500