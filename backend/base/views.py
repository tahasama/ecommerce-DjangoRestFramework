from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.aggregates import Avg
from django.db.models.fields import IntegerField
from django.db.models import Q
from .models import Product, Order, OrderItem, Review, ShippingAddress
from .serializers import MyTokenObtainPairSerializer, OrderSerializer, ProductSerializer, UserSerializer, UserSerializerWithToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView


from datetime import datetime


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serialize = UserSerializer(users, many=True)
        return Response(serialize.data)


class deleteUser(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk=None):
        userForDeletion = User.objects.get(id=pk)
        userForDeletion.delete()
        return Response('User was deleted')


class GetUserById(APIView):
    def get(self, request, pk=None):
        user = User.objects.get(id=pk)
        serialize = UserSerializer(user)
        return Response(serialize.data)


class UpdateUser(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        user = User.objects.get(id=pk)

        data = request.data

        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        user.is_staff = data['isAdmin']

        user.save()
        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)


class registerUser(APIView):
    serializer_class = UserSerializerWithToken
    model_class = User

    def post(self, request):
        data = self.request.data
        users = User.objects.all()
        emails = [user.email for user in users]
        names = [user.first_name for user in users]

        if data['email'] in emails:
            message = {'detail': 'email already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        elif len(data['password']) < 4:
            message = {'detail': 'password too short'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        elif len(data['password']) > 6:
            message = {'detail': 'password too long'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        elif data['name'] in names:
            message = {'detail': 'name already used'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        user = self.model_class.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = self.serializer_class(user)
        return Response(serializer.data)


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,):
        user = request.user
        serialize = UserSerializer(user)
        return Response(serialize.data)


class UpdateUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']

        if len(data['password']) < 4:
            message = {'detail': 'password too short'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        elif data['password'] != '':
            user.password = make_password(data['password'])

        user.save()

        serializer = UserSerializerWithToken(user)
        return Response(serializer.data)


class ProductList(APIView):
    def get(self, request):
        query = request.query_params.get('keyword')
        print('query:', query)
        if query == None:
            query = ''

        products = Product.objects.filter(Q(name__icontains=query) | Q(
            brand__icontains=query) | Q(category__icontains=query))
        print(products)

        page = request.query_params.get('page')
        paginator = Paginator(products, 2)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        print('Page:', page)
        serializer = ProductSerializer(products, many=True)
        return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


class ProductRetrieve(APIView):
    def get(self, request, pk=None):
        product = Product.objects.get(_id=pk)
        serialize = ProductSerializer(product)
        return Response(serialize.data)


class AddOrderItems(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        orderItems = data['orderItems']

        if orderItems and len(orderItems) == 0:
            return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

        # (1) Create order

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        # (2) Create shipping address

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        # (3) Create order items adn set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=product.price,
                image=product.image.url,
            )
            product.countInStock -= item.qty
            product.save()
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


class getOrderById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):

        user = request.user

        try:
            order = Order.objects.get(_id=pk)
            if user.is_staff or order.user == user:
                serializer = OrderSerializer(order, many=False)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Not authorized to view this order'},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class getMyOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class updateOrderToPaid(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        order = Order.objects.get(_id=pk)

        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()

        return Response('Order was paid')


class getOrders(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class createProduct(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = request.user

        product = Product.objects.create(
            user=user,
            name='Sample Name',
            price=0,
            brand='Sample Brand',
            countInStock=0,
            category='Sample Category',
            description=''
        )

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class updateProduct(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        data = request.data
        product = Product.objects.get(_id=pk)

        product.name = data['name']
        product.price = data['price']
        product.brand = data['brand']
        product.countInStock = data['countInStock']
        product.category = data['category']
        product.description = data['description']

        product.save()

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class deleteProduct(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        product = Product.objects.get(_id=pk)
        product.delete()
        return Response('Producted Deleted')


class uploadImage(APIView):

    def post(self, request):
        data = request.data

        product_id = data['product_id']
        product = Product.objects.get(_id=product_id)

        product.image = request.FILES.get('image')

        product.save()

        return Response('Image was uploaded')


class updateOrderToDelivered(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        order = Order.objects.get(_id=pk)

        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.save()

        return Response('Order was delivered')


class createProductReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        product = Product.objects.get(_id=pk)
        data = request.data
        print('new data yo:', data)

        # 1 - Review already exists
        alreadyExists = product.review_set.filter(user=user).exists()
        if alreadyExists:
            content = {'detail': 'Product already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 2 - No Rating or 0
        elif data['rating'] == 0:
            content = {'detail': 'Please select a rating'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # 3 - Create review
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                name=user.first_name,
                rating=data['rating'],
                comment=data['comment'],
            )

            product.rating = product.review_set.aggregate(
                Avg('rating', output_field=IntegerField()))['rating__avg']

            reviews = product.review_set.all()
            product.numReviews = len(reviews)

            product.save()

            return Response('Review Added')


class getTopProducts(APIView):

    def get(self, request):
        products = Product.objects.filter(
            rating__gte=4).order_by('-rating')[:2]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
