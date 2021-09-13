from app import app

if __name__ == "__main__":
    app.run()

#  uwsgi --http :5000 --home /home/sonhos/Basement/VisionDemo/.venv --chdir /home/sonhos/Basement/VisionDemo/ -w main:app
#  uwsgi --http :5000 --home /home/ubuntu/venv --chdir /home/ubuntu/HMM -w main:app
