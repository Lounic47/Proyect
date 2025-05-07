from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para persistencia
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    min_calories = db.Column(db.Integer, nullable=False)
    max_weight = db.Column(db.Integer, nullable=False)
    items_used = db.Column(db.String(500), nullable=False)
    total_weight = db.Column(db.Integer, nullable=False)
    total_calories = db.Column(db.Integer, nullable=False)

# Clase optimizadora (Principio SOLID de Responsabilidad Única)
class KnapsackOptimizer:
    @staticmethod
    def optimize(items, min_calories, max_weight):
        # Filtramos elementos que pesen más que el máximo permitido
        valid_items = [item for item in items if item.weight <= max_weight]
        
        # Ordenamos por eficiencia calorías/peso (mayor primero)
        valid_items.sort(key=lambda x: x.calories/x.weight, reverse=True)
        
        selected_items = []
        current_weight = 0
        current_calories = 0
        
        for item in valid_items:
            if current_weight + item.weight <= max_weight:
                selected_items.append(item)
                current_weight += item.weight
                current_calories += item.calories
                if current_calories >= min_calories:
                    break
        
        return selected_items if current_calories >= min_calories else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # Validación básica
        if not data or 'items' not in data:
            return jsonify({"error": "Datos incompletos"}), 400
        
        # Crear objetos Item
        items = [
            Item(name=item['name'], weight=int(item['weight']), calories=int(item['calories']))
            for item in data['items']
        ]
        
        # Ejecutar optimización
        optimizer = KnapsackOptimizer()
        result = optimizer.optimize(
            items,
            int(data['minCalories']),
            int(data['maxWeight'])
        )
        
        if not result:
            return jsonify({"error": "No hay solución válida"}), 404
        
        # Guardar en historial
        calculation = Calculation(
            min_calories=int(data['minCalories']),
            max_weight=int(data['maxWeight']),
            items_used=', '.join([item.name for item in result]),
            total_weight=sum(item.weight for item in result),
            total_calories=sum(item.calories for item in result)
        )
        db.session.add(calculation)
        db.session.commit()
        
        return jsonify({
            "items": [item.name for item in result],
            "totalWeight": calculation.total_weight,
            "totalCalories": calculation.total_calories
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Insertar datos de ejemplo (E1, E2, E3, E4, E5)
    with app.app_context():
        if not Item.query.first():
            example_items = [
                Item(name='E1', weight=5, calories=3),
                Item(name='E2', weight=3, calories=5),
                Item(name='E3', weight=5, calories=2),
                Item(name='E4', weight=1, calories=8),
                Item(name='E5', weight=2, calories=3)
            ]
            db.session.bulk_save_objects(example_items)
            db.session.commit()
    
    app.run(debug=True)