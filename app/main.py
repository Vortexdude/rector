from pathlib import Path
import uvicorn
from app.core.register import register_app
from app.core.config import settings
from app.common.utils.log import timestamp_log_config

app = register_app()

if __name__ == "__main__":
    try:
        config = uvicorn.Config(
            app=f"{Path(__file__).stem}:app",
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=True,
            reload_dirs=[str(Path(__file__).parent)],
            log_config=timestamp_log_config(uvicorn.config.LOGGING_CONFIG)
        )
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
