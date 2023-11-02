# Meeting Scheduler

Meeting Scheduler is a comprehensive, full-stack web application designed to simplify and streamline scheduling for any team or organization. Built on a modern stack using React and Flask, this application allows users to create, manage, and join meetings, enhancing team collaboration and efficiency.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
    - [Backend](#backend)
    - [Frontend](#frontend)
4. [Usage](#usage)
5. [Running Tests](#running-tests)
6. [Contribution Guidelines](#contribution-guidelines)
7. [License](#license)
8. [Contact](#contact)

## Features

- User Authentication: Secure registration and login functionality.
- Meeting Management: Create, update, view, and delete meetings.
- Comprehensive Scheduling: Add multiple time slots while creating each meeting.
- Meeting Time Suggestion: Participants (users with meeting link) can add and remove new time suggestions
- Voting System: Users can vote on their preferred meeting times.
- Meeting URLs: Generate unique meeting URLs that can be shared with anyone.
- Responsive Design: Works on a variety of devices, from mobile to desktop.

## Prerequisites

To run this application, you will need the following:

- Node.js (v14.0.0 or above)
- Yarn (v1.22.0 or above) or npm (v6.14.0 or above)
- Python (v3.8 or above)
- Flask (v2.0.0 or above)
- A local or remote relational database instance (PostgreSQL, MySQL,etc).

## Installation

### Backend

1. **Clone the Repository**

    ```bash
    git clone https://github.com/afonne-cid/meeting-scheduler.git
    cd meeting-scheduler/backend
    ```

2. **Install Python Dependencies**

    Create a virtual environment and activate it. Then, install the necessary Python dependencies.

    ```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

3. **Set up Environment Variables**

    Copy `.env.example` to a new file named `.env`. To generate unique secret keys for SECRET_KEY and JWT_SECRET_KEY, you can use the following Python command:

    ```bash
    python -c "import secrets; print(secrets.token_hex(32))"
    ```
    Then, fill in your environment variables in the .env file.

4. **Initialize the Flask Application**

    Run the Flask application.

    ```bash
    python main.py
    ```

### Frontend

1. **Navigate to the Frontend Directory**

    ```bash
    cd ../frontend
    ```

2. **Install Node.js Dependencies**

    Make sure to have Node.js and npm installed in your system. Then, install the required dependencies.

    ```bash
    yarn install
    ```

    or

    ```bash
    npm install
    ```

3. **Start the Application**

    Run the application in development mode.

    ```bash
    yarn dev
    ```

    or

    ```bash
    npm run dev
    ```

The application should now be running on `http://localhost:5173`, and it will interact with the backend API running on `http://localhost:5000`.

## Usage

Once the application is running, you can navigate to `http://localhost:5173` in your web browser to access the Meeting Scheduler. If you want to utilize the API directly, you can send HTTP requests to `http://localhost:5000/api`.

## Running Tests

This project uses Python's built-in `unittest` module for backend testing.

- **Backend**

    ```bash
    cd backend
    python -m unittest discover -s tests
    ```

## Contribution Guidelines

Contributions to the Meeting Scheduler project are always welcome. Here's how you can help:

- **Submitting a Pull Request**: If you see something that needs improvement, please feel free to fork the

 repository and submit a pull request. We appreciate your help!
- **Reporting Issues**: If you find a bug or something that doesn't work as expected, please report it in the issue tracker.
- **Documentation**: If you're interested in improving the project's documentation or translating it, we would love your assistance.
- **Reviewing Pull Requests**: Another valuable contribution is reviewing pull requests. Your feedback can help shape the future of the project.

Before contributing, please make sure to read and follow our [Code of Conduct](LINK_TO_CODE_OF_CONDUCT).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, suggestions, or general feedback, please feel free to reach out.

- Twitter: [@cidelight_](https://twitter.com/cee_eye_d)
- LinkedIn: [Cidelight](https://linkedin/in/cidelight)

---