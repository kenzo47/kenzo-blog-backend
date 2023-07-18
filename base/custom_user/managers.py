from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        full_name,
        profile_picture,
        password=None,
        is_admin=False,
        is_staff=False,
        is_active=True,
    ) -> object:
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not full_name:
            raise ValueError("User must have a full name")

        user = self.model(email=self.normalize_email(email))
        user.full_name = full_name
        user.set_password(password)  # change password to hash
        user.profile_picture = profile_picture
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields) -> object:
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
