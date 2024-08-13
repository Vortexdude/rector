from mangum import Mangum
from app.core.register import register_app

app = register_app()

handler = Mangum(app)
