import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from trino.dbapi import connect
from trino.auth import BasicAuthentication
import warnings 
import graphviz as gv
from datetime import datetime

warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")

conn = connect(
    host="tcp.cheerful-maggot.dataos.app",
    port="7432",
    auth=BasicAuthentication("balaji","YXRsYXNfZTc1YzFhNjZhZTQwNmRiN2QyZjQ1MWIyMTZiMTA2NjQuODljMGJjZjUtNzVhMC00ZDFlLThkZGYtYWFiM2JlZWI0NDRl"),
    http_scheme="https",
    http_headers={"cluster-name": "minervac"}
)

url = "https://cheerful-maggot.dataos.app/atlas/public/dashboards/uP1JgXn3PxDfLXdkT4ZDzN2eqOLslqgs45MzBLum?org_slug=default"


customer_qr = "SELECT customer_id, concat(first_name, CONCAT(' ', last_name)) AS full_name, age, gender, phone_number, email_id, birth_date, mailing_street, city, state, country, zip_code FROM icebasedev.retail_accelerator.customers"
customer_df = pd.read_sql(customer_qr,conn)

customer_id = list(customer_df["customer_id"])
selected_customer = st.text_input("Customer ID")


product_views_qr = "SELECT customer_id, days, sum(total_views) total_views FROM ( SELECT customer_id, date_diff('day', CURRENT_TIMESTAMP, visit_start_time) days, count(visitorid) total_views FROM icebasedev.retail_accelerator.clickstream AS clickstream LEFT JOIN icebasedev.retail_accelerator.customers AS customers ON clickstream.clientid = customers.customer_id WHERE date_diff('day', CURRENT_TIMESTAMP, visit_start_time) BETWEEN 1 AND 180 GROUP BY 1, 2 ORDER BY 2 ) GROUP BY 1, 2 ORDER BY 2"
product_views_df = pd.read_sql(product_views_qr,conn)

addtocart_qr = '''SELECT customer_id, day_number, total_cart_items FROM (SELECT "customer.customer_id" AS customer_id, date_diff('day', "items_added_to_cart.activity_ts.day", current_date) AS day_number, "items_added_to_cart.total_cart_items" AS total_cart_items FROM LENS (SELECT "items_added_to_cart.total_cart_items", "customer.customer_id" FROM c360_solution_accelerator DATE "items_added_to_cart.activity_ts" RANGE "" GRANULARITY DAY TIMEZONE ("Asia/Kolkata")) ) WHERE day_number BETWEEN 1 AND 180'''
addtocart_df = pd.read_sql(addtocart_qr,conn)

order_qr = '''SELECT customer_id, quantity, day_number FROM ( SELECT "customer.customer_id" AS customer_id, "order_placed.quantity" AS quantity, date_diff( 'day', "order_placed.activity_ts.day", current_date ) AS day_number FROM LENS ( SELECT "customer.customer_id", "order_placed.quantity" FROM c360_solution_accelerator DATE "order_placed.activity_ts" RANGE "" GRANULARITY DAY TIMEZONE ("Asia/Kolkata") ) ) WHERE day_number BETWEEN 1 AND 180'''
order_df = pd.read_sql(order_qr,conn) 

top_10_prodcat_qr = "SELECT customer_id, product_subcategory, total_quantity FROM ( SELECT customer_id, product_subcategory, total_quantity, ROW_NUMBER() OVER ( PARTITION BY customer_id ORDER BY total_quantity DESC ) number FROM ( SELECT cust.customer_id, p1.product_subcategory, sum(c1.product_quantity) total_quantity FROM icebasedev.retail_accelerator.clickstream AS c1 JOIN icebasedev.retail_accelerator.product AS p1 ON c1.productsku = p1.sku_id JOIN icebasedev.retail_accelerator.customers AS cust ON c1.clientid = cust.customer_id WHERE event_name = 'verify_order' GROUP BY 1, 2 ) ORDER BY 4 DESC ) WHERE number <= 10"
top_10_prodcat_df = pd.read_sql(top_10_prodcat_qr,conn)
# print(top_10_prod_df)

top_10_prod_qr = "SELECT customer_id, product_name, total_quantity FROM ( SELECT customer_id, product_name, total_quantity, ROW_NUMBER() OVER ( PARTITION BY customer_id ORDER BY total_quantity DESC ) number FROM ( SELECT cust.customer_id, p1.product_name, sum(c1.product_quantity) total_quantity FROM icebasedev.retail_accelerator.clickstream AS c1 JOIN icebasedev.retail_accelerator.product AS p1 ON c1.productsku = p1.sku_id JOIN icebasedev.retail_accelerator.customers AS cust ON c1.clientid = cust.customer_id WHERE event_name = 'verify_order' GROUP BY 1, 2 ) ORDER BY 4 DESC ) WHERE number <= 10"
top_10_prod_df = pd.read_sql(top_10_prod_qr,conn)
# print(top_10_prodcat_df)
segment_qr = '''SELECT customer_id, full_name, segment_name FROM ( SELECT "customer.customer_id" AS customer_id, concat( "customer.first_name", concat(' ', "customer.last_name") ) AS full_name, "segment.segment_name" AS segment_name FROM LENS ( SELECT "customer.customer_id", "customer.first_name", "customer.last_name", "segment.segment_name" FROM c360_solution_accelerator ) )'''
segment_df = pd.read_sql(segment_qr,conn)


product_views_df = product_views_df[product_views_df['customer_id'] == selected_customer]
addtocart_df = addtocart_df[addtocart_df['customer_id'] == selected_customer]
top_10_prod_df = top_10_prod_df[top_10_prod_df['customer_id'] == selected_customer]
top_10_prodcat_df = top_10_prodcat_df[top_10_prodcat_df['customer_id'] == selected_customer]
order_df = order_df[order_df['customer_id']== selected_customer]
segment_df = segment_df[segment_df['customer_id'] == selected_customer]


tab1, tab2, tab3 ,tab4 = st.tabs(["Customer Profile", "Activity", "Orders", "Segment"])

with tab1:
    st.header("Customer Profile")

   
    selected_row = customer_df[customer_df["customer_id"] == selected_customer]#.iloc[0]
    print(selected_row)

    st.write("Full Name:", selected_row["full_name"].values[0])
    st.write("Gender:", selected_row["gender"].values[0])
    st.write("Phone Number:", selected_row["phone_number"].values[0])
    st.write("Email ID:", selected_row["email_id"].values[0])
    st.write("Birth Date:",selected_row["birth_date"].values[0])
    st.write("Age:", selected_row["age"].values[0])
    st.write("Mailing Street:", selected_row["mailing_street"].values[0])
    st.write("City:", selected_row["city"].values[0])
    st.write("State:", selected_row["state"].values[0])
    st.write("Country:", selected_row["country"].values[0])
    st.write("Zipcode:", selected_row["zip_code"].values[0])


# order_views_df['full_name']=order_views_df['selected_customer']

with tab2:
    
    st.header("Activity")
    
    with st.expander("Product Views", expanded=False):
        st.line_chart(data=product_views_df, x="days", y="total_views")

    with st.expander("Add to Card", expanded=False):
        st.line_chart(data=addtocart_df, x="day_number", y="total_cart_items")

    with st.expander("Order Placed", expanded=False):
        st.line_chart(data=order_df, x="day_number", y="quantity")       

with tab3:
    st.header("Orders")

    with st.expander("Top 10 Products", expanded=False):
        st.bar_chart(data=top_10_prod_df, x="product_name", y="total_quantity")

    with st.expander("Top 10 Product Categories", expanded=False):
        st.bar_chart(data=top_10_prodcat_df, x="product_subcategory", y="total_quantity")

with tab4:
    st.header("Segment")

    def create_graphviz_chart(segment_df):
        chart = gv.Digraph()
        customers = segment_df['full_name'].unique()

        for customer in customers:
            segments = segment_df[segment_df['full_name'] == customer]['segment_name']
            segment_labels = '\n'.join(segments)
            chart.node(customer, label=f'{customer}\n{segment_labels}')

        st.graphviz_chart(chart.pipe(format='svg').decode('utf-8'), use_container_width=True)

    # Sample data (replace with your actual data)
    segment_df = pd.DataFrame(segment_df)  # Replace ... with your data

    create_graphviz_chart(segment_df)

        