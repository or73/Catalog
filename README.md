# Items & Categories Project

## Description   
Provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
This is a dynamic website with persistent data storage to create a web application that provides ac compelling service to th users.   
 
## Languages, Frameworks & Style Sheets 

| Item                      | Description  |
|:---                       |:---          |
| Frameworks                | Bootstrap    | 
| Languages                 | Python 3     |
| Protocols                 | HTTP, TCP    |
| Markup Language           | HTML         |
| Object Relational Mapper  | SQLAlchemy   |
| Stylesheets Languages     | CSS          |
| Version Control           | Git, GitHub  |
| Web Application Framework | Flask        |

## DB Structure   

| Table         |Description                                                               |
|:---           |:---                                                                      |
| User          | User data table                                                          |
| Category      | Category data table                                                      |
| Item          | Item data table                                                          |
| User_Category | Table for many-to-many relationship between `User` and `Category` tables |
| Category_Item | Table for many-to-many relationship between `Item` and `Category` tables |


### `user` Table   

| Name    | Details                     | Description              |
|:---     |:---                         |:---                      |
| id      | int AUTO_INCREMENT unsigned | Unique `user` identifier |
| name    | varchar(250)                | `user` name              |
| email   | varchar(250)                | `user` email             |
| picture | varchar(250)                | `user` picture path      |
| profile | bool                        | `user` profile           |
|         |                             | `0`: user                |
|         |                             | `1`: admin               |
| created | datetime                    | `user` creation date     |
 
### `category` Table   

| Name        | Details                     | Description                  |
|:---         |:---                         |:---                          |
| id          | int AUTO_INCREMENT unsigned | Unique `category` identifier |
| name        | varchar(250)                | `category` name              |
| description | varchar(250)                | `category` description       |
| created     | datetime                    | `category` creation date     |

### `item` Table   

| Name        | Details                     | Description              |
|:---         |:---                         |:---                      |
| id          | int AUTO_INCREMENT unsigned | Unique `item` identifier |
| name        | varchar(250)                | `item` name              |
| description | varchar(250)                | `item` description       |
| price       | varchar(15)                 | `item` price             |
| created     | datetime                    | `item` creation date     |

### `item_category` Table    

| Name        | Details | Description                                |
|:---         |:---     |:---                                        |
| category_id | int     | Foreign Key - Unique `category` identifier |
| item_id     | int     | Foreign Key - Unique `item` identifier     | 

### `user_category` Table    

| Name        | Details | Description                                |
|:---         |:---     |:---                                        |
| category_id | int     | Foreign Key - Unique `category` identifier |
| user_id     | int     | Foreign Key - Unique `user` identifier     |


This is the Database Structure, and its relationships:   

![Database Structure](./static/images/DB.png)

## Routes / Paths
For this project the server is `localhost`, and the port is `5000`.  Then, for all the following routes/paths  add 
`http://localhost:5000` to the beginning.  Example: `http:localhost:5000/<path>`
### Public
#### Public Routes/Paths - Root   
![Public Routes/Paths - Root](./static/images/1.public_route_main.png)   

| Path     | Description                               |
|:---      |:---                                       |
| /        | Show a list of **Categories** & **Items** |
| /catalog |                                           |   

#### Public Routes/Paths - Category   
![Public Routes/Paths - Category](./static/images/2.public_route_category.png)      

| Path                            | Description                                         |
|:---                             |:---                                                 |
| /catalog/<category_id>/         | Show a list of **items** in a selected **Category** |
| /catalog</category_id>/category |                                                     |   

#### Public Routes/Paths - Item   
![Public Routes/Paths - Item](./static/images/3.public_route_category_item.png)      
| Path                             | Description                      |
|:---                              |:---                              |
| /catalog/category/<item_id>/     | Show data of a selected **item** |
| /catalog/category/<item_id>/item |                                  |


### Private   
#### Private Routes/Paths - Root
| Path             | Description                                                |
|:---              |:---                                                        |
| /private         | Show a list of **Categories** & **Items** after user login |
| /private/catalog |    with `update` & `delete` options                        |   

#### Private Routes/Paths - Category   
| Path                                    | Description                                                          |
|:---                                     |:---                                                                  |
| /private/catalog/<category_id>/         | Show a list of **items** in a selected **Category** after user login |
| /private/catalog</category_id>/category |    with `update` & `delete` options                                  |   

#### Private Routes/Paths - Item   
| Path                                     | Description                                       |
|:---                                      |:---                                               |
| /private/catalog/category/<item_id>/     | Show data of a selected **item** after user login |
| /private/catalog/category/<item_id>/item |    with `update` & `delete` options               |

