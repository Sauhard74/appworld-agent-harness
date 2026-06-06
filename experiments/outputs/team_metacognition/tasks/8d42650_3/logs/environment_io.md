
### Environment Interaction 1
----------------------------------------------------------------------------
```python
from appworld.common.datetime import DateTime
from appworld.common.utils import find_all_from_pages, find_one

# Get the current year
current_year = DateTime.now().year

# Get the access token for the main user's email account
email_access_token = apis.email.access_token_from(apis.supervisor.main_user)

# Search for emails with the subject "Cable Bill" and sent on the 1st of every month
cable_bills = find_all_from_pages(
    apis.email.search_emails,
    access_token=email_access_token,
    subject="Cable Bill",
    sent_date=f"{current_year}-01-01",
)

# Print the cable bills to inspect
print(cable_bills)
```

```
Execution failed. Traceback:
  File "<python-input>", line 8, in <module>
    email_access_token = apis.email.access_token_from(apis.supervisor.main_user)
                         ^^^^^^^^^^
Exception: No app named 'email' found.
```


### Environment Interaction 2
----------------------------------------------------------------------------
```python
print(apis.api_docs.show_app_descriptions())
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
```


### Environment Interaction 3
----------------------------------------------------------------------------
```python
# Get the access token for the main user's gmail account
gmail_access_token = apis.gmail.access_token_from(apis.supervisor.main_user)

# Search for emails with the subject "Cable Bill" and sent on the 1st of every month
print(apis.gmail.search_emails(access_token=gmail_access_token, subject="Cable Bill"))
```

```
Execution failed. Traceback:
  File "<python-input>", line 2, in <module>
    gmail_access_token = apis.gmail.access_token_from(apis.supervisor.main_user)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'access_token_from' found in the gmail app.
```


### Environment Interaction 4
----------------------------------------------------------------------------
```python
print(apis.api_docs.show_api_descriptions(app_name='gmail'))
```

```
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
  "name": "search_users",
  "description": "Search Gmail users by name or email address."
 },
 {
  "name": "show_inbox_threads",
  "description": "Show or search email threads you have received. This will not show detailed information about emails within the thread."
 },
 {
  "name": "show_outbox_threads",
  "description": "Show or search email threads you have sent. This will not show detailed information about emails within the thread."
 },
 {
  "name": "show_archived_threads",
  "description": "Show or search email threads you have archived. This will not show detailed information about emails within the thread."
 },
 {
  "name": "show_spam_threads",
  "description": "Show or search email threads that have been marked as spam. This will not show detailed information about emails within the thread."
 },
 {
  "name": "show_category_sizes",
  "description": "Show the number of email threads in each category of inbox, outbox, archived, spam, and the number of unscheduled and scheduled email drafts."
 },
 {
  "name": "show_thread",
  "description": "Show detailed information about a given email thread, including emails and drafts within it."
 },
 {
  "name": "delete_thread",
  "description": "Delete an email thread."
 },
 {
  "name": "show_email",
  "description": "Show detailed information about a given email."
 },
 {
  "name": "label_thread",
  "description": "Label an email thread."
 },
 {
  "name": "unlabel_thread",
  "description": "Remove label from an email thread."
 },
 {
  "name": "mark_thread_read",
  "description": "Mark an email thread as read."
 },
 {
  "name": "mark_thread_unread",
  "description": "Mark an email thread as unread."
 },
 {
  "name": "mark_thread_archived",
  "description": "Mark an email thread as archived."
 },
 {
  "name": "mark_thread_unarchived",
  "description": "Mark an email thread as unarchived."
 },
 {
  "name": "mark_thread_spam",
  "description": "Mark an email thread as spam."
 },
 {
  "name": "mark_thread_not_spam",
  "description": "Mark an email thread as not spam."
 },
 {
  "name": "mark_thread_starred",
  "description": "Mark an email thread as starred."
 },
 {
  "name": "mark_thread_unstarred",
  "description": "Mark an email thread as unstarred."
 },
 {
  "name": "delete_email_in_thread",
  "description": "Delete an email in a thread."
 },
 {
  "name": "send_email",
  "description": "Send a new email to one or more recipients."
 },
 {
  "name": "reply_to_email",
  "description": "Reply to an existing email in a thread."
 },
 {
  "name": "forward_email_from_thread",
  "description": "Forward an email from an email thread to one or more recipients."
 },
 {
  "name": "forward_email_thread",
  "description": "Forward entire email thread to one or more recipients."
 },
 {
  "name": "show_drafts",
  "description": "Show a list of user drafts."
 },
 {
  "name": "create_draft",
  "description": "Create a new draft."
 },
 {
  "name": "show_draft",
  "description": "Show detailed draft information."
 },
 {
  "name": "delete_draft",
  "description": "Delete draft information."
 },
 {
  "name": "update_draft",
  "description": "Update draft information."
 },
 {
  "name": "send_email_from_draft",
  "description": "Send a new email from a draft right away."
 },
 {
  "name": "download_attachment",
  "description": "Download a file attachment."
 },
 {
  "name": "upload_attachments_to_draft",
  "description": "Upload attachments to a draft."
 },
 {
  "name": "remove_attachment_from_draft",
  "description": "Delete an attachment from a draft."
 }
]
```


### Environment Interaction 5
----------------------------------------------------------------------------
```python
print(apis.api_docs.show_api_doc(app_name='gmail', api_name='login'))
```

```
{
 "app_name": "gmail",
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


### Environment Interaction 6
----------------------------------------------------------------------------
```python
print(apis.supervisor.show_account_passwords())
```

```
[
 {
  "account_name": "amazon",
  "password": "oIhoOb9"
 },
 {
  "account_name": "file_system",
  "password": "4k9jcny"
 },
 {
  "account_name": "gmail",
  "password": "#x}}5n5"
 },
 {
  "account_name": "phone",
  "password": "X53y6aW"
 },
 {
  "account_name": "simple_note",
  "password": "eizVxAh"
 },
 {
  "account_name": "splitwise",
  "password": "F{Q8_pw"
 },
 {
  "account_name": "spotify",
  "password": "3a-m^o6"
 },
 {
  "account_name": "todoist",
  "password": "+&R$o4K"
 },
 {
  "account_name": "venmo",
  "password": "rl2A-Xl"
 }
]
```


### Environment Interaction 7
----------------------------------------------------------------------------
```python
gmail_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'gmail'), None)
if gmail_credentials:
    email = apis.supervisor.main_user.email
    password = gmail_credentials['password']
    response = apis.gmail.login(username=email, password=password)
    if 'access_token' in response:
        gmail_access_token = response['access_token']
        print(gmail_access_token)
    else:
        print("Failed to login to Gmail")
else:
    print("Gmail credentials not found")
```

```
Execution failed. Traceback:
  File "<python-input>", line 3, in <module>
    email = apis.supervisor.main_user.email
            ^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'main_user' found in the supervisor app.
```


### Environment Interaction 8
----------------------------------------------------------------------------
```python
gmail_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'gmail'), None)
if gmail_credentials:
    email = apis.supervisor.email
    password = gmail_credentials['password']
    response = apis.gmail.login(username=email, password=password)
    if 'access_token' in response:
        gmail_access_token = response['access_token']
        print(gmail_access_token)
    else:
        print("Failed to login to Gmail")
else:
    print("Gmail credentials not found")
```

```
Execution failed. Traceback:
  File "<python-input>", line 3, in <module>
    email = apis.supervisor.email
            ^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'email' found in the supervisor app.
```


### Environment Interaction 9
----------------------------------------------------------------------------
```python
gmail_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'gmail'), None)
if gmail_credentials:
    email = apis.supervisor.MainUserMunch.email
    password = gmail_credentials['password']
    response = apis.gmail.login(username=email, password=password)
    if 'access_token' in response:
        gmail_access_token = response['access_token']
        print(gmail_access_token)
    else:
        print("Failed to login to Gmail")
else:
    print("Gmail credentials not found")
```

```
Execution failed. Traceback:
  File "<python-input>", line 3, in <module>
    email = apis.supervisor.MainUserMunch.email
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'MainUserMunch' found in the supervisor app.
```


### Environment Interaction 10
----------------------------------------------------------------------------
```python
gmail_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'gmail'), None)
if gmail_credentials:
    email = apis.supervisor.MainUserMunch['email']
    password = gmail_credentials['password']
    response = apis.gmail.login(username=email, password=password)
    if 'access_token' in response:
        gmail_access_token = response['access_token']
        print(gmail_access_token)
    else:
        print("Failed to login to Gmail")
else:
    print("Gmail credentials not found")
```

```
Execution failed. Traceback:
  File "<python-input>", line 3, in <module>
    email = apis.supervisor.MainUserMunch['email']
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'MainUserMunch' found in the supervisor app.
```


### Environment Interaction 11
----------------------------------------------------------------------------
```python
gmail_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'gmail'), None)
if gmail_credentials:
    email = apis.supervisor.email
    password = gmail_credentials['password']
    response = apis.gmail.login(username=email, password=password)
    if 'access_token' in response:
        gmail_access_token = response['access_token']
        print(gmail_access_token)
    else:
        print("Failed to login to Gmail")
else:
    print("Gmail credentials not found")
```

```
Execution failed. Traceback:
  File "<python-input>", line 3, in <module>
    email = apis.supervisor.email
            ^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'email' found in the supervisor app.
```


### Environment Interaction 12
----------------------------------------------------------------------------
```python
print(apis.supervisor.MainUserMunch)
```

```
Execution failed. Traceback:
  File "<python-input>", line 1, in <module>
    print(apis.supervisor.MainUserMunch)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'MainUserMunch' found in the supervisor app.
```


### Environment Interaction 13
----------------------------------------------------------------------------
```python
main_user = apis.supervisor.MainUserMunch({'first_name': 'Carl', 'last_name': 'Brown', 'email': 'carbrown@gmail.com', 'phone_number': '7934818191'})
gmail_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'gmail'), None)
if gmail_credentials:
    email = main_user['email']
    password = gmail_credentials['password']
    response = apis.gmail.login(username=email, password=password)
    if 'access_token' in response:
        gmail_access_token = response['access_token']
        print(gmail_access_token)
    else:
        print("Failed to login to Gmail")
else:
    print("Gmail credentials not found")
```

```
Execution failed. Traceback:
  File "<python-input>", line 1, in <module>
    main_user = apis.supervisor.MainUserMunch({'first_name': 'Carl', 'last_name': 'Brown', 'email': 'carbrown@gmail.com', 'phone_number': '7934818191'})
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'MainUserMunch' found in the supervisor app.
```


### Environment Interaction 14
----------------------------------------------------------------------------
```python
main_user = {'first_name': 'Carl', 'last_name': 'Brown', 'email': 'carbrown@gmail.com', 'phone_number': '7934818191'}
gmail_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'gmail'), None)
if gmail_credentials:
    email = main_user['email']
    password = gmail_credentials['password']
    response = apis.gmail.login(username=email, password=password)
    if 'access_token' in response:
        gmail_access_token = response['access_token']
        print(gmail_access_token)
    else:
        print("Failed to login to Gmail")
else:
    print("Gmail credentials not found")
```

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbWFpbCtjYXJicm93bkBnbWFpbC5jb20iLCJleHAiOjE2ODk2ODI0OTh9.Z3ojsBN5_Q4H4baXgCxEaj6vNNHfr5_M_MlgdH1Saz8
```


### Environment Interaction 15
----------------------------------------------------------------------------
```python
gmail_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbWFpbCtjYXJicm93bkBnbWFpbC5jb20iLCJleHAiOjE2ODk2ODI0OTh9.Z3ojsBN5_Q4H4baXgCxEaj6vNNHfr5_M_MlgdH1Saz8"
print(apis.gmail.show_inbox_threads(access_token=gmail_access_token, subject="Cable Bill"))
```

```
[
 {
  "email_thread_id": 47821,
  "email_ids": [
   20867
  ],
  "draft_ids": [],
  "incoming": true,
  "outgoing": false,
  "read": false,
  "label": null,
  "starred": false,
  "archived": false,
  "spam": false,
  "created_at": "2023-07-01T10:49:29",
  "updated_at": "2023-07-01T10:49:29",
  "subject": "Electricity Bill for 2023-06-01 - 2023-06-30",
  "participants": [
   {
    "name": "Carl Brown",
    "email": "carbrown@gmail.com"
   },
   {
    "name": "Electrasource Notifications",
    "email": "notifications@electrasource.com"
   }
  ]
 },
 {
  "email_thread_id": 47823,
  "email_ids": [
   20868
  ],
  "draft_ids": [],
  "incoming": true,
  "outgoing": false,
  "read": false,
  "label": null,
  "starred": false,
  "archived": false,
  "spam": false,
  "created_at": "2023-07-01T10:49:29",
  "updated_at": "2023-07-01T10:49:29",
  "subject": "Internet Bill for June 2023",
  "participants": [
   {
    "name": "Carl Brown",
    "email": "carbrown@gmail.com"
   },
   {
    "name": "Netboost Notifications",
    "email": "notifications@netboost.com"
   }
  ]
 },
 {
  "email_thread_id": 47825,
  "email_ids": [
   20869
  ],
  "draft_ids": [],
  "incoming": true,
  "outgoing": false,
  "read": false,
  "label": null,
  "starred": false,
  "archived": false,
  "spam": false,
  "created_at": "2023-07-01T10:49:29",
  "updated_at": "2023-07-01T10:49:29",
  "subject": "Cable Bill for June 2023",
  "participants": [
   {
    "name": "Carl Brown",
    "email": "carbrown@gmail.com"
   },
   {
    "name": "Thundercable Notifications",
    "email": "notifications@thundercable.com"
   }
  ]
 },
 {
  "email_thread_id": 47827,
  "email_ids": [
   20870
  ],
  "draft_ids": [],
  "incoming": true,
  "outgoing": false,
  "read": false,
  "label": null,
  "starred": false,
  "archived": false,
  "spam": false,
  "created_at": "2023-06-01T14:42:52",
  "updated_at": "2023-06-01T14:42:52",
  "subject": "Electricity Bill for 2023-05-01 - 2023-05-31",
  "participants": [
   {
    "name": "Carl Brown",
    "email": "carbrown@gmail.com"
   },
   {
    "name": "Electrasource Notifications",
    "email": "notifications@electrasource.com"
   }
  ]
 },
 {
  "email_thread_id": 47829,
  "email_ids": [
   20871
  ],
  "draft_ids": [],
  "incoming": true,
  "outgoing": false,
  "read": false,
  "label": null,
  "starred": false,
  "archived": false,
  "spam": false,
  "created_at": "2023-06-01T14:42:52",
  "updated_at": "2023-06-01T14:42:52",
  "subject": "Internet Bill for May 2023",
  "participants": [
   {
    "name": "Carl Brown",
    "email": "carbrown@gmail.com"
   },
   {
    "name": "Netboost Notifications",
    "email": "notifications@netboost.com"
   }
  ]
 }
]
```


### Environment Interaction 16
----------------------------------------------------------------------------
```python
gmail_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbWFpbCtjYXJicm93bkBnbWFpbC5jb20iLCJleHAiOjE2ODk2ODI0OTh9.Z3ojsBN5_Q4H4baXgCxEaj6vNNHfr5_M_MlgdH1Saz8"
email_threads = apis.gmail.show_inbox_threads(access_token=gmail_access_token, subject="Cable Bill")
cable_bills = [thread for thread in email_threads if 'Cable Bill for' in thread['subject']]
for bill in cable_bills:
    email_id = bill['email_ids'][0]
    print(apis.gmail.show_email(access_token=gmail_access_token, email_id=email_id))
```

```
{
 "email_id": 20869,
 "subject": "Cable Bill for June 2023",
 "body": "Please find attached the cable bill for June 2023.",
 "response_to_email_id": null,
 "created_at": "2023-07-01T10:49:29",
 "sender": {
  "name": "Thundercable Notifications",
  "email": "notifications@thundercable.com"
 },
 "recipients": [
  {
   "name": "Carl Brown",
   "email": "carbrown@gmail.com"
  }
 ],
 "attachments": [
  {
   "id": 8485,
   "file_name": "2023-06.txt"
  }
 ]
}
```


### Environment Interaction 17
----------------------------------------------------------------------------
```python
gmail_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbWFpbCtjYXJicm93bkBnbWFpbC5jb20iLCJleHAiOjE2ODk2ODI0OTh9.Z3ojsBN5_Q4H4baXgCxEaj6vNNHfr5_M_MlgdH1Saz8"
email_id = 20869
attachment_id = 8485
attachment_content = apis.gmail.download_attachment(access_token=gmail_access_token, email_id=email_id, attachment_id=attachment_id)
print(attachment_content)
```

```
Execution failed. Traceback:
  File "<python-input>", line 4, in <module>
    attachment_content = apis.gmail.download_attachment(access_token=gmail_access_token, email_id=email_id, attachment_id=attachment_id)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: Response status code is 422:
{"message":"Validation error. Reason: \nfile_system_access_token: field required"}
```


### Environment Interaction 18
----------------------------------------------------------------------------
```python
file_system_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'file_system'), None)
if file_system_credentials:
    file_system_password = file_system_credentials['password']
    response = apis.file_system.login(username=apis.supervisor.MainUserMunch['email'], password=file_system_password)
    if 'access_token' in response:
        file_system_access_token = response['access_token']
        gmail_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbWFpbCtjYXJicm93bkBnbWFpbC5jb20iLCJleHAiOjE2ODk2ODI0OTh9.Z3ojsBN5_Q4H4baXgCxEaj6vNNHfr5_M_MlgdH1Saz8"
        email_id = 20869
        attachment_id = 8485
        attachment_content = apis.gmail.download_attachment(access_token=gmail_access_token, email_id=email_id, attachment_id=attachment_id, file_system_access_token=file_system_access_token)
        print(attachment_content)
    else:
        print("Failed to login to file system")
else:
    print("File system credentials not found")
```

```
Execution failed. Traceback:
  File "<python-input>", line 4, in <module>
    response = apis.file_system.login(username=apis.supervisor.MainUserMunch['email'], password=file_system_password)
                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'MainUserMunch' found in the supervisor app.
```


### Environment Interaction 19
----------------------------------------------------------------------------
```python
main_user = {'first_name': 'Carl', 'last_name': 'Brown', 'email': 'carbrown@gmail.com', 'phone_number': '7934818191'}
file_system_credentials = next((cred for cred in apis.supervisor.show_account_passwords() if cred['account_name'] == 'file_system'), None)
if file_system_credentials:
    file_system_password = file_system_credentials['password']
    response = apis.file_system.login(username=main_user['email'], password=file_system_password)
    if 'access_token' in response:
        file_system_access_token = response['access_token']
        gmail_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbWFpbCtjYXJicm93bkBnbWFpbC5jb20iLCJleHAiOjE2ODk2ODI0OTh9.Z3ojsBN5_Q4H4baXgCxEaj6vNNHfr5_M_MlgdH1Saz8"
        email_id = 20869
        attachment_id = 8485
        attachment_content = apis.gmail.download_attachment(access_token=gmail_access_token, email_id=email_id, attachment_id=attachment_id, file_system_access_token=file_system_access_token)
        print(attachment_content)
    else:
        print("Failed to login to file system")
else:
    print("File system credentials not found")
```

```
{
 "message": "Attachment downloaded in file_system app.",
 "file_path": "/home/carl/downloads/2023-06.txt"
}
```

