# Expression Data API

Un servicio Flask ligero que expone consultas de expresión génica y metadatos a través de HTTP.  
Los clientes pueden obtener perfiles de expresión por gen, realizar consultas por lotes de varios ID con condiciones seleccionadas y recuperar metadatos de conjuntos de datos.

---

## Project Structure

```bash
📦PhabaseDB-GeneExpressionAPI
 ┣ 📂src
 ┃ ┣ 📂gene
 ┃ ┃ ┣ 📂repository
 ┃ ┃ ┃ ┣ 📜csv_repository.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂routes
 ┃ ┃ ┃ ┣ 📜routes.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂services
 ┃ ┃ ┃ ┣ 📜expression_helpers.py
 ┃ ┃ ┃ ┣ 📜gene_service.py
 ┃ ┃ ┃ ┣ 📜meta_service.py
 ┃ ┃ ┃ ┣ 📜query_service.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📂utils
 ┃ ┃ ┃ ┣ 📜read_file.py
 ┃ ┃ ┃ ┣ 📜resolve_file.py
 ┃ ┃ ┃ ┣ 📜validators.py
 ┃ ┃ ┃ ┗ 📜__init__.py
 ┃ ┃ ┣ 📜constants.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜app.py
 ┃ ┣ 📜config.py
 ┃ ┗ 📜wsgi.py
 ┣ 📜.env-sample
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

Currently, the API is focused on **gene-level expression data** and all related logic lives under the `gene/` module.

At a high level:

Each folder has a clear responsibility:

- **repository**: reads and validates expression datasets
- **services**: contains the core query logic (genes, transcripts, batch queries)
- **utils**: shared helpers and input validation
- **routes**: defines the HTTP endpoints exposed by the API
- **constants**: definition of reusable constants

---

## 📦 Installation & Environment Setup

This project uses Python and Flask. All dependencies are listed in `requirements.txt`.

### Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (Linux / macOS)
source .venv/bin/activate
```

### Install dependencies

```bash
# Clear pip cache (recommended)
pip cache purge

# Install requirements
pip install -r requirements.txt
```

---

## Environment Configuration (.env)

The API relies on external expression datasets that must be configured via environment variables.

You must create a `.env` file and define the directory where expression files are located.

You have two options:

### Option 1: Use an external directory

Provide an absolute path to your expression datasets.

### Option 2: Use the project directory

You may place your datasets inside the project under a folder named `expdb/`.

- The `expdb/` directory is ignored by Git
- Safe for local datasets and large files

---

## API Endpoints

The API currently exposes three endpoints related to gene expression queries.

All routes are defined in:

```bash
src/gene/routes/routes.py
```

Refer to that file for the most up-to-date list of available endpoints and their paths.

---

## Running the Application

### Development (Windows / local)

For local development and debugging, the API can be started using Flask’s built-in server.

Make sure your `.env` file includes the following variables:

```env
FLASK_ENV=development
FLASK_APP=src.wsgi:app
```

Then run:

```bash
flask run --host=0.0.0.0 --port=4002 --reload
```

This enables:

- Hot reloading
- Debug-friendly error messages
- Faster local iteration

### Production Deployment

For production environments, the application should be served using Gunicorn.

Gunicorn provides a more robust and performant WSGI server suitable for deployment behind a reverse proxy (e.g. Nginx).

⚠️ Flask’s built-in server is not recommended for production use.
