from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import (
    get_password_validators,
    validate_password,
)
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from base.custom_user.models import User

"""
Base User setup which serializes a User to login
via their email and aligns their username (required by Django)
to its given email.

You can use this as-is as it is set in the Django settings
as the default User model/flow. Or you can overwrite it
based on this implementation to ad additional fields
to a User model (and subsequently to these serializers).

Don't forget to update your User model in your settings
if you do decide to use your own model.
"""


class IsOwnUser(permissions.BasePermission):
    """
    Only allow the actual user to view or update their user data.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj == request.user


class UserSerializer(serializers.ModelSerializer):
    """
    Base User data serializer and validator.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(min_length=8, max_length=32)

    def create(self, validated_data) -> User:
        try:
            validate_password(
                validated_data["password"],
                password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS),
            )
        except ValidationError as e:
            # raise a validation error for the serializer
            raise exceptions.ValidationError({"password": e.messages}) from e

        user = User.objects.create_user(
            validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        group, created = Group.objects.get_or_create(id=4)

        user.groups.add(group)

        self.update(user, validated_data)

        return user 

    def update(self, instance, validated_data) -> User:
        if "email" in validated_data:
            instance.email = validated_data["email"]

        instance.save()

        return instance

    class Meta:
        model = User
        fields = (
            "id",
            "email",
        )


class UserViewSerializer(serializers.ModelSerializer):
    """
    Separate serializer for displaying a user where
    we remove the password from the returned list of fields.
    """

    class Meta:
        model = User
        fields = ("id", "email")


@extend_schema(tags=["Users"])
class UserAPIView(
    generics.CreateAPIView,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = [IsOwnUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self) -> User:
        if self.kwargs.get("pk", None) == "me":
            self.kwargs["pk"] = self.request.user.pk
        return super(generics.RetrieveUpdateDestroyAPIView, self).get_object()

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Overwritten the retrieve method to set a different
        (passwordless) serializer for getting a user.
        """
        instance = self.get_object()
        serializer = UserViewSerializer(instance)
        return Response(serializer.data)


class UserPasswordUpdateSerializer(serializers.Serializer):
    """
    Separate serializer to change a user's password.
    """

    model = User

    old_password = serializers.CharField(min_length=8)
    password = serializers.CharField(min_length=8)


@extend_schema(tags=["Users"])
class UserPasswordUpdateView(generics.UpdateAPIView):
    serializer_class = UserPasswordUpdateSerializer
    model = User
    queryset = User.objects.all()
    permission_classes = (IsOwnUser,)

    def __init__(self, **kwargs) -> None:
        super().__init__(kwargs)
        self.object = None

    def get_object(self):
        if self.kwargs.get("pk", None) == "me":
            self.kwargs["pk"] = self.request.user.pk
        return super(generics.UpdateAPIView, self).get_object()

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
