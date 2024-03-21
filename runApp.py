from app import api
import os

application = api.create_app()
port = int(os.environ.get("PORT", 8080))
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=port, debug=True)
