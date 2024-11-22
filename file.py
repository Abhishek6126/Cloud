import os

# Define the directory structure
project_structure = {
    "project-folder": {
        "main.py": None,
        "simulation": {
            "__init__.py": None,
            "simulation_manager.py": None,
            "uav_simulation.py": None,
            "iot_simulation.py": None,
            "energy_model.py": None,
            "communication_model.py": None,
            "task_offloading.py": None,
            "path_planning.py": None,
        },
        "results": {
            "logs": {},
            "plots": {},
            "data": {},
        },
        "tests": {
            "test_energy_model.py": None,
            "test_task_offloading.py": None,
            "test_path_planning.py": None,
        },
        "docs": {
            "README.md": None,
            "setup_instructions.md": None,
            "algorithm_details.pdf": None,
        },
        "requirements.txt": None,
        "config.json": None,
        "utils": {
            "__init__.py": None,
            "helpers.py": None,
            "constants.py": None,
        },
    }
}

# Function to create the structure
def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)  # Create directory
            create_project_structure(path, content)  # Recursively create subfolders/files
        else:
            with open(path, "w") as file:  # Create an empty file
                if name.endswith(".json"):  # Example content for JSON
                    file.write("{}")  # Write empty JSON
                elif name.endswith(".md"):  # Example content for Markdown
                    file.write(f"# {name.replace('.md', '').capitalize()}\n")
                elif name.endswith(".py"):  # Example content for Python files
                    file.write(f"# {name}\n\n")
                elif name.endswith(".txt"):  # Example content for text files
                    file.write("# Python dependencies\n")
                else:
                    pass  # Leave other files empty

# Specify base directory
base_dir = "."

# Generate the project structure
create_project_structure(base_dir, project_structure)

print("Project structure created successfully!")

