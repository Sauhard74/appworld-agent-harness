
### Environment Interaction 1
----------------------------------------------------------------------------
```python
# Get the access token for the main user's Amazon account
amazon_access_token = apis.amazon.access_token_from(apis.supervisor.main_user)

# Get the access token for the main user's phone
phone_access_token = apis.phone.access_token_from(apis.supervisor.main_user)

# Search for the partner's phone number in the main user's contact book
partner_contact = apis.phone.search_contacts(
    access_token=phone_access_token, query="partner", relationship="partner"
)

# Get the partner's phone number
partner_phone_number = partner_contact[0].phone_number

# Get the main user's Amazon wish list
wish_list = apis.amazon.show_wish_list(amazon_access_token)

# Create a list to store the itemized wish list
itemized_wish_list = []

# Iterate over each product in the wish list
for product in wish_list:
    # Calculate the total price of the product
    total_price = round(product.price * product.quantity)

    # Add the product to the itemized wish list
    itemized_wish_list.append(f"{product.name} => ${total_price}")

# Join the itemized wish list into a single string
message = "\n".join(itemized_wish_list)

# Print the message to be sent to the partner
print(message)
```

```
Execution failed. Traceback:
  File "<python-input>", line 2, in <module>
    amazon_access_token = apis.amazon.access_token_from(apis.supervisor.main_user)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'access_token_from' found in the amazon app.
```


### Environment Interaction 2
----------------------------------------------------------------------------
```python
# Get the access token for the main user's Amazon account
print(apis.amazon.api_docs.show_api_descriptions())

# Get the access token for the main user's phone
print(apis.phone.api_docs.show_api_descriptions())

# Search for the partner's phone number in the main user's contact book
print(apis.phone.api_docs.show_api_doc('search_contacts'))

# Get the main user's Amazon wish list
print(apis.amazon.api_docs.show_api_descriptions())
```

```
Execution failed. Traceback:
  File "<python-input>", line 2, in <module>
    print(apis.amazon.api_docs.show_api_descriptions())
          ^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'api_docs' found in the amazon app.
```


### Environment Interaction 3
----------------------------------------------------------------------------
```python
# Get the API descriptions for all apps
print(apis.supervisor.api_docs.show_app_descriptions())

# Get the API descriptions for the amazon app
print(apis.supervisor.api_docs.show_api_descriptions('amazon'))

# Get the API descriptions for the phone app
print(apis.supervisor.api_docs.show_api_descriptions('phone'))
```

```
Execution failed. Traceback:
  File "<python-input>", line 2, in <module>
    print(apis.supervisor.api_docs.show_app_descriptions())
          ^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'api_docs' found in the supervisor app.
```


### Environment Interaction 4
----------------------------------------------------------------------------
```python
# Get the API descriptions for all apps
print(apis.api_docs.show_app_descriptions())

# Get the API descriptions for the amazon app
print(apis.api_docs.show_api_descriptions(app_name='amazon'))

# Get the API descriptions for the phone app
print(apis.api_docs.show_api_descriptions(app_name='phone'))
```

```
[
 {
  "name": "api_docs",
  "description": "An app to search and explore API documentation."
 },
 {
  "name": "supervisor",
  "description": "An app to access supervisor's personal information, account credentials, addresses, payment cards, and manage the assigned task."
 },
 {
  "name": "amazon",
  "description": "An online shopping app to buy products and manage orders, returns, etc."
 },
 {
  "name": "phone",
  "description": "An app to find and manage contact information for friends, family members, etc., send and receive messages, and manage alarms."
 },
 {
  "name": "file_system",
  "description": "A file system app to create and manage files and folders."
 },
 {
  "name": "spotify",
  "description": "A music streaming app to stream songs and manage song, album and playlist libraries."
 },
 {
  "name": "venmo",
  "description": "A social payment app to send, receive and request money to and from others."
 },
 {
  "name": "gmail",
  "description": "An email app to draft, send, receive, and manage emails."
 },
 {
  "name": "splitwise",
  "description": "A bill splitting app to track and split expenses with people."
 },
 {
  "name": "simple_note",
  "description": "A note-taking app to create and manage notes"
 },
 {
  "name": "todoist",
  "description": "A task management app to manage todo lists and collaborate on them with others."
 }
]
[
 {
  "name": "show_account",
  "description": "Show your account information. Unlike show_profile, this includes private information."
 },
 {
  "name": "signup",
  "description": "Sign up to create account."
 },
 {
  "name": "delete_account",
  "description": "Delete your account."
 },
 {
  "name": "update_account_name",
  "description": "Update your first or last name in the account profile."
 },
 {
  "name": "login",
  "description": "Login to your account."
 },
 {
  "name": "logout",
  "description": "Logout from your account."
 },
 {
  "name": "send_verification_code",
  "description": "Send account verification code to your email address."
 },
 {
  "name": "verify_account",
  "description": "Verify your account using the verification code sent to your email address."
 },
 {
  "name": "send_password_reset_code",
  "description": "Send password reset code to your email address."
 },
 {
  "name": "reset_password",
  "description": "Reset your password using the password reset code sent to your email address."
 },
 {
  "name": "show_profile",
  "description": "Show public profile information of a user."
 },
 {
  "name": "show_product",
  "description": "Show product information based on its ID."
 },
 {
  "name": "search_sellers",
  "description": "Search for sellers with a query."
 },
 {
  "name": "show_seller",
  "description": "Show a detailed information about the seller."
 },
 {
  "name": "search_product_types",
  "description": "Search product types present in the database."
 },
 {
  "name": "show_product_feature_choices",
  "description": "Show the choices of colors, relative sizes and sellers aggregated over all products of the given product type. Because it's an aggregation, the choices may not be available for all products. If product type is not passed, it will return the choices for all products in the database."
 },
 {
  "name": "search_products",
  "description": "Search for products with a query and various filtering criteria."
 },
 {
  "name": "show_cart",
  "description": "show your cart."
 },
 {
  "name": "clear_cart",
  "description": "Clear your cart."
 },
 {
  "name": "add_product_to_cart",
  "description": "Add product by id and quantities to your cart."
 },
 {
  "name": "delete_product_from_cart",
  "description": "Remove a product from your cart."
 },
 {
  "name": "update_product_quantity_in_cart",
  "description": "Update product quantity in the user cart."
 },
 {
  "name": "apply_promo_code_to_cart",
  "description": "Apply a promo code to your cart."
 },
 {
  "name": "remove_promo_code_from_cart",
  "description": "Remove a promo code from your cart."
 },
 {
  "name": "show_wish_list",
  "description": "Get list of products in your wishlist."
 },
 {
  "name": "clear_wish_list",
  "description": "Clear wish list."
 },
 {
  "name": "add_product_to_wish_list",
  "description": "Add product by id and quantities to your wish list."
 },
 {
  "name": "delete_product_from_wish_list",
  "description": "Remove product from the user wish list."
 },
 {
  "name": "update_product_quantity_in_wish_list",
  "description": "Update product quantity in the user wish_list."
 },
 {
  "name": "move_product_from_cart_to_wish_list",
  "description": "Move product from the cart to the wish list."
 },
 {
  "name": "move_product_from_wish_list_to_cart",
  "description": "Move product from the wish list to the cart."
 },
 {
  "name": "add_gift_wrapping_to_product",
  "description": "Add gift wrapping to a product in your cart. If the product is already set to be gift wrapped, its quantity will be updated."
 },
 {
  "name": "remove_gift_wrapping_from_product",
  "description": "Remove gift wrapping from a product in your cart."
 },
 {
  "name": "show_orders",
  "description": "Show or search your past orders"
 },
 {
  "name": "place_order",
  "description": "Place an order for all the items in your cart."
 },
 {
  "name": "show_order",
  "description": "Get details of a past order."
 },
 {
  "name": "download_order_receipt",
  "description": "Download the receipt of a past order."
 },
 {
  "name": "show_payment_cards",
  "description": "Get a list of your payment_cards."
 },
 {
  "name": "add_payment_card",
  "description": "Add a new payment card."
 },
 {
  "name": "show_payment_card",
  "description": "Get details of a payment card."
 },
 {
  "name": "delete_payment_card",
  "description": "Delete payment card information."
 },
 {
  "name": "update_payment_card",
  "description": "Update payment card information."
 },
 {
  "name": "show_addresses",
  "description": "Get a list of your addresses."
 },
 {
  "name": "add_address",
  "description": "Add a new address."
 },
 {
  "name": "delete_address",
  "description": "Delete address information."
 },
 {
  "name": "update_address",
  "description": "Update address information."
 },
 {
  "name": "show_product_reviews",
  "description": "Get a list of product reviews."
 },
 {
  "name": "write_product_review",
  "description": "Write a product review."
 },
 {
  "name": "delete_product_review",
  "description": "Delete a product review."
 },
 {
  "name": "update_product_review",
  "description": "Update a product review."
 },
 {
  "name": "show_product_questions",
  "description": "Get a list of product questions."
 },
 {
  "name": "write_product_question",
  "description": "Post a question about a product."
 },
 {
  "name": "show_product_question_answers",
  "description": "Get a list of answers to a product question."
 },
 {
  "name": "write_product_question_answer",
  "description": "Write a answer to a product question."
 },
 {
  "name": "delete_product_question",
  "description": "Delete a product question."
 },
 {
  "name": "update_product_question",
  "description": "Update a product question."
 },
 {
  "name": "delete_product_question_answer",
  "description": "Delete a answer to a product question."
 },
 {
  "name": "update_product_question_answer",
  "description": "Update answer to a product question."
 },
 {
  "name": "show_returns",
  "description": "Get a list of your product returns."
 },
 {
  "name": "initiate_return",
  "description": "Initiate a product return."
 },
 {
  "name": "show_return",
  "description": "Show product return status."
 },
 {
  "name": "show_return_deliverers",
  "description": "Get a list of product return deliverers."
 },
 {
  "name": "show_prime_plans",
  "description": "Show information about prime plans available. Delivery fee is waived for prime members."
 },
 {
  "name": "show_prime_subscriptions",
  "description": "Show your prime subscription history."
 },
 {
  "name": "subscribe_prime",
  "description": "Subscribe to prime membership."
 },
 {
  "name": "download_prime_subscription_receipt",
  "description": "Download the receipt for a prime subscription."
 }
]
[
 {
  "name": "show_account",
  "description": "Show your account information. Unlike show_profile, this includes private information."
 },
 {
  "name": "signup",
  "description": "Sign up to create account."
 },
 {
  "name": "delete_account",
  "description": "Delete your account."
 },
 {
  "name": "update_account_name",
  "description": "Update your first or last name in the account profile."
 },
 {
  "name": "login",
  "description": "Login to your account."
 },
 {
  "name": "logout",
  "description": "Logout from your account."
 },
 {
  "name": "send_password_reset_code",
  "description": "Send password reset code to your phone number."
 },
 {
  "name": "reset_password",
  "description": "Reset your password using the password reset code sent to your email address."
 },
 {
  "name": "show_profile",
  "description": "Show public profile information of a user."
 },
 {
  "name": "show_contact_relationships",
  "description": "Get a list of all relationships available in your contact book."
 },
 {
  "name": "search_contacts",
  "description": "Search your contact book for relatives' information."
 },
 {
  "name": "add_contact",
  "description": "Add a new contact."
 },
 {
  "name": "delete_contact",
  "description": "Delete contact information."
 },
 {
  "name": "update_contact",
  "description": "Update contact information."
 },
 {
  "name": "show_text_message_window",
  "description": "Show text messages with a contact around a given date and time."
 },
 {
  "name": "search_text_messages",
  "description": "Show or search your text messages."
 },
 {
  "name": "show_text_message",
  "description": "Show text message details."
 },
 {
  "name": "delete_text_message",
  "description": "Delete a text message."
 },
 {
  "name": "send_text_message",
  "description": "Send a text message on the given phone number."
 },
 {
  "name": "show_alarms",
  "description": "Get a list of alarms."
 },
 {
  "name": "create_alarm",
  "description": "Create a new alarm."
 },
 {
  "name": "show_alarm",
  "description": "Show alarm details."
 },
 {
  "name": "delete_alarm",
  "description": "Delete an alarm."
 },
 {
  "name": "update_alarm",
  "description": "Update an alarm's settings."
 },
 {
  "name": "show_voice_message_window",
  "description": "Show voice messages with a contact around a given date and time."
 },
 {
  "name": "search_voice_messages",
  "description": "Show or search text voice_messages between the user and a contact."
 },
 {
  "name": "show_voice_message",
  "description": "Show voice message details."
 },
 {
  "name": "delete_voice_message",
  "description": "Delete a voice message."
 },
 {
  "name": "send_voice_message",
  "description": "Send a voice message on the given phone number."
 },
 {
  "name": "get_current_date_and_time",
  "description": "Show current date and time."
 }
]
```


### Environment Interaction 5
----------------------------------------------------------------------------
```python
# Get the access token for the main user's Amazon account
print(apis.supervisor.show_account_passwords())

# Get the access token for the main user's phone
print(apis.supervisor.show_account_passwords())

# Search for the partner's phone number in the main user's contact book
print(apis.phone.api_docs.show_api_doc('search_contacts'))

# Get the main user's Amazon wish list
print(apis.amazon.api_docs.show_api_descriptions())
```

```
Execution failed. Traceback:
  File "<python-input>", line 8, in <module>
    print(apis.phone.api_docs.show_api_doc('search_contacts'))
          ^^^^^^^^^^^^^^^^^^^
Exception: No API named 'api_docs' found in the phone app.
```


### Environment Interaction 6
----------------------------------------------------------------------------
```python
# Get the API description for the search_contacts API in the phone app
print(apis.api_docs.show_api_doc(app_name='phone', api_name='search_contacts'))

# Get the API descriptions for the amazon app
print(apis.api_docs.show_api_descriptions(app_name='amazon'))
```

```
{
 "app_name": "phone",
 "api_name": "search_contacts",
 "path": "/contacts",
 "method": "GET",
 "description": "Search your contact book for relatives' information.",
 "parameters": [
  {
   "name": "access_token",
   "type": "string",
   "required": true,
   "description": "Access token obtained from phone app login.",
   "default": null,
   "constraints": []
  },
  {
   "name": "query",
   "type": "string",
   "required": false,
   "description": "Search query for the contacts list.",
   "default": "",
   "constraints": []
  },
  {
   "name": "relationship",
   "type": "string",
   "required": false,
   "description": "Relationship with the person in the contacts list to filter by.",
   "default": null,
   "constraints": []
  },
  {
   "name": "page_index",
   "type": "integer",
   "required": false,
   "description": "The index of the page to return.",
   "default": 0,
   "constraints": [
    "value >= 0.0"
   ]
  },
  {
   "name": "page_limit",
   "type": "integer",
   "required": false,
   "description": "The maximum number of results to return per page.",
   "default": 5,
   "constraints": [
    "value >= 1.0, <= 20.0"
   ]
  }
 ],
 "response_schemas": {
  "success": [
   {
    "contact_id": 1,
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "phone_number": "string",
    "relationships": [
     "string"
    ],
    "birthday": "string",
    "home_address": "string",
    "work_address": "string",
    "created_at": "2019-01-01T00:00:00"
   }
  ],
  "failure": {
   "message": "string"
  }
 }
}
[
 {
  "name": "show_account",
  "description": "Show your account information. Unlike show_profile, this includes private information."
 },
 {
  "name": "signup",
  "description": "Sign up to create account."
 },
 {
  "name": "delete_account",
  "description": "Delete your account."
 },
 {
  "name": "update_account_name",
  "description": "Update your first or last name in the account profile."
 },
 {
  "name": "login",
  "description": "Login to your account."
 },
 {
  "name": "logout",
  "description": "Logout from your account."
 },
 {
  "name": "send_verification_code",
  "description": "Send account verification code to your email address."
 },
 {
  "name": "verify_account",
  "description": "Verify your account using the verification code sent to your email address."
 },
 {
  "name": "send_password_reset_code",
  "description": "Send password reset code to your email address."
 },
 {
  "name": "reset_password",
  "description": "Reset your password using the password reset code sent to your email address."
 },
 {
  "name": "show_profile",
  "description": "Show public profile information of a user."
 },
 {
  "name": "show_product",
  "description": "Show product information based on its ID."
 },
 {
  "name": "search_sellers",
  "description": "Search for sellers with a query."
 },
 {
  "name": "show_seller",
  "description": "Show a detailed information about the seller."
 },
 {
  "name": "search_product_types",
  "description": "Search product types present in the database."
 },
 {
  "name": "show_product_feature_choices",
  "description": "Show the choices of colors, relative sizes and sellers aggregated over all products of the given product type. Because it's an aggregation, the choices may not be available for all products. If product type is not passed, it will return the choices for all products in the database."
 },
 {
  "name": "search_products",
  "description": "Search for products with a query and various filtering criteria."
 },
 {
  "name": "show_cart",
  "description": "show your cart."
 },
 {
  "name": "clear_cart",
  "description": "Clear your cart."
 },
 {
  "name": "add_product_to_cart",
  "description": "Add product by id and quantities to your cart."
 },
 {
  "name": "delete_product_from_cart",
  "description": "Remove a product from your cart."
 },
 {
  "name": "update_product_quantity_in_cart",
  "description": "Update product quantity in the user cart."
 },
 {
  "name": "apply_promo_code_to_cart",
  "description": "Apply a promo code to your cart."
 },
 {
  "name": "remove_promo_code_from_cart",
  "description": "Remove a promo code from your cart."
 },
 {
  "name": "show_wish_list",
  "description": "Get list of products in your wishlist."
 },
 {
  "name": "clear_wish_list",
  "description": "Clear wish list."
 },
 {
  "name": "add_product_to_wish_list",
  "description": "Add product by id and quantities to your wish list."
 },
 {
  "name": "delete_product_from_wish_list",
  "description": "Remove product from the user wish list."
 },
 {
  "name": "update_product_quantity_in_wish_list",
  "description": "Update product quantity in the user wish_list."
 },
 {
  "name": "move_product_from_cart_to_wish_list",
  "description": "Move product from the cart to the wish list."
 },
 {
  "name": "move_product_from_wish_list_to_cart",
  "description": "Move product from the wish list to the cart."
 },
 {
  "name": "add_gift_wrapping_to_product",
  "description": "Add gift wrapping to a product in your cart. If the product is already set to be gift wrapped, its quantity will be updated."
 },
 {
  "name": "remove_gift_wrapping_from_product",
  "description": "Remove gift wrapping from a product in your cart."
 },
 {
  "name": "show_orders",
  "description": "Show or search your past orders"
 },
 {
  "name": "place_order",
  "description": "Place an order for all the items in your cart."
 },
 {
  "name": "show_order",
  "description": "Get details of a past order."
 },
 {
  "name": "download_order_receipt",
  "description": "Download the receipt of a past order."
 },
 {
  "name": "show_payment_cards",
  "description": "Get a list of your payment_cards."
 },
 {
  "name": "add_payment_card",
  "description": "Add a new payment card."
 },
 {
  "name": "show_payment_card",
  "description": "Get details of a payment card."
 },
 {
  "name": "delete_payment_card",
  "description": "Delete payment card information."
 },
 {
  "name": "update_payment_card",
  "description": "Update payment card information."
 },
 {
  "name": "show_addresses",
  "description": "Get a list of your addresses."
 },
 {
  "name": "add_address",
  "description": "Add a new address."
 },
 {
  "name": "delete_address",
  "description": "Delete address information."
 },
 {
  "name": "update_address",
  "description": "Update address information."
 },
 {
  "name": "show_product_reviews",
  "description": "Get a list of product reviews."
 },
 {
  "name": "write_product_review",
  "description": "Write a product review."
 },
 {
  "name": "delete_product_review",
  "description": "Delete a product review."
 },
 {
  "name": "update_product_review",
  "description": "Update a product review."
 },
 {
  "name": "show_product_questions",
  "description": "Get a list of product questions."
 },
 {
  "name": "write_product_question",
  "description": "Post a question about a product."
 },
 {
  "name": "show_product_question_answers",
  "description": "Get a list of answers to a product question."
 },
 {
  "name": "write_product_question_answer",
  "description": "Write a answer to a product question."
 },
 {
  "name": "delete_product_question",
  "description": "Delete a product question."
 },
 {
  "name": "update_product_question",
  "description": "Update a product question."
 },
 {
  "name": "delete_product_question_answer",
  "description": "Delete a answer to a product question."
 },
 {
  "name": "update_product_question_answer",
  "description": "Update answer to a product question."
 },
 {
  "name": "show_returns",
  "description": "Get a list of your product returns."
 },
 {
  "name": "initiate_return",
  "description": "Initiate a product return."
 },
 {
  "name": "show_return",
  "description": "Show product return status."
 },
 {
  "name": "show_return_deliverers",
  "description": "Get a list of product return deliverers."
 },
 {
  "name": "show_prime_plans",
  "description": "Show information about prime plans available. Delivery fee is waived for prime members."
 },
 {
  "name": "show_prime_subscriptions",
  "description": "Show your prime subscription history."
 },
 {
  "name": "subscribe_prime",
  "description": "Subscribe to prime membership."
 },
 {
  "name": "download_prime_subscription_receipt",
  "description": "Download the receipt for a prime subscription."
 }
]
```


### Environment Interaction 7
----------------------------------------------------------------------------
```python
# Get the access token for the main user's phone
print(apis.supervisor.show_account_passwords())

# Get the access token for the main user's Amazon account
print(apis.supervisor.show_account_passwords())

# Search for the partner's phone number in the main user's contact book
phone_access_token = apis.phone.login(username="brenda.webe@gmail.com", password=apis.supervisor.show_account_passwords()[0]['password'])
partner_contacts = apis.phone.search_contacts(access_token=phone_access_token, query="partner", relationship="partner")

# Get the partner's phone number
partner_phone_number = partner_contacts[0].phone_number

# Get the main user's Amazon wish list
amazon_access_token = apis.amazon.login(username="brenda.webe@gmail.com", password=apis.supervisor.show_account_passwords()[1]['password'])
wish_list = apis.amazon.show_wish_list(access_token=amazon_access_token)

# Print the wish list
print(wish_list)
```

```
Execution failed. Traceback:
  File "<python-input>", line 8, in <module>
    phone_access_token = apis.phone.login(username="brenda.webe@gmail.com", password=apis.supervisor.show_account_passwords()[0]['password'])
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: Response status code is 401:
{"message":"Invalid credentials"}
```


### Environment Interaction 8
----------------------------------------------------------------------------
```python
# Get the account passwords for the main user
print(apis.supervisor.show_account_passwords())

# Get the API description for the login API in the phone app
print(apis.api_docs.show_api_doc(app_name='phone', api_name='login'))

# Get the API description for the login API in the amazon app
print(apis.api_docs.show_api_doc(app_name='amazon', api_name='login'))
```

```
[
 {
  "account_name": "amazon",
  "password": "{(u%}@f"
 },
 {
  "account_name": "file_system",
  "password": "$0a_HKP"
 },
 {
  "account_name": "gmail",
  "password": "p5%#xC5"
 },
 {
  "account_name": "phone",
  "password": "N^ssqde"
 },
 {
  "account_name": "simple_note",
  "password": "nwrDB{O"
 },
 {
  "account_name": "splitwise",
  "password": "mD5-IE2"
 },
 {
  "account_name": "spotify",
  "password": "MPzz6^n"
 },
 {
  "account_name": "todoist",
  "password": "ItI_3PU"
 },
 {
  "account_name": "venmo",
  "password": "$LRYdG7"
 }
]
{
 "app_name": "phone",
 "api_name": "login",
 "path": "/auth/token",
 "method": "POST",
 "description": "Login to your account.",
 "parameters": [
  {
   "name": "username",
   "type": "string",
   "required": true,
   "description": "Your account phone_number.",
   "default": null,
   "constraints": []
  },
  {
   "name": "password",
   "type": "string",
   "required": true,
   "description": "Your account password.",
   "default": null,
   "constraints": []
  }
 ],
 "response_schemas": {
  "success": {
   "access_token": "string",
   "token_type": "string"
  },
  "failure": {
   "message": "string"
  }
 }
}
{
 "app_name": "amazon",
 "api_name": "login",
 "path": "/auth/token",
 "method": "POST",
 "description": "Login to your account.",
 "parameters": [
  {
   "name": "username",
   "type": "string",
   "required": true,
   "description": "Your account email.",
   "default": null,
   "constraints": []
  },
  {
   "name": "password",
   "type": "string",
   "required": true,
   "description": "Your account password.",
   "default": null,
   "constraints": []
  }
 ],
 "response_schemas": {
  "success": {
   "access_token": "string",
   "token_type": "string"
  },
  "failure": {
   "message": "string"
  }
 }
}
```


### Environment Interaction 9
----------------------------------------------------------------------------
```python
# Get the access token for the main user's phone
phone_access_token = apis.phone.login(username="9312015677", password="N^ssqde")

# Get the access token for the main user's Amazon account
amazon_access_token = apis.amazon.login(username="brenda.webe@gmail.com", password="{(u%}@f")

# Search for the partner's phone number in the main user's contact book
partner_contacts = apis.phone.search_contacts(access_token=phone_access_token, query="partner", relationship="partner")

# Get the partner's phone number
partner_phone_number = partner_contacts[0].phone_number

# Get the main user's Amazon wish list
wish_list = apis.amazon.show_wish_list(access_token=amazon_access_token)

# Print the wish list
print(wish_list)
```

```
Execution failed. Traceback:
  File "<python-input>", line 8, in <module>
    partner_contacts = apis.phone.search_contacts(access_token=phone_access_token, query="partner", relationship="partner")
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: Response status code is 401:
{"message":"You are either not authorized to access this phone API endpoint or your access token is missing, invalid or expired."}
```


### Environment Interaction 10
----------------------------------------------------------------------------
```python
# Get the access token for the main user's phone
phone_login_response = apis.phone.login(username="9312015677", password="N^ssqde")
phone_access_token = phone_login_response['access_token']

# Get the access token for the main user's Amazon account
amazon_login_response = apis.amazon.login(username="brenda.webe@gmail.com", password="{(u%}@f")
amazon_access_token = amazon_login_response['access_token']

# Search for the partner's phone number in the main user's contact book
partner_contacts = apis.phone.search_contacts(access_token=phone_access_token, query="partner", relationship="partner")

# Get the partner's phone number
partner_phone_number = partner_contacts[0].phone_number

# Get the main user's Amazon wish list
wish_list = apis.amazon.show_wish_list(access_token=amazon_access_token)

# Print the wish list
print(wish_list)
```

```
Execution failed. Traceback:
  File "<python-input>", line 13, in <module>
    partner_phone_number = partner_contacts[0].phone_number
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'dict' object has no attribute 'phone_number'
```


### Environment Interaction 11
----------------------------------------------------------------------------
```python
# Get the access token for the main user's phone
phone_login_response = apis.phone.login(username="9312015677", password="N^ssqde")
phone_access_token = phone_login_response['access_token']

# Get the access token for the main user's Amazon account
amazon_login_response = apis.amazon.login(username="brenda.webe@gmail.com", password="{(u%}@f")
amazon_access_token = amazon_login_response['access_token']

# Search for the partner's phone number in the main user's contact book
partner_contacts = apis.phone.search_contacts(access_token=phone_access_token, query="partner", relationship="partner")

# Get the partner's phone number
partner_phone_number = partner_contacts[0]['phone_number']

# Get the main user's Amazon wish list
wish_list = apis.amazon.show_wish_list(access_token=amazon_access_token)

# Print the wish list
print(wish_list)
```

```
[
 {
  "product_id": 55,
  "product_name": "3M Scotch 8-in Cable Ties",
  "quantity": 2,
  "price": 2.5
 },
 {
  "product_id": 387,
  "product_name": "Sawyer Products Mini Water Filtration System",
  "quantity": 1,
  "price": 24.9
 },
 {
  "product_id": 597,
  "product_name": "Hamilton Beach 8-Cup Compact Food Processor",
  "quantity": 1,
  "price": 30.0
 },
 {
  "product_id": 1651,
  "product_name": "Craftsman 8-Inch Arc Joint Pliers",
  "quantity": 1,
  "price": 9.0
 },
 {
  "product_id": 1688,
  "product_name": "Husky Adjustable Height Work Table",
  "quantity": 1,
  "price": 199.0
 },
 {
  "product_id": 2100,
  "product_name": "Ascend Trekking Poles",
  "quantity": 1,
  "price": 30.0
 },
 {
  "product_id": 2218,
  "product_name": "OXO Good Grips\u00ae Stainless Steel Soap Dispenser",
  "quantity": 1,
  "price": 20.0
 }
]
```


### Environment Interaction 12
----------------------------------------------------------------------------
```python
# Get the access token for the main user's phone
phone_login_response = apis.phone.login(username="9312015677", password="N^ssqde")
phone_access_token = phone_login_response['access_token']

# Get the access token for the main user's Amazon account
amazon_login_response = apis.amazon.login(username="brenda.webe@gmail.com", password="{(u%}@f")
amazon_access_token = amazon_login_response['access_token']

# Search for the partner's phone number in the main user's contact book
partner_contacts = apis.phone.search_contacts(access_token=phone_access_token, query="partner", relationship="partner")

# Get the partner's phone number
partner_phone_number = partner_contacts[0]['phone_number']

# Get the main user's Amazon wish list
wish_list = apis.amazon.show_wish_list(access_token=amazon_access_token)

# Create an itemized list of the wish list
itemized_list = []
for product in wish_list:
    total_price = round(product['price'] * product['quantity'])
    itemized_list.append(f"{product['product_name']} => ${total_price}")

# Send the itemized list to the partner via a phone text
message = "\n".join(itemized_list)
apis.phone.send_text_message(access_token=phone_access_token, phone_number=partner_phone_number, message=message)
```

```
Execution successful.
```


### Environment Interaction 13
----------------------------------------------------------------------------
```python
print("Task completed successfully")
```

```
Task completed successfully
```


### Environment Interaction 14
----------------------------------------------------------------------------
```python
apis.supervisor.complete_task(answer=None, status="success")
```

```
Execution successful.
```


### Environment Interaction 15
----------------------------------------------------------------------------
```python
# Get the access token for the main user's phone
phone_login_response = apis.phone.login(username="9312015677", password="N^ssqde")
phone_access_token = phone_login_response['access_token']

# Get the access token for the main user's Amazon account
amazon_login_response = apis.amazon.login(username="brenda.webe@gmail.com", password="{(u%}@f")
amazon_access_token = amazon_login_response['access_token']

# Search for the partner's phone number in the main user's contact book
partner_contacts = apis.phone.search_contacts(access_token=phone_access_token, query="partner", relationship="partner")

# Get the partner's phone number
partner_phone_number = partner_contacts[0]['phone_number']

# Get the main user's Amazon wish list
wish_list = apis.amazon.show_wish_list(access_token=amazon_access_token)

# Create an itemized list of the wish list
itemized_list = []
for product in wish_list:
    total_price = round(product['price'] * product['quantity'])
    itemized_list.append(f"{product['product_name']} => ${total_price}")

# Send the itemized list to the partner via a phone text
message = "\n".join(itemized_list)
print(message)

# Verify the message was sent correctly
sent_messages = apis.phone.search_text_messages(access_token=phone_access_token, phone_number=partner_phone_number)
for message in sent_messages:
    if message['message'] == "\n".join(itemized_list):
        print("Message sent correctly")
        break
else:
    print("Message not sent correctly")

# Check if only the required changes were made
print(apis.phone.show_text_message_window(access_token=phone_access_token, phone_number=partner_phone_number))

print("DONE_VERIFIED")
```

```
3M Scotch 8-in Cable Ties => $5
Sawyer Products Mini Water Filtration System => $25
Hamilton Beach 8-Cup Compact Food Processor => $30
Craftsman 8-Inch Arc Joint Pliers => $9
Husky Adjustable Height Work Table => $199
Ascend Trekking Poles => $30
OXO Good Grips® Stainless Steel Soap Dispenser => $20
Message sent correctly
[
 {
  "text_message_id": 10305,
  "sender": {
   "contact_id": null,
   "name": "Brenda Smith",
   "phone_number": "9312015677"
  },
  "receiver": {
   "contact_id": 1007,
   "name": "Marcus Smith",
   "phone_number": "7196131136"
  },
  "message": "Sure thing!",
  "sent_at": "2023-05-17T14:32:39"
 },
 {
  "text_message_id": 16794,
  "sender": {
   "contact_id": 1007,
   "name": "Marcus Smith",
   "phone_number": "7196131136"
  },
  "receiver": {
   "contact_id": null,
   "name": "Brenda Smith",
   "phone_number": "9312015677"
  },
  "message": "Can you send me your amazon wish list?",
  "sent_at": "2023-05-18T09:32:57"
 },
 {
  "text_message_id": 16796,
  "sender": {
   "contact_id": 1007,
   "name": "Marcus Smith",
   "phone_number": "7196131136"
  },
  "receiver": {
   "contact_id": null,
   "name": "Brenda Smith",
   "phone_number": "9312015677"
  },
  "message": "I will be late for dinner tonight. Please don't wait for me.",
  "sent_at": "2023-05-18T09:39:40"
 },
 {
  "text_message_id": 16798,
  "sender": {
   "contact_id": 1007,
   "name": "Marcus Smith",
   "phone_number": "7196131136"
  },
  "receiver": {
   "contact_id": null,
   "name": "Brenda Smith",
   "phone_number": "9312015677"
  },
  "message": "Sounds good.",
  "sent_at": "2023-05-18T09:46:20"
 },
 {
  "text_message_id": 16799,
  "sender": {
   "contact_id": null,
   "name": "Brenda Smith",
   "phone_number": "9312015677"
  },
  "receiver": {
   "contact_id": 1007,
   "name": "Marcus Smith",
   "phone_number": "7196131136"
  },
  "message": "3M Scotch 8-in Cable Ties => $5\nSawyer Products Mini Water Filtration System => $25\nHamilton Beach 8-Cup Compact Food Processor => $30\nCraftsman 8-Inch Arc Joint Pliers => $9\nHusky Adjustable Height Work Table => $199\nAscend Trekking Poles => $30\nOXO Good Grips\u00ae Stainless Steel Soap Dispenser => $20",
  "sent_at": "2023-05-18T12:00:00"
 }
]
DONE_VERIFIED
```

