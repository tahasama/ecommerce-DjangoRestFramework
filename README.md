# ecommerce-DjangoRestFramework

An E-commerce API with Django Rest Framework.

The login system is built with Json Web Token.

Any technology can be implemented for payments (Braintree, Paypal, Stripe...) directly in the order view, I recommend using it with Atomic Transactions , 

Nginx was used as reverse proxy,

Docker was used in this application as a demostration, Docker files and docker-compose,

the database used is Postgres, 

deploymen with Gunicorn to Heroku

future add :

  It is possible to add a e-mail service to alert customers or send bills, the usage of Celery for queueing with Redis or RabbitMq

  Also possible to use caching system with Redis
