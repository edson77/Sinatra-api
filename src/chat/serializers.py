from pkg_resources import require
from rest_framework import  serializers
from chat.models import User, Message
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    name = serializers.CharField(min_length=3)
    password = serializers.CharField(min_length=6)
    class Meta:
        model = User
        fields = ('id','email','password','name', 'phone','image_url','date_joined','last_login')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    def get_photo_url(self, obj):
        request = self.context.get('request')
        url_image = obj.fingerprint.url
        return request.build_absolute_uri(url_image)
    
class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image_url']

    def save(self, *args, **kwargs):
        # if self.instance.image_url:
        #     self.instance.image_url.delete()
        return super().save(*args, **kwargs)
    
    def get_photo_url(self, obj):
        request = self.context.get('request')
        url_image = obj.fingerprint.url
        return request.build_absolute_uri(url_image)

class UserInfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','name', 'date_of_birth', 'about', 'phone','image_url','date_joined','last_login')
    
    def get_photo_url(self, obj):
        request = self.context.get('request')
        url_image = obj.fingerprint.url
        return request.build_absolute_uri(url_image)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.about = validated_data.get('about', instance.about)
        instance.save()
        return instance

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'