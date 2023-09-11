from rest_framework import serializers


try:

    from general.models import Product

except:
    pass 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:

        try:
            model = Product
        except:
            pass    
        fields = '__all__'

