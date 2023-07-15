from tortoise import fields
from tortoise.models import Model


# Модель для хранения данных о ставках
class Rate(Model):
    id = fields.IntField(pk=True)
    cargo_type = fields.CharField(max_length=255)
    rate = fields.DecimalField(max_digits=10, decimal_places=2)
    effective_date = fields.DateField()

    class Meta:
        table = "rates"
