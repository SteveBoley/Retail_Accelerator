import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from trino.dbapi import connect
from trino.auth import BasicAuthentication
import requests as req
import warnings 
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")

conn = connect(
    host="tcp.cheerful-maggot.dataos.app",
    port="7432",
    auth=BasicAuthentication("balaji","YXRsYXNfZTc1YzFhNjZhZTQwNmRiN2QyZjQ1MWIyMTZiMTA2NjQuODljMGJjZjUtNzVhMC00ZDFlLThkZGYtYWFiM2JlZWI0NDRl"),
    http_scheme="https",
    http_headers={"cluster-name": "minerva"}
)

url = "https://cheerful-maggot.dataos.app/atlas/public/dashboards/uP1JgXn3PxDfLXdkT4ZDzN2eqOLslqgs45MzBLum?org_slug=default"


customer_qr = "SELECT concat(first_name, CONCAT(' ', last_name)) AS full_name, age, gender, phone_number, email_id, birth_date,mailing_street, city, state, country, zip_code FROM icebasedev.retail_accelerator.customers"
customer_df = pd.read_sql(customer_qr,conn)

customer_names = list(customer_df["full_name"])
selected_customer = st.selectbox("Customer Name", customer_names)

product_views_qr = "SELECT full_name, days, sum(total_views) total_views FROM ( SELECT concat(first_name, concat(' ', last_name)) full_name, date_diff('day', CURRENT_TIMESTAMP, visit_start_time) days, count(visitorid) total_views FROM icebasedev.retail_accelerator.clickstream AS clickstream LEFT JOIN icebasedev.retail_accelerator.customers AS customers ON clickstream.clientid = customers.customer_id WHERE date_diff('day', CURRENT_TIMESTAMP, visit_start_time) BETWEEN 1 AND 180 GROUP BY 1, 2 ORDER BY 2 ) GROUP BY 1, 2 ORDER BY 2"
product_views_df = pd.read_sql(product_views_qr,conn)

addtocart_qr = "SELECT full_name, days, total_added_items_to_cart FROM ( SELECT CONCAT(first_name, CONCAT(' ', last_name)) full_name, date_diff('day', activity_ts, CURRENT_TIMESTAMP(6)) days, add_items_to_cart__total_items AS total_added_items_to_cart FROM ( SELECT customer.first_name, customer.last_name, activity_ts, SUM(add_items_to_cart.quantity) add_items_to_cart__total_items FROM ( SELECT * FROM icebasedev.retail_accelerator.customers ) AS customer LEFT JOIN ( SELECT activity_uuid, entity_id, activity_ts, feature1 AS transaction_id, feature2 AS product_sku, feature3 AS product_price, feature4 AS quantity, feature5 AS order_value FROM icebasedev.retail_accelerator.activity_schema_data WHERE activity = 'product_add' ) AS add_items_to_cart ON customer.customer_id = add_items_to_cart.entity_id GROUP BY 1, 2, 3 ) ) WHERE DAYS BETWEEN 1 AND 180 ORDER BY 2"
addtocart_df = pd.read_sql(addtocart_qr,conn)

order_qr = "SELECT concat(first_name, concat(' ', last_name)) full_name, DAY(order_date) day_number, count(order_id) total_order FROM postgres.retail_accelerator.orders orders JOIN icebasedev.retail_accelerator.customers customers ON orders.customer_id = customers.customer_id WHERE order_status != 'canceled' AND date_diff('day', current_date, order_date) BETWEEN 1 AND 180 GROUP BY 1, 2"
order_df = pd.read_sql(order_qr,conn) 

top_10_prod_qr = "SELECT full_name, product_name, total_quantity FROM ( SELECT full_name, product_name, total_quantity, ROW_NUMBER() OVER ( PARTITION BY full_name ORDER BY total_quantity DESC ) number FROM ( SELECT concat(cust.first_name, concat(' ', cust.last_name)) full_name, p1.product_name, sum(c1.product_quantity) total_quantity FROM icebasedev.retail_accelerator.clickstream AS c1 JOIN icebasedev.retail_accelerator.product AS p1 ON c1.productsku = p1.sku_id JOIN icebasedev.retail_accelerator.customers AS cust ON c1.clientid = cust.customer_id WHERE event_name = 'verify_order' GROUP BY 1, 2 ) ORDER BY 4 DESC ) WHERE number <= 10"
top_10_prod_df = pd.read_sql(top_10_prod_qr,conn)
# print(top_10_prod_df)

top_10_prodcat_qr = "SELECT full_name, product_subcategory, total_quantity FROM ( SELECT full_name, product_subcategory, total_quantity, ROW_NUMBER() OVER ( PARTITION BY full_name ORDER BY total_quantity DESC ) number FROM ( SELECT concat(cust.first_name, concat(' ', cust.last_name)) full_name, p1.product_subcategory, sum(c1.product_quantity) total_quantity FROM icebasedev.retail_accelerator.clickstream AS c1 JOIN icebasedev.retail_accelerator.product AS p1 ON c1.productsku = p1.sku_id JOIN icebasedev.retail_accelerator.customers AS cust ON c1.clientid = cust.customer_id WHERE event_name = 'verify_order' GROUP BY 1, 2 ) ORDER BY 4 DESC ) WHERE number <= 10"
top_10_prodcat_df = pd.read_sql(top_10_prodcat_qr,conn)
# print(top_10_prodcat_df)
segment_qr = "SELECT full_name, segment_name FROM ( SELECT concat(first_name, concat(' ', last_name)) AS full_name, segment_name FROM ( SELECT customer.first_name first_name, customer.last_name last_name, segment.name segment_name FROM ( SELECT * FROM icebasedev.retail_accelerator.customers ) AS customer LEFT JOIN ( SELECT b.segment_id, b.customer_id, a.name, a.lens FROM lensdb.public.segment AS a RIGHT JOIN icebase.audience_segment.segment_stream AS b ON CAST(a.guid AS VARCHAR) = b.segment_id ) AS segment ON customer.customer_id = segment.customer_id ORDER BY 1 ASC ) )"
segment_df = pd.read_sql(segment_qr,conn)


product_views_df = product_views_df[product_views_df['full_name'] == selected_customer]
addtocart_df = addtocart_df[addtocart_df['full_name'] == selected_customer]
top_10_prod_df = top_10_prod_df[top_10_prod_df['full_name'] == selected_customer]
top_10_prodcat_df = top_10_prodcat_df[top_10_prodcat_df['full_name'] == selected_customer]
order_df = order_df[order_df['full_name']== selected_customer]
segment_df = segment_df[segment_df['full_name'] == selected_customer]


tab1, tab2, tab3 ,tab4 = st.tabs(["Customer Profile", "Activity", "Orders", "Segment"])

with tab1:
    st.header("Customer Profile")

   
    selected_row = customer_df[customer_df["full_name"] == selected_customer].iloc[0]

    st.write("Full Name:", selected_row["full_name"])
    st.write("Gender:", selected_row["gender"])
    st.write("Phone Number:", selected_row["phone_number"])
    st.write("Email ID:", selected_row["email_id"])
    st.write("Birth Date:", selected_row["birth_date"].strftime('%Y-%m-%d'))
    st.write("Age:", selected_row["age"])
    st.write("Mailing Street:", selected_row["mailing_street"])
    st.write("City:", selected_row["city"])
    st.write("State:", selected_row["state"])
    st.write("Country:", selected_row["country"])
    st.write("Zipcode:", selected_row["zip_code"])


# order_views_df['full_name']=order_views_df['selected_customer']

with tab2:
    
    st.header("Activity")
    
    with st.expander("Product Views", expanded=False):
        st.line_chart(data=product_views_df, x="days", y="total_views")

    with st.expander("Add to Card", expanded=False):
        st.line_chart(data=addtocart_df, x="days", y="total_added_items_to_cart")

    with st.expander("Order Placed", expanded=False):
        st.line_chart(data=order_df, x="day_number", y="total_order")       

with tab3:
    st.header("Orders")

    with st.expander("Top 10 Products", expanded=False):
        st.bar_chart(data=top_10_prod_df, x="product_name", y="total_quantity")

    with st.expander("Top 10 Product Categories", expanded=False):
        st.bar_chart(data=top_10_prodcat_df, x="product_subcategory", y="total_quantity")

with tab4:
    st.header("Segment")
    

    def create_donut_chart(segment_df, selected_customer):
        selected_segments = segment_df[segment_df['full_name'] == selected_customer]['segment_name']
        segment_counts = selected_segments.value_counts()
        fig, ax = plt.subplots()
        ax.pie(segment_counts, labels=segment_counts.index, startangle=90, wedgeprops=dict(width=0.3))
        circle = plt.Circle((0, 0), 0.1, color='white')
        ax.add_artist(circle)
        ax.set_aspect('equal')
        ax.set_title(f'Segment Distribution - {selected_customer}')
        st.pyplot(fig)

    create_donut_chart(segment_df, selected_customer)
