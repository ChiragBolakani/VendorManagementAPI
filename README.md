# VendorManagementAPI
This backend provides required routes to implement a Vendor Management System.


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
