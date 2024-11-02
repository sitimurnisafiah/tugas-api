from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data contoh sepatu
shoes = [
    {"id": "1", "name": "Nike Air Max", "description": "High performance running shoes", "price": 1500000, "size": 42},
    {"id": "2", "name": "Adidas Ultraboost", "description": "Comfortable everyday sneakers", "price": 1800000, "size": 41},
    {"id": "3", "name": "Puma RS-X", "description": "Trendy casual sneakers", "price": 1200000, "size": 43}
]

# Detail ulasan pelanggan untuk setiap sepatu
details = {
    "1": {"customerReviews": []},
    "2": {"customerReviews": []},
    "3": {"customerReviews": []}
}

# Class untuk daftar sepatu
class ShoeList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(shoes),
            "shoes": shoes
        }

# Class untuk detail sepatu berdasarkan ID
class ShoeDetail(Resource):
    def get(self, shoe_id):
        shoe = next((shoe for shoe in shoes if shoe['id'] == shoe_id), None)
        if shoe:
            return {
                "error": False,
                "message": "success",
                "shoe": shoe
            }
        return {"error": True, "message": "Shoe not found"}, 404

# Class untuk mencari sepatu berdasarkan nama atau deskripsi
class ShoeSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [shoe for shoe in shoes if query in shoe['name'].lower() or query in shoe['description'].lower()]
        return {
            "error": False,
            "founded": len(result),
            "shoes": result
        }

# Class untuk menambah ulasan pelanggan
class AddReview(Resource):
    def post(self):
        data = request.get_json()
        shoe_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if shoe_id in details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            details[shoe_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "customerReviews": details[shoe_id]['customerReviews']
            }
        return {"error": True, "message": "Shoe not found"}, 404

# Class untuk memperbarui ulasan
class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        shoe_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if shoe_id in details:
            reviews = details[shoe_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Shoe not found"}, 404

# Class untuk menghapus ulasan
class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        shoe_id = data.get('id')
        name = data.get('name')
        
        if shoe_id in details:
            reviews = details[shoe_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Shoe not found"}, 404

# Menambahkan resource ke API
api.add_resource(ShoeList, '/shoes')
api.add_resource(ShoeDetail, '/shoe/<string:shoe_id>')
api.add_resource(ShoeSearch, '/shoes/search')
api.add_resource(AddReview, '/review')
api.add_resource(UpdateReview, '/review/update')
api.add_resource(DeleteReview, '/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
