# Large-Data-Processing
Python file which can we use to update the large file in the mysql type database

# Steps to run the file
1. Copy the project in the local
2. Open the terminal go to the folder where you copy the project.
4. Install the required modules present in requirement.txt file using this command
    pip install -r requirements.txt
5. Create a environment variable with name "MYSQLDB". It contain the user name, password and port address of the data base in this formate.
 ```
export MYSQLDB = mysql://<username>:<password>@<ip address>:<port>
```
6. There are 3 different things you can do using large_data_processing.py.
    a. Can ingest the product.csv using this command.
        python3 large_data_processing.py --action upload_product_details --database <database name> --csv <csv file address> 
        Here database name is where you want to store the product detail table.
    b. Update the product count table using this command.
        python3 large_data_processing.py --action update_product_count_table --database <database name>
        Here database name is where product detail table is stored.
    c. Update the product detail table on the basis of "sku" key.
       i. To update name and description both:-
          python3 large_data_processing.py --action update_product_details_table --database <database name> --sku <sku key value> --name <updated name value> --desc            <updated description>
       ii. To Update name only:-
          python3 large_data_processing.py --action update_product_details_table --database <database name> --sku <sku key value> --name <updated name value>
       ii. To Update description only:-
          python3 large_data_processing.py --action update_product_details_table --database <database name> --sku <sku key value>  --desc <updated description>
