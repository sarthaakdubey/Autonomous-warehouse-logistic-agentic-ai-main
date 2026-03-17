data = """order_id,warehouse,product,quantity,distance_km,transport_mode,delay,picking_time_min
1001,Indore,Electronics,5,230,Truck,Yes,45
1002,Bhopal,Furniture,2,120,Van,No,18
1003,Indore,Clothing,12,560,Truck,Yes,55
1004,Delhi,Electronics,1,40,Bike,No,10
1005,Indore,Furniture,4,300,Truck,Yes,50
1006,Bhopal,Clothing,8,80,Van,No,15
"""

with open("logistics_dataset.csv", "w") as file:
    file.write(data)

print("CSV file created successfully!")
