from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Countries(models.Model):
    """List of all possible countries"""

    flag = models.CharField(max_length=300, null=True, blank=True)
    dial = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class StateProvidence(models.Model):
    """
        List of state or providence
    """
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """ create and save new user """
        if not email:
            raise ValueError('The email field must be provided')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """create a new super user"""
        if not email:
            raise ValueError('The email field must be provided')
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    address         = models.CharField(max_length=254)
    city            = models.CharField(max_length=25)
    country         = models.CharField(max_length=254, blank=True, null=True)
    state           = models.CharField(max_length=254, blank=True, null=True)
    phone           = models.CharField(max_length=11)
    email           = models.EmailField(max_length=255, unique=True)
    image           = models.ImageField(upload_to='users/user_image/', default=None, blank=True, null=True)
    updated         = models.DateTimeField(auto_now=True)
    created         = models.DateTimeField(auto_now_add=True)
    gender          = models.TextField(choices=GENDER_CHOICES, blank=True, null=True)
    dob             = models.CharField(max_length=25, blank=True, null=True)
    surname         = models.CharField(max_length=254, default=None, null=True)
    last_name         = models.CharField(max_length=254, default=None, null=True)
    first_name      = models.CharField(max_length=255, default=None, null=True)
    about           = models.CharField(max_length=255, default=None, null=True)
    username        = models.CharField(max_length=255, blank=True, null=True)
    # total_questions = models.IntegerField(default=0)
    # total_upvotes   = models.IntegerField(default=0)
    # total_downvotes = models.IntegerField(default=0)
    # total_answers   = models.IntegerField(default=0)
    ts_rank         = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class LoginLogoutFail(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    device              = models.CharField(max_length=254, default="Non-Mobile")
    login               = models.BooleanField(default=False)
    login_time          = models.DateTimeField(default=None, null=True)
    logout              = models.BooleanField(default=False)
    logout_time         = models.DateTimeField(default=None, null=True)
    failed_login        = models.BooleanField(default=False)
    failed_login_time   = models.DateTimeField(default=None, null=True)
    message             = models.TextField(default=None, null=True)
    spare0              = models.CharField(max_length=100, default=None, null=True)
    spare1              = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "LoginLogoutFailures"
        verbose_name_plural = "LoginLogoutFailures"


class ContactUs(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type     = models.CharField(max_length=100, default="Android")
    created_at      = models.DateTimeField(auto_now_add=True)
    subject         = models.CharField(max_length=150)
    message         = models.TextField()
    spare           = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class DeviceId(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id       = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    device_type     = models.CharField(max_length=100, default="Android")
    active          = models.BooleanField(default=True)
    deactivate_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "Device ID"
        verbose_name_plural = "Device IDs"


class ResetRequests(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    token           = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    consumed_at     = models.DateTimeField(auto_now=True)
    consumed        = models.BooleanField(default=False)
    use_case        = models.CharField(max_length=100)

    @property
    def get_consumption(self):
        if self.created_at == self.consumed_at:
            return False
        return True

    def save(self, *args, **kwargs):
        self.consumed = self.get_consumption
        super(ResetRequests, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Reset Request"
        verbose_name_plural = "Reset Requests"


class OtherRequests(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    request_type    = models.CharField(max_length=100)
    details         = models.CharField(max_length=254, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "Other Request"
        verbose_name_plural = "Other Requests"


class ExperienceModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "User Experience"
        verbose_name_plural = "User Experiences"


class SkillsModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "User Skill"
        verbose_name_plural = "User Skills"


class AwardsModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image_url = models.CharField(max_length=350, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "User Award"
        verbose_name_plural = "User Awards"


class CertificationModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image_url = models.CharField(max_length=350, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "User Award"
        verbose_name_plural = "User Awards"


class ProjectsModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, default=None, null=True)
    image_url = models.CharField(max_length=350, default=None, null=True)
    project_start_date = models.DateField(null=True)
    project_launch_date = models.DateField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "User Experience"
        verbose_name_plural = "User Experiences"


class EducationModels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=250)
    qualification = models.CharField(max_length=350, default=None, null=True)
    image_url = models.CharField(max_length=350, default=None, null=True)
    name_of_school = models.CharField(max_length=350, default=None, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "User Educational background"
        verbose_name_plural = "User Educational backgrounds"
