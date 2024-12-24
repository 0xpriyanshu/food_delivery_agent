import time
from fuzzywuzzy import process  # For string matching

# Example Order Data
class Order:
    def __init__(self, pizza_name, quantity):
        self.pizza_name = pizza_name
        self.quantity = quantity
        self.status = 'Ordered'  # Possible states: Ordered, Cooking, Ready, Delivered
        self.review_requested = False

# Agent 1: Customer Bot with NLP
class CustomerBot:
    def __init__(self):
        self.orders = []  # To store multiple orders
        self.pizza_list = ["Margherita", "Onion", "BBQ Chicken", "Veggie", "Paneer", 
                           "Mushroom", "Tomato", "Corn", "Spicy Sausage", "Farmhouse"]

    def select_pizza(self):
        while True:
            print("Please select a pizza from the following menu:")
            for i, pizza in enumerate(self.pizza_list, 1):
                print(f"{i}. {pizza}")
            
            pizza_choice = input("You can either type the name of the pizza or the number: ").lower()

            # Check if input is a number
            if pizza_choice.isdigit():
                pizza_choice = int(pizza_choice) - 1  # Convert to zero-based index
                if 0 <= pizza_choice < len(self.pizza_list):
                    pizza_name = self.pizza_list[pizza_choice]
                    print(f"Your selected pizza is: {pizza_name}")
                else:
                    print("Invalid selection. Please select a valid pizza number.")
                    continue
            else:
                # Using fuzzy matching for name-based selection
                matched_pizza, score = process.extractOne(pizza_choice, self.pizza_list)

                if score >= 80:  # Acceptable match (80% or above match)
                    pizza_name = matched_pizza
                    print(f"Your selected pizza is: {pizza_name}")
                else:
                    print("Sorry, I couldn't find that pizza. Please select from the list.")
                    continue
            
            # Get quantity
            quantity = input(f"Enter the quantity for {pizza_name}: ")
            if quantity.isdigit() and int(quantity) > 0:
                quantity = int(quantity)
                self.orders.append(Order(pizza_name, quantity))
                print(f"{quantity} x {pizza_name} added to your order.")
            else:
                print("Invalid quantity. Please enter a valid number greater than 0.")
                continue

            # Ask if user wants to order more pizzas
            another = input("Do you want to select another pizza? (yes/no): ").lower()
            if another != 'yes':
                break
        
        self.confirm_payment()

    def confirm_payment(self):
        print("Do you agree to charge your Web3 wallet for this order? (Yes/No)")
        response = input()
        if response.lower() == "yes":
            print("Payment confirmed! Your order will be prepared soon.")
            self.communicate_to_restaurant()
        else:
            self.offer_alternate_payment()

    def offer_alternate_payment(self):
        print("You selected 'No'. Please choose an alternative payment method:")
        print("1. Credit Card")
        print("2. Paytm")
        choice = int(input("Select payment method by number: "))
        if choice == 1:
            print("Credit Card payment selected. Please enter your card details.")
            self.communicate_to_restaurant()
        elif choice == 2:
            print("Paytm payment selected. Open Paytm app and do the payment.")
            self.communicate_to_restaurant()
        else:
            print("Invalid selection. Please select a valid payment method.")
            self.offer_alternate_payment()

    def communicate_to_restaurant(self):
        print("Communicating order to Restaurant Bot...")
        # Send entire order (all pizzas and quantities) to the restaurant
        restaurant_bot.accept_order(self.orders)

    def ask_for_review(self):
        # Wait for 20 seconds before asking for the review of all pizzas
        time.sleep(20)
        
        # Ask for review after delay for all pizzas in the order
        for order in self.orders:
            if not order.review_requested:
                print(f"Please leave a review for your {order.quantity} x {order.pizza_name} pizza!")
                order.review_requested = True

# Agent 2: Restaurant Bot
class RestaurantBot:
    def __init__(self):
        pass
    
    def accept_order(self, orders):
        print(f"Order for {sum([order.quantity for order in orders])} pizzas received. Starting to prepare...")
        # Prepare all pizzas together
        time.sleep(10)  # Cooking time for all pizzas
        for order in orders:
            order.status = 'Cooking'
            print(f"Your {order.pizza_name} pizza is cooking...")

        self.update_order_status(orders)
        
    def update_order_status(self, orders):
        print("All pizzas are ready for delivery!")
        for order in orders:
            order.status = 'Ready'
        delivery_bot.assign_driver(orders)

# Agent 3: Delivery Bot
class DeliveryBot:
    def __init__(self):
        pass
    
    def assign_driver(self, orders):
        print(f"Assigning driver to deliver {sum([order.quantity for order in orders])} pizzas...")
        time.sleep(10)  # Delivery time for all pizzas
        for order in orders:
            order.status = 'Delivered'
        self.update_customer(orders)

    def update_customer(self, orders):
        for order in orders:
            print(f"Your {order.quantity} x {order.pizza_name} pizza has been delivered!")
        customer_bot.ask_for_review()

# Initialize bots
customer_bot = CustomerBot()
restaurant_bot = RestaurantBot()
delivery_bot = DeliveryBot()

# Start the process
customer_bot.select_pizza()
