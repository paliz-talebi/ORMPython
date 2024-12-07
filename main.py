from peewee import *

# اتصال به پایگاه داده SQLite
db = SqliteDatabase('sales.db')

# مدل پایه
class BaseModel(Model):
    class Meta:
        database = db

# مدل Sales
class Sales(BaseModel):
    product_name = CharField()
    amount = FloatField()

# تابع اصلی
def main():
    # اتصال به پایگاه داده و ایجاد جدول
    db.connect()
    db.create_tables([Sales])

    # افزودن داده‌های نمونه
    sample_data = [
        {"product_name": "Product A", "amount": 100.0},
        {"product_name": "Product B", "amount": 200.0},
        {"product_name": "Product A", "amount": 50.0},
        {"product_name": "Product C", "amount": 300.0},
        {"product_name": "Product B", "amount": 150.0},
    ]
    Sales.insert_many(sample_data).execute()

    # محاسبه مجموع فروش برای هر محصول
    query = (Sales
             .select(Sales.product_name, fn.SUM(Sales.amount).alias('total_sales'))
             .group_by(Sales.product_name))

    # نمایش نتایج
    print("مجموع فروش هر محصول:")
    for record in query:
        print(f"محصول: {record.product_name}, مجموع فروش: {record.total_sales}")

    # بستن اتصال به پایگاه داده
    db.close()

if __name__ == "__main__":
    main()
