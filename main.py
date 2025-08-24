import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db

# Carregar variáveis de ambiente
load_dotenv()

# Importar todos os modelos para garantir que sejam criados
from src.models.user import User
from src.models.product import Product
from src.models.cart import Cart, CartItem
from src.models.ticket import Ticket, TicketItem
from src.models.password_reset import PasswordResetToken

# Importar blueprints
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.product import product_bp
from src.routes.cart import cart_bp
from src.routes.password_reset import password_reset_bp
from src.routes.ticket import ticket_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))  # 16MB

# Configurar CORS para permitir requisições do frontend
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"])

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(cart_bp, url_prefix='/api')
app.register_blueprint(password_reset_bp, url_prefix='/api/auth')
app.register_blueprint(ticket_bp, url_prefix='/api')

# Inicializar banco de dados
db.init_app(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Rota de health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'ok', 'message': 'Servidor funcionando corretamente'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

