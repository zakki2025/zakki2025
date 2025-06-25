from . import ma
from .models import Shop

class ShopSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shop
        load_instance = True

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)

class ChartData(ma.Schema):
    class Meta:
        fields = ('name', 'value')

chart_schema = ChartData(many=True)
