# Adaptive Applications: Group Demeter backend
This is the backend repository for Group Demeter in the Adaptive Applications module at Trinty College Dublin.

The application implements API endpoints which interact with an SQLite database to facilitate a personalised experience for users.
No user authentication information is stored on any of the database dealt with here --- that is left to the Google Firebase Authentication service, which the frontend application interacts with directly.

**The application, as it stands, has two directories:**
- `api`: This contains the `main.py` file and individual files (e.g. `age.py`) corresponding to different API endpoints. The `main.py` file gathers all of the endpoints (represented as Python classes) from the other files in this folder, and uses them to create an API.
- `db`: for storing the SQLite3 database (currently just `example.db`) as well as auxiliary documents.

Before executing everything, ensure that the necessary dependencies are installed. These are listed in the `requirements.txt` file. To install them all, navigate to the root directory and execute `pip install -r requirements.txt` (first creating a virtual environment, e.g. through `python3 -m venv ./venv/` if you would prefer not to install these packages globally).

To run the server, navigate to the root project directory and execute `python3 api/main.py`.
