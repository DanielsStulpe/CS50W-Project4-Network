# CS50 Web - Project 4 - Network

## Project Overview
Network is a Threads-like social networking website where users can create posts, follow other users, like posts, and interact with each other. The platform includes features such as pagination, profile pages, post editing, and a following feed.

## Getting Started

### Prerequisites
Ensure you have Python and Django installed on your system.

### Installation
1. Clone the repository:
   ```sh
   git clone <repository_url>
   ```

2. **Navigate to the Project Directory**  
   Open a terminal and move into the project directory:
   ```sh
   cd project4
   ```

3. **Apply Migrations**  
   Run the following commands to set up the database:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the Server**  
   Start the Django development server:
   ```sh
   python manage.py runserver
   ```
   The application will be available at `http://127.0.0.1:8000/`.

## Features

### 1. User Authentication
- Users can register, log in, and log out.
- Authentication is handled using Django’s built-in authentication system.

### 2. Posting
- Signed-in users can create new text-based posts.
- Posts appear on the "All Posts" page in reverse chronological order.

### 3. Profile Pages
- Each user has a profile page displaying:
  - Their posts.
  - Number of followers and followings.
  - A "Follow" or "Unfollow" button for signed-in users viewing other profiles.

### 4. Following Feed
- Signed-in users can view posts made by users they follow.
- Functions like the "All Posts" page but displays only followed users' posts.

### 5. Pagination
- Posts are paginated, displaying 10 per page.
- "Next" and "Previous" buttons allow navigation between pages.

### 6. Post Editing
- Users can edit their own posts.
- Editing is done in-line using JavaScript and does not require a page reload.
- Only the original author of a post can edit it.

### 7. Like and Unlike Posts
- Users can like and unlike posts.
- The like count updates asynchronously using JavaScript and fetch API.
- Users cannot like their own posts.

## File Structure
```
project4/
│-- network/
│   │-- migrations/          # Database migrations
│   │-- static/network/      # CSS, JavaScript
│   │-- templates/network/   # HTML templates
│   │-- __init__.py
│   │-- admin.py             # Django admin setup
│   │-- apps.py
│   │-- models.py            # Database models
│   │-- tests.py
│   │-- urls.py              # URL routing
│   │-- views.py             # View logic
|-- project4/ ...
│-- manage.py                # Django management script
```

## Technologies Used
- **Django** (Backend, Database ORM, Authentication)
- **SQLite** (Database)
- **HTML/CSS** (Frontend Styling)
- **JavaScript (Fetch API)** (Asynchronous interactions, dynamic updates)

## How to Contribute
If you’d like to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push your changes (`git push origin feature-name`).
5. Open a pull request.

## License
This project is for educational purposes and follows CS50's academic guidelines.

## Acknowledgments
- CS50 Web Programming with Python and JavaScript
- Django Documentation

Happy coding! 🚀

