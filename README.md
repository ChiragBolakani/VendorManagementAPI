# VendorManagementAPI
This backend provides required routes to implement a Vendor Management System.

It consists of the following models:
1. Vendor
   - Stores vendor information like name, contact details, address.
   - Has a unique identifier (vendor_code).
   - Tracks performance metrics:
     - On-time delivery rate
     - Average quality rating
     - Average response time
     - Fulfillment rate
    
2. Purchase Orders
   - Tracks order details:
     - Order date (order placed by buyer)
     -  Delivery date (delivery by vendor)
     -  Expected delivery date (required)
     -  ist of items (JSON format)
     -  Order quantity (minimum 1)
     -  Order status (pending, cancelled, completed)
     -  Quality rating (optional)
     -  Issue date (automatic on creation)
     -  Acknowledgement date (vendor acknowledges the order)
3. Performance History
   - Tracks historical performance data for vendors.
   - Linked to a specific vendor (vendor foreign key).
   - Stores performance metrics for a specific date:
     - On-time delivery rate
     - Average quality rating
     - Average response time
     - Fulfillment rate
       
## Perfomance Evaluation
Metrics:
- `On-Time Delivery Rate:` Percentage of orders delivered by the promised date.
- `Quality Rating:` Average of quality ratings given to a vendor’s purchase orders.
- `Response Time:` Average time taken by a vendor to acknowledge or respond to purchase orders.
- `Fulfilment Rate:` Percentage of purchase orders fulfilled without issues.

## Auth
The routes are protected using JWT Authentication. You need an access token to access the endpoints. 
| Method   | URL                                      | Description                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `POST`    | `/api/token`                             |Retrieve access and refresh token.                      |
| `POST`    | `/api/token`                             |Retrieve access and refresh token.                      |
| `POST`    | `/api/refresh/`                          | Retrieve new access token using refresh token.                       |
| `POST`    | `/api/token/blacklist`                          | Blackist a token.                       |


`/api/register`
request body:
```json
{
    "username": "testuser",
    "email": "test@test.com",
    "password": "<password>"
}
```

`/api/token`
request body:
```json
{
    "username": "testuser",
    "password": "<password>"
}
```

response:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTUwNjc4NSwiaWF0IjoxNzE1NDIwMzg1LCJqdGkiOiJhOWZmMjUwNzYxMDM0OGQyOGQ4MmQ1ODg0MzEyYjZhZCIsInVzZXJfaWQiOjF9.9wMgz2rmvJcudEMAU2xYQImdzaQnxvGxyRhf_I6XhM0",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1NDIxNTg1LCJpYXQiOjE3MTU0MjAzODUsImp0aSI6Ijg5MDM4Yjc3YjVjZjRlYzM4YjY4YjRmNWYzYTNkYzZjIiwidXNlcl9pZCI6MX0.TTn2BsszZwXxGxBK3K57hlCBUFG4zLQvGQmaNoRHrUw"
}
```

`/api/token/refresh`
request body:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTUwNjc4NSwiaWF0IjoxNzE1NDIwMzg1LCJqdGkiOiJhOWZmMjUwNzYxMDM0OGQyOGQ4MmQ1ODg0MzEyYjZhZCIsInVzZXJfaWQiOjF9.9wMgz2rmvJcudEMAU2xYQImdzaQnxvGxyRhf_I6XhM0"
}
```

response:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1NDYwMzczLCJpYXQiOjE3MTU0NTkxNDQsImp0aSI6IjE3NzIzMGVmOTQ0ODQ1YjVhOWE2N2RjMDQ0MDllYmYwIiwidXNlcl9pZCI6MX0.wtw_d7umBeL7A-0Gv6JJnSYknsJ3LmIeIFSmXvqJKm8"
}
```

## API Documentation
The API provides the following routes:
| Method   | URL                                      | Description                              |
| -------- | ---------------------------------------- | ---------------------------------------- |
| `GET`    | `/api/vendors`                             |Retrieve all vendors.                      |
| `GET`    | `/api/vendors/28`                          | Retrieve vendor #28.                       |
| `GET`    | `/api/vendors/28/purchase_orders`                          | Retrieve purhcase orders allocated to vendor #28.                       |
| `GET`    | `/api/vendors/28/performance`                          | Retrieve vendor #28 performance data.                       |
| `POST`   | `/api/vendors`                             | Create a new vendor.                       |
| `PUT`  | `/api/vendors/28`                          | Update data in vendor #28.                 |
| `DELETE`  | `/api/vendors/28`                          | Delete vendor #28.                 |
| `GET`    | `/api/purchase_orders` | Retrieve all purchase orders. |
| `GET`    | `/api/purchase_orders/28` | Retrieve purchase order with id 28. |
| `POST`   | `/api/purchase_orders`                             | Create a new purchase order.                       |
| `PUT` | `/api/purchase_orders/28` | Update data in purchase order 28.                    |
| `DELETE`  | `/api/purchase_orders/28`                          | Delete purchase order #28.                 |
