# ecommerce-DjangoRestFramework

An E-commerce API with Django Rest Framework.

Users can register, login, create orders, modify them...and an admin panel for the admin with permissions etc

The login system is built with Json Web Token.

Nginx was used as reverse proxy for Gunicorn

Docker was used in this application as a demostration, Docker files and docker-compose,

the database used is Postgres, 

deploymen with Gunicorn to Heroku

future add :

  Any technology can be implemented for payments (Braintree, Paypal, Stripe...) directly in the order view, I recommend using it with Atomic Transactions 

  It is possible to add a e-mail service to alert customers or send bills, the usage of Celery for queueing with Redis or RabbitMq

  Also possible to use caching system with Redis
