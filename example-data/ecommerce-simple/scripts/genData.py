#
# ~ Fake Retail Data Generator ~
# This script generates fake item, user, and order data for demonstration purposes
#
# Author: Jeremy Pedersen
# Created: 2020-11-04
# Updated: 2021-03-15
#
import names, random

userNum = 1000 # Generate 1000 users
orderNum = 10000 # Generate 10000 orders
productNum = 100 # Generate 100 products

#
# Generate users
#

# Pull in list of country names and country codes, which we will
# select from at random when creating new users
f = open('countries.csv', 'r')
countries = [x.split(',') for x in f.read().split('\n')]
f.close()

# Open CSV file to store user data
f = open('users.csv','w')
f.write('user_id,name,age,sex,country,country_code\n') # Header row for CSV file

for i in range(0,userNum):

    # Generate user ID (sequential, from 0 to N)
    user_id = str(i)

    # Randomly select user's age
    age = random.randint(18,80)
    
    # Choose user's gender, and generate a name that matches the 
    # selected gender
    if random.random() > 0.5:
        sex = 'M'
        name = names.get_full_name(gender='male')
    else:
        sex = 'F'
        name = names.get_full_name(gender='female')

    # Choose random country of origin for user
    index = random.randint(1,len(countries)-1)
    location = countries[index][0]
    country_code = countries[index][1]

    # Write user data out to new row in CSV file
    f.write('{},{},{},{},{},{}\n'.format(user_id, name, age, sex, location, country_code))

f.close()

#
# Generate product data
#
def fakename():
    # Create a fake, IKEA-style product name by mixing random vowels and consonants
    # according to the pattern "CVCCVC"
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    lc = len(consonants) - 1
    lv = len(vowels) - 1

    product = ''.join([
        consonants[random.randint(0,lc)],
        vowels[random.randint(0,lv)],
        consonants[random.randint(0,lc)],
        consonants[random.randint(0,lc)],
        vowels[random.randint(0,lv)],
        consonants[random.randint(0,lc)]
    ])

    return product.title()

f = open('products.csv', 'w') 
f.write('product_id,product_name,price\n') # Header row for CSV file

for i in range(0,productNum):
    # Generate ID, name, and price for each product
    product_id = str(i)
    product_name = fakename()
    price = round(random.random() * 1000, 2)

    # Write product info out to new line in CSV file
    f.write('{},{},{}\n'.format(product_id,product_name,price))

#
# Generate orders
#
f = open('orders.csv', 'w')
f.write('order_id,year,month,product_code,quantity,user_id\n') # Header row for CSV file

for i in range(0,orderNum):

    # Generate order ID (sequential, 0 to N)
    order_id = str(i)

    # Generate year and month for order
    year = str(random.randint(2018,2020))
    month = str(random.randint(1,12))

    # Generate product code, purchase quantity, and user ID of purchaser
    # NOTE: "product code" and "user ID" need to fall inside the ranges
    # specified in the "for" loops above, as we may want to use this demo data
    # to demonstrate full table JOIN operations, which will require a 1-to-1 match
    # between users, products, and orders. 
    product_code = random.randint(0,productNum - 1)
    quantity = random.randint(1,10)
    user_id = random.randint(0,userNum - 1)

    # Write order information to a new line in the CSV file
    f.write('{},{},{},{},{},{}\n'.format(order_id, year, month, product_code, quantity, user_id))

f.close()
