# BBC_API_Automation
BBC API GetRequest Automation

API Test Automation - project that uses Cucumber-style testing with Python and Behave

# Prerequisites
- Python installation (https://www.python.org/downloads/)
- Git
- Optional: [Visual Studio Code](https://code.visualstudio.com/)

## Setup Instructions

# Clone the repository

git clone https://github.com/NaliniNandakumar/BBC_API_Automation.git
cd your-repo

# Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
# Or manually:
pip install behave requests

# Running Tests
behave
# Run a specific feature file:
behave features/get_api.feature
