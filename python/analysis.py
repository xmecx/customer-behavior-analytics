## Завантаження даних
import pandas as pd
import matplotlib.pyplot as plt

customers = pd.read_csv("data/customers.csv")
sales = pd.read_csv("data/sales.csv")

print(customers.head())
print(sales.head())

## Кількість замовлень на клієнта
orders_per_customer = (
        sales
        .groupby("customer_id")
        .agg(orders_count=("invoice_id", "count"))
        .reset_index()
)

print(orders_per_customer)

## Додати всіх клієнтів (навіть без замовлень)
customers_full = customers.merge(
        orders_per_customer,
        on="customer_id",
        how="left"
)

customers_full["orders_count"] = customers_full["orders_count"].fillna(0).astype(int)

print(customers_full.head())

## Статус клієнта
def customer_status(count):
        if count == 0:
            return "inactive"
        elif count == 1:
            return "new"
        else:
            return "active"

customers_full["customer_status"] = customers_full["orders_count"].apply(customer_status)

print(customers_full[["customer_id", "orders_count", "customer_status"]].head())

## Розподіл клієнтів
status_distribution = customers_full["customer_status"].value_counts()
print(status_distribution)

##Дохід в sales
sales["total_amount"] = sales["amount"]

##Рахуємо дохід по клієнтах
revenue_per_customer = (
     sales 
     .groupby("customer_id")
     .agg(total_revenue=("total_amount", "sum"))
     .reset_index()
)

##Приєднюємо до основної таблиці
customers_full = customers_full.merge(
     revenue_per_customer,
     on="customer_id",
     how="left"
)

customers_full["total_revenue"] = (
     customers_full["total_revenue"]
     .fillna(0)
)

##Аналіз по статусах##
##Загальний дохід по статусах
revenue_by_status = (
     customers_full
     .groupby("customer_status")
     .agg(
          customer_count = ("customer_id", "count"),
          total_revenue = ("total_revenue", "sum"),
          avg_revenue = ("total_revenue", "mean")
     )
)

print(revenue_by_status)

##Візуалізація##
##Розподіл клієнтів

customers_full["customer_status"].value_counts().plot(kind="bar")
plt.title("Розподіл клієнтів за статусом")
plt.xlabel("Статус")
plt.ylabel("Кількість клієнтів")
plt.tight_layout()
plt.show()

##Дохід по статусах
revenue_by_status["total_revenue"].plot(kind="bar")
plt.title("Загальний дохід по статусах клієнтів")
plt.ylabel("Дохід")
plt.tight_layout()
plt.show()
