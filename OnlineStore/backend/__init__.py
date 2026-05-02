import os

from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager


from dotenv import load_dotenv

from OnlineStore.backend.services import ProductService, CartService, OrderService
from bot_vk_ng import send_notification

load_dotenv()

PRODUCT_SERVICE = ProductService()
CART_SERVICE = CartService(PRODUCT_SERVICE)
ORDER_SERVICE = OrderService(CART_SERVICE)

app = Flask(
    __name__,
    static_folder='dist',
    template_folder='dist'
)
app.config["JWT_SECRET_KEY"] = os.getenv('vk_token')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400
jwt = JWTManager(app)

ADMIN_ID = os.getenv('vk_admin_id')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    full_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user id"}), 400
    try:
        user_id = str(data['user_id'])
        admin_id = os.getenv('vk_admin_id')

        is_admin = True if user_id == admin_id else False

        access_token = create_access_token(identity=user_id)
        return jsonify({
            "accessToken": access_token,
            "isAdmin" : False
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/init')
@jwt_required()
def get_admin_init_data():
    user_id = get_jwt_identity()

    if str(user_id) == ADMIN_ID:
        statuses = ORDER_SERVICE.retrieve_order_statuses()
        return jsonify(statuses=statuses), 200
    else:
        return (), 403


@app.route('/api/init')
@jwt_required()
def get_init_data():
    user_id = get_jwt_identity()
    items_count = CART_SERVICE.get_total_items_count(user_id)
    return jsonify(items_count=items_count), 200

@app.route('/api/categories')
def get_categories():
    categories = PRODUCT_SERVICE.retrieve_categories()
    return jsonify(categories), 200

@app.route('/api/category')
def get_category():
    category_id = request.args.get('category_id')
    category = PRODUCT_SERVICE.retrieve_category(category_id)
    return jsonify(category)

@app.route('/api/group')
def get_group():
    group_id = request.args.get('group_id')
    category_id = request.args.get('category_id')
    group = PRODUCT_SERVICE.retrieve_group(group_id, category_id)
    return jsonify(group)


@app.route('/api/product')
@jwt_required()
def get_product_data():
    user_id = get_jwt_identity()
    product_id = request.args.get('product_id')
    product = PRODUCT_SERVICE.retrieve_product(product_id)
    cart_count = CART_SERVICE.get_item_quantity(product_id, user_id)
    fav_status = PRODUCT_SERVICE.get_fav_status(product_id, user_id)
    return jsonify(product=product, fav_status=fav_status, count = cart_count)

@app.route('/api/cart')
@jwt_required()
def get_cart_data():
    user_id = get_jwt_identity()
    cart=CART_SERVICE.retrieve_active_cart(user_id)
    return jsonify(
        items=cart['items'],
        items_count=cart['items_count'],
        full_price=cart['full_price'],
        total_discount=cart['total_discount'],
        total=cart['total']
    ), 200

@app.route('/api/cart/item/add', methods=['POST'])
@jwt_required()
def add_product_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    CART_SERVICE.add_to_cart(product_id, user_id)
    return jsonify(count=1), 200

@app.route('/api/cart/item/delete', methods=['POST'])
@jwt_required()
def delete_product_from_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    CART_SERVICE.delete_from_cart(product_id, user_id)
    return jsonify(0), 200

@app.route('/api/cart/item/increment', methods=['POST'])
@jwt_required()
def increment_cart_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = CART_SERVICE.increment_cart_item_quantity(product_id, user_id)
    return jsonify(quantity), 200

@app.route('/api/cart/item/decrement', methods=['POST'])
@jwt_required()
def decrement_cart_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = CART_SERVICE.decrement_cart_item_quantity(product_id, user_id)
    return jsonify(quantity), 200

@app.route('/api/cart/clear')
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()
    CART_SERVICE.clear_cart(user_id)
    return jsonify(), 200

@app.route('/api/cart/refresh_summary')
@jwt_required()
def refresh_summary():
    user_id = get_jwt_identity()
    cart = CART_SERVICE.refresh_summary(user_id)
    return jsonify(cart), 200

@app.route('/api/product/add_to_fav', methods=['POST'])
@jwt_required()
def add_product_to_favorites():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    status = PRODUCT_SERVICE.add_product_to_favorites(product_id, user_id)
    return jsonify(status), 200

@app.route('/api/product/delete_from_fav', methods=['POST'])
@jwt_required()
def delete_product_from_favorites():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    status = PRODUCT_SERVICE.delete_product_from_favorites(product_id, user_id)
    return jsonify(status), 200

@app.route('/api/favorites')
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    products = PRODUCT_SERVICE.retrieve_favorites(user_id)
    return jsonify(products), 200

@app.route('/api/checkout/options')
@jwt_required()
def get_checkout_options():
    payment_methods = ORDER_SERVICE.retrieve_payment_methods()
    drop_points = ORDER_SERVICE.retrieve_available_drop_points()
    return jsonify(paymentMethods=payment_methods, dropPoints=drop_points), 200

@app.route('/api/checkout', methods=['POST'])
@jwt_required()
def checkout():

    user_id = get_jwt_identity()
    data = request.get_json()
    cart = CART_SERVICE.get_active_cart(user_id)
    dp = data.get('DP')
    pm = data.get('PM')
    order_id = ORDER_SERVICE.create_order(user_id, cart, dp, pm)

    send_notification(f'У вас новый заказ, номер заказа №{order_id}!', ADMIN_ID, f"https://wokd3r-94-141-53-179.ru.tuna.am/orders/order/{order_id}")
    f'Заказ №{order_id}, был отменен пользователем!'


    return jsonify(order_id=order_id), 200

@app.route('/api/order')
@jwt_required()
def get_order():
    user_id = get_jwt_identity()
    order_id = request.args.get('order_id')
    statuses = ORDER_SERVICE.retrieve_order_statuses()
    order = ORDER_SERVICE.retrieve_order(user_id, order_id)
    return jsonify(statuses=statuses, orderData=order), 200


@app.route('/api/orders')
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = ORDER_SERVICE.retrieve_orders(user_id)
    return jsonify(orders), 200

@app.route('/api/order/cancel')
@jwt_required()
def cancel_order():
    user_id = get_jwt_identity()
    order_id = request.args.get('order_id')
    is_canceled = ORDER_SERVICE.cancel_order(user_id, order_id)
    if is_canceled is not None:
        send_notification(f'Заказ №{order_id}, был отменен пользователем!', ADMIN_ID)
        return jsonify(is_canceled=is_canceled), 200
    else:
        return jsonify(), 404

@app.route('/api/orders/admin')
@jwt_required()
def get_orders_admin():
    user_id = get_jwt_identity()
    status_id = request.args.get('status_id', type=int)
    is_canceled = request.args.get('is_canceled') == 'true'
    is_completed = request.args.get('is_completed') == 'true'
    if str(user_id) == ADMIN_ID:
        if status_id is not None:
            orders = ORDER_SERVICE.retrieve_orders_by_status(status_id)
        elif is_canceled:
            orders = ORDER_SERVICE.retrieve_canceled_orders()
        elif is_completed:
            orders = ORDER_SERVICE.retrieve_completed_orders()
        return jsonify(orders), 200
    else:
        return jsonify(), 403

@app.route('/api/orders/admin/update', methods=['POST'])
@jwt_required()
def update_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get('order_id')
    status_id = data.get('status_id')
    is_completed = data.get('is_completed')
    if str(user_id) == ADMIN_ID:
        res, user_id = ORDER_SERVICE.update_order(order_id, status_id, is_completed)
        if res:
            send_notification(f'Статус вашего заказа №{order_id} был обновлен!', user_id, f"https://wokd3r-94-141-53-179.ru.tuna.am/orders/order/{order_id}")
            return jsonify({"success": True}) ,  200
        else:
            return jsonify({"success": False}) ,  400
    else:
        return jsonify(), 403

if __name__ == '__main__':
    app.run(debug=True, port=5000)
