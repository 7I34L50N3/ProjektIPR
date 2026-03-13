# Language Learning Web Application

This repository contains a web-based application designed to facilitate foreign language learning. The graphical user interface (GUI) is heavily inspired by GitHub's design system, providing a clean and familiar user experience.

<img width="960" height="462" alt="image" src="[https://github.com/user-attachments/assets/49ad3519-be2e-492f-978c-769c4403a96a](https://github.com/user-attachments/assets/49ad3519-be2e-492f-978c-769c4403a96a)" />

---

## Current Project Status

The following core features are currently implemented in the latest version:

* **Authentication:** A fully functional login panel.
* **System Architecture:** A base user class that serves as the architectural foundation for all other roles and actors within the system.

---

## Setup and Installation

The application can be deployed in two ways: locally via a Python environment, or containerized using Docker. Choose the method that best suits your development workflow.

### Option 1: Local Deployment

To run the application directly in a standard development environment (such as PyCharm or a local terminal):

1. Navigate to the root directory of the project.
2. Execute the main application script using the following command:

```bash
python app.py

```

### Option 2: Docker Deployment

Running the application via Docker ensures a consistent environment but requires appropriate system preparation.

**Prerequisites (Windows Users):**

* Windows Subsystem for Linux (WSL 2) must be installed and configured.
* A Docker environment must be installed (e.g., Docker Desktop).

**Execution Steps:**

1. Open your command line interface or the integrated terminal in your IDE.
2. Build the image and start the container using Docker Compose:

```bash
docker-compose up --build

```

---

## Accessing the Application

Upon successful initialization using either of the methods above, the application will be accessible via your web browser at the following local address:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
