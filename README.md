# intern-city

## Setup guide
- make sure you have `python` and `pip` installed

### Clone the repository

```
git clone https://github.com/ysh1th/intern-city.git
cd <repository-directory>
```

### Create & source python virtual environment

```
python -m venv .venv
source .venv/bin/activate  # for mac os
.env\Scripts\activate  # for windows
```

### install dependencies
```
pip install -r requirements.txt
```

### Set up google maps API key
1. Sign up for the Google Cloud Platform and create a new project.
2. Enable the Google Maps JavaScript API and Places API.
3. Generate an API key.
4. Create a `.env` file in the project directory and add you API key:
```
GOOGLE_MAPS_API=<your_api_key>
```

### Run the application
```
streamlit run app.py
```

## Contributing
To contribute to the repository:
1. Fork the repository
2. Create a new branch using the following command:
  ```
  git checkout -b your-branch-name
  ```
3. Make your changes and commit using the following commands:
  ```
  git add .
  git commit -m "commit-message"
  git push origin your-branch-name
  ```
4. Open a pull request