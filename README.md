# E-commerce Django Rest Framework

An E-commerce API built with Django Rest Framework.

## Features

- User authentication (registration, login)
- Order creation and modification
- Admin panel with permissions
- Json Web Token for the login system
- Nginx as a reverse proxy for Gunicorn
- Docker for demonstration purposes (Docker files and docker-compose included)
- PostgreSQL as the database
- Deployment with Gunicorn to Heroku

## Future Additions

- Implementation of various payment technologies (Braintree, Paypal, Stripe...) directly in the order view. Consider using Atomic Transactions.
- Integration of an email service to alert customers or send bills. Utilize Celery for queuing with Redis or RabbitMQ.
- Possibility to implement a caching system with Redis.

Feel free to customize and expand upon this template to better suit your project. Add code snippets, installation instructions, or any other relevant information to help users understand and use your E-commerce Django Rest Framework application.
