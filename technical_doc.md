[Following Backend Basic Features](https://excalidraw.com/#json=4azlKRgj0UYs3oJKsitXN,-A6byzcdubEiuevVPXwGZg)

# Business Logic

## Users-Level

### Users

-   **User Roles**
    -   `Anyone` - All unahintcated users
    -   `Customer` - is the default authintcated user
    -   `Vendor` - is the user that has Market
    -   `Staff` - is the user that has access to the admin site
    -   `Superuser` - is the user that has Full-Access

---

-   `Anyone`
    -   Create a new account (Verify account before create it)
-   `Customer`
    -   Setup own account as vendor (By creating Market-Account)
    -   Update/Delete/Retrieve own account
-   `Vendor`
    -   Edit/Delete/Retrieve own Market-Account

---

-   **Signals**
    -   After CREATE Market --> UPDATE User role to seller
    -   After DELETE Market --> UPDATE User role to buyer
    -   After CREATE User --> CREATE Cart object

---

### Stores

-   Anyone:
    -   LIST stores
    -   RETRIEVE store
-   Authenticated:
    -   CREATE new store
    -   RERIEVE own store
-   Seller:
    -   UPDATE/DELETE own store

---

-   urls:
    -   `stores/` LIST, CREATE
    -   `stores/<uuid:pk>/` RETRIEVE, UPDATE, DELETE
    -   `store/` RETRIEVE auth user store

---

-   Pagination applied
-   Searcing by name

---

### Addresses

-   Anyone:
    -   RETRIEVE/LIST stores addresses
-   Customer:
    -   CREATE/UPDATE/DELETE/RETRIEVE/LISTS own address
        -   Notice: that user has access only on his own addresses
-   Vendor:
    -   CREATE/UPDATE/DELETE/RETRIEVE own store adress

---

-   **views:**
    -   viewset for store addreses
    -   viewset for user addresses

---

-   **urls:**
    -   `store/addresses/` LIST store addresess
    -   `store/addresses/<uuid:pk>` CREATE/UPDATE/DELETE own store addreses | RETRIEVE anyone
    -   `users/addresses/` LIST own user address
    -   `users/addreses/<uuid:pk>` CREATE/UPDATE/DELETE/RETRIEVE own user address

---

## Products-Level

### Categories

**Permissions**

-   `Admin`
    -   CREATE/UPDATE/DELETE Categories
-   `Anyone`
    -   RETRIEVE/LIST Categories

---

-   **views:**
    -   Category ViewSet for all operations

---

-   **urls:**
    -   `categories` CREATE/LIST
    -   `categories/<uuid:pk>` UPDATE/DELETE/RETRIEVE

---

### Products

-   **permissions:**
    -   `Vendor`
        -   CREATE/UPDATE/DELETE/RETRIEVE/LIST own Products
    -   `Anyone`
        -   RETRIEVE/LIST Products

---

-   **views:**
    -   ViewSet for all vendor operations
    -   ViewGeneric for list
    -   ViewGeneric for retrive

---

-   **urls:**
    -   For Vendor
        -   `store/products` CREATE/LIST
        -   `store/products/<uuid:pk>` UPDATE/RETRIEVE/DELETE
    -   For Customer
        -   `products` LIST
        -   `products/<uuid:pk>` RETRIEVE

---

-   Filter Products by (Category, Price, Rate)
-   Sort Products by (Price, Rate)
-   Search
-   Pagination applied on Products and Categories

### Reviews

-   **permissions:**
    -   `Customer`
        -   CREATE/UPDATE/DELETE/RETRIEVE/LIST Reviews

---

-   **exceptions&validations:**
    -   Seller can't review own Products
    -   Customer can't review product twice

---

-   **views:**
    -   ViewSet for all operations

---

-   **urls:**
    -   `products/<uuid:pk>/reviewes`
    -   `products/<uuid:pk>/reviews/<uuid:pk>`

---

-   Filter reviews by (Product, Rate, Seller, user)
-   Sort reviews by
-   Search throug Comments
-   Pagination applied to reviews

## Cart-Level

### Cart&CartItem

-   Cart object created automatically when new user creates account

---

-   `Customer`
    -   CREATE/UPDATE/DELETE/RETRIEVE/LIST own CartItems
    -   Custome logic
        -   DESTROY Cart -> this removes all cart items

---

-   **views:**
    -   One ViewSet for all operations
        -   DestroyCart function-view

---

-   **urls:**
    -   `cart-items/` CREATE/LIST
    -   `cart-items/<uuid:pk>` UPDATE/DELETE/RETRIEVE

---

## Orders-Level

### Order & OrderItems

-   `Customer`
    -   LIST Orders
    -   LIST OrderItems
    -   MAKE Payment

---

-   **views:**
    -   2 list views
    -   list orders with (ordered by date)

---

-   **urls:**
    -   `orders/` LIST Orders
    -   `orders/<uuid:pk>/` LIST OrderItems
    -   `payment/` MAKE Payment

---

-   **signals:**
    -   After UPDATE Payment --> IF Pyament-Status is Completed
        -   Create Order object
        -   Create OrderItems object
        -   Send Mail to customer about order
    -   After CREATE OrderItem
        -   Clean Cart from CartItem related
        -   Update stock_quantity
    -   After UPDATE Order --> If Order-Status is shipped
        -   Send mail to cutomer

---

# Overall Technical Overview

## End-Points List

## End-Points Features

### Filtering/Sorting/Searching

-   Categories
    -   Alphabetical Order

## Authentication/Authorization

-   Use basic setup of jwt
-   Setup permessions for each role
    -   Any - Buier - Seller - Admin

## Exceptions & Validations

> Enure Consistency, Integrity ...

-   Model level vlidations
    -   Secure DB level
-   Serializer level validations
    -   Check valid data before go to db
-   Create Endpoints exceptions
    -   Permissions

## Email Services

-   Verify email before creating
-   Order Created mail
    -   Send Mail to customer about order after complete payment
-   Shipping mail
    -   When order is shipped

## Signals

## Caching

## Throttling

## Scripts Utils

## Payment Integrations

## Deployment solutions

## seed-strategy

#### users

```
create 5 customers
create 3 sellers

create 3 stores 1 for each seller

create 3 addresses 1 for 3 customers
create 4 addresses 2 for 2 customers
create 3 addresses 1 for each store
```

#### products

```
create 5 categoreis

create 9 products 3 for each store
create 3 products 1 for each store without category

create 10 reviewes 2 by each customer
create 6 reviewes 2 by each seller
```

-   users app
    -   After create market, update user role to seller
    -   After delete market, update user role to buyer
    -   After create user, create cart object
