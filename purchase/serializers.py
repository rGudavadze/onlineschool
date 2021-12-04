from rest_framework import serializers
from user.models import User
from .models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'product', )
        # depth = 1

    def validate(self, attrs):
        user = attrs.get('user')
        product = attrs.get('product')

        if user.purchase.filter(product=product).first():
            raise serializers.ValidationError("You already own this product!")

        return super().validate(attrs)

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance
