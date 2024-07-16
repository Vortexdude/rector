from pathlib import Path
import uvicorn
from app.core.register import register_app

app = register_app()

if __name__ == "__main__":
    try:
        config = uvicorn.Config(app=f"{Path(__file__).stem}:app", reload=True)
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
