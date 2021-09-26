# Large-Data-Processing
Python file which can we use to update the large file in the mysql type database

# Steps to run the file
1. Copy the project in the local.
2. Open the terminal go to the folder where you copy the project.
3. Install the required modules present in requirement.txt file using this command\
    ```pip install -r requirements.txt```\
4. Create a environment variable with name "MYSQLDB". It contain the user name, password and port address of the data base in this formate.
 ```
export MYSQLDB = mysql://<username>:<password>@<ip address>:<port>
```
5. There are 3 different things you can do using large_data_processing.py.\
  a. Can ingest the product.csv using this command.\
      ```python3 large_data_processing.py --action upload_product_details --database <database name> --csv <csv file address> ```\
      Here database name is where you want to store the product detail table.\
  b. Update the product count table using this command.\
      ```python3 large_data_processing.py --action update_product_count_table --database <database name>```\
      Here database name is where product detail table is stored.\
  c. Update the product detail table on the basis of "sku" key.\
      i. To update name and description both:-\
      ```python3 large_data_processing.py --action update_product_details_table --database <database name> --sku <sku key value> --name <updated name value> --desc <updated description>```\
      ii. To Update name only:-\
      ```python3 large_data_processing.py --action update_product_details_table --database <database name> --sku <sku key value> --name <updated name value>```\
      iii. To Update description only:-\
      ``` python3 large_data_processing.py --action update_product_details_table --database <database name> --sku <sku key value>  --desc <updated description>```

# Tables Used
1. product_details - To store the product.csv.\
    <img width="1772" alt="Screenshot 2021-09-26 at 6 45 25 PM" src="https://user-images.githubusercontent.com/38307298/134809672-3d179b8b-597f-487e-9fa4-bddec52402ce.png">\
    Columns in the table\
    a. name - name of the product.\
    b. sku - is use to update the table.\
    c. description - description of the product.\
    d. upload_date - date at which a perticular entry is appended in the table, this is use when we perfrom the aggregation query.
2. product_count - To store the aggregated value of name and no. of products.\
    <img width="419" alt="Screenshot 2021-09-26 at 6 48 02 PM" src="https://user-images.githubusercontent.com/38307298/134809749-787a2318-0cfb-423e-a912-47f7208fbe62.png">\
     Columns in the table\
    a. name - name of the product.\
    b. no. of products - no. of products with a perticular name.
3. product_count_update_date - To store upto which date the product_count table is updated.\
    <img width="428" alt="Screenshot 2021-09-26 at 6 50 16 PM" src="https://user-images.githubusercontent.com/38307298/134809816-22247557-49fa-464d-abc9-be3742505b8b.png">\
    Columns in the table\
    a. update_date - date upto which product_count table is updated as per the upload_date column present in product_details table.

# This to improve in the code if got more time.
1. Add a table which store the action type is perform and status of that command, if a error occurs than store the error.
2. Add support to use different sql based databases.
