
### Environment Interaction 1
----------------------------------------------------------------------------
```python
# Get Gmail access token for main_user
print(apis.gmail.access_token_from(main_user={'first_name': 'Katie', 'last_name': 'Simpson', 'email': 'kat_simp@gmail.com', 'phone_number': '6727300099'}))

# Define a helper to fetch all pages
def fetch_all(api, **kw):
    out, page = [], 0
    while True:
        r = api(**kw, page_index=page, page_limit=20)
        if not r: break
        out += r
        if len(r) < 20: break
        page += 1
    return out

# Fetch all Gmail drafts
drafts = fetch_all(apis.gmail.show_drafts, access_token=apis.gmail.access_token_from(main_user={'first_name': 'Katie', 'last_name': 'Simpson', 'email': 'kat_simp@gmail.com', 'phone_number': '6727300099'}))

# Print the drafts to inspect
print(drafts)
```

```
Execution failed. Traceback:
  File "<python-input>", line 2, in <module>
    print(apis.gmail.access_token_from(main_user={'first_name': 'Katie', 'last_name': 'Simpson', 'email': 'kat_simp@gmail.com', 'phone_number': '6727300099'}))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: No API named 'access_token_from' found in the gmail app.
```


### Environment Interaction 2
----------------------------------------------------------------------------
```python
# Get Gmail access token for main_user
print(apis.gmail.api_docs.show_api_descriptions())
print(apis.gmail.api_docs.show_app_descriptions())
```

```
Execution failed. Traceback:
  File "<python-input>", line 2, in <module>
    print(apis.gmail.api_docs.show_api_descriptions())
          ^^^^^^^^^^^^^^^^^^^
Exception: No API named 'api_docs' found in the gmail app.
```


### Environment Interaction 3
----------------------------------------------------------------------------
```python
# Get Gmail access token for main_user
print(apis.api_docs.show_app_descriptions())
print(apis.api_docs.show_api_descriptions(app_name='gmail'))
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


### Environment Interaction 4
----------------------------------------------------------------------------
```python
# Get Gmail access token for main_user
print(apis.supervisor.show_account_passwords())
```

```
[
 {
  "account_name": "amazon",
  "password": "!#i62}T"
 },
 {
  "account_name": "file_system",
  "password": "0rE1V#a"
 },
 {
  "account_name": "gmail",
  "password": "u%TW7ah"
 },
 {
  "account_name": "phone",
  "password": "4_%505T"
 },
 {
  "account_name": "simple_note",
  "password": "Q=srh$w"
 },
 {
  "account_name": "splitwise",
  "password": "]aOK-3Z"
 },
 {
  "account_name": "spotify",
  "password": "aHOM-+d"
 },
 {
  "account_name": "todoist",
  "password": "ffqROlZ"
 },
 {
  "account_name": "venmo",
  "password": "B)]&d{u"
 }
]
```


### Environment Interaction 5
----------------------------------------------------------------------------
```python
# Login to Gmail and get access token
gmail_password = [x['password'] for x in apis.supervisor.show_account_passwords() if x['account_name'] == 'gmail'][0]
print(apis.gmail.login(email='kat_simp@gmail.com', password=gmail_password))
```

```
Execution failed. Traceback:
  File "<python-input>", line 3, in <module>
    print(apis.gmail.login(email='kat_simp@gmail.com', password=gmail_password))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exception: Response status code is 422:
{"message":"Validation error. Reason: \nusername: field required"}
```


### Environment Interaction 6
----------------------------------------------------------------------------
```python
# Login to Gmail and get access token
gmail_password = [x['password'] for x in apis.supervisor.show_account_passwords() if x['account_name'] == 'gmail'][0]
print(apis.gmail.login(username='kat_simp@gmail.com', password=gmail_password))
```

```
{
 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbWFpbCtrYXRfc2ltcEBnbWFpbC5jb20iLCJleHAiOjE2ODQ0MTIwOTh9.ChdP7jyPQYnkUJXZBywOBrJmq36axbD0MMgSYdFGSGI",
 "token_type": "Bearer"
}
```


### Environment Interaction 7
----------------------------------------------------------------------------
```python
# Login to Gmail and get access token
gmail_password = [x['password'] for x in apis.supervisor.show_account_passwords() if x['account_name'] == 'gmail'][0]
access_token = apis.gmail.login(username='kat_simp@gmail.com', password=gmail_password)['access_token']

# Define a helper to fetch all pages
def fetch_all(api, **kw):
    out, page = [], 0
    while True:
        r = api(**kw, page_index=page, page_limit=20)
        if not r: break
        out += r
        if len(r) < 20: break
        page += 1
    return out

# Fetch all Gmail drafts
drafts = fetch_all(apis.gmail.show_drafts, access_token=access_token)

# Print the drafts to inspect
print(drafts)
```

```
[
 {
  "draft_id": 479,
  "subject": "Performance Review Schedules",
  "body": "Hello Adrian,\n\nYour performance review is scheduled for next week. Please prepare any materials or feedback you'd like to discuss.\n\nThanks,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-17T18:36:03",
  "updated_at": "2023-05-17T18:36:03",
  "recipients": [
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 25,
  "subject": "Updated Office Security Protocols",
  "body": "Dear team,\n\nPlease review the updated security protocols for our office. It's important that everyone is aware and compliant. Safety first!\n\nCheers,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-15T13:30:25",
  "updated_at": "2023-05-15T13:30:25",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 27,
  "subject": "Upcoming Project Deadlines",
  "body": "",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-11T08:36:31",
  "updated_at": "2023-05-11T08:36:31",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 26,
  "subject": "Internship Program Applications Open",
  "body": "Hello team,\n\nOur internship program applications are now open! If you know any students or recent graduates who would be interested in joining our team, please share the attached flyer with them. We appreciate your help in spreading the word.\n\nBest regards,\nKatie\n",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-10T15:51:40",
  "updated_at": "2023-05-10T15:51:40",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 85,
  "subject": "",
  "body": "",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-09T15:26:10",
  "updated_at": "2023-05-09T15:26:10",
  "recipients": [
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 210,
  "subject": "Invitation: Diversity and Inclusion Workshop",
  "body": "Team,\n\nWe have organized a Diversity and Inclusion workshop next month. It's highly encouraged for everyone to attend. Please RSVP.\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-03T12:23:52",
  "updated_at": "2023-05-03T12:23:52",
  "recipients": [
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 209,
  "subject": "",
  "body": "",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-01T16:30:14",
  "updated_at": "2023-05-01T16:30:14",
  "recipients": [
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 478,
  "subject": "Upcoming Project Deadlines",
  "body": "Hello team,\n\nA quick reminder about the upcoming project deadlines. Let's ensure we're on track.\n\nBest,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-01T10:22:01",
  "updated_at": "2023-05-01T10:22:01",
  "recipients": [
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 84,
  "subject": "Updated Company Policies",
  "body": "",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-04-29T13:04:43",
  "updated_at": "2023-04-29T13:04:43",
  "recipients": [
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 473,
  "subject": "Year-End Party Planning Committee",
  "body": "Hi team,\n\nWho would be interested in being part of the year-end party planning committee? We need volunteers!\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-04-20T14:49:58",
  "updated_at": "2023-04-20T14:49:58",
  "recipients": [
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 24,
  "subject": "",
  "body": "",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-03-26T15:13:25",
  "updated_at": "2023-03-26T15:13:25",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 276,
  "subject": "Dinner Plans Tonight?",
  "body": "I'm craving pizza for dinner tonight. Are you up for it? Let's satisfy those taste buds!\n\nHungry hugs,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-12-25T08:04:21",
  "updated_at": "2022-12-25T08:04:21",
  "recipients": [
   {
    "name": "Jeffery Simpson",
    "email": "je.simpson@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 476,
  "subject": "",
  "body": "",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-11-14T14:24:41",
  "updated_at": "2022-11-14T14:24:41",
  "recipients": [
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 52,
  "subject": "",
  "body": "Dear team,\n\nA friendly reminder to submit your expense reports for the recent business trip by end of today. Please ensure that all receipts are attached and expenses are properly categorized. Let's keep our financial records accurate and up to date.\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-10-10T18:30:19",
  "updated_at": "2022-10-10T18:30:19",
  "recipients": [
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 50,
  "subject": "Invitation: Diversity and Inclusion Workshop",
  "body": "Team,\n\nWe have organized a Diversity and Inclusion workshop next month. It's highly encouraged for everyone to attend. Please RSVP.\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-10-08T09:04:00",
  "updated_at": "2022-10-08T09:04:00",
  "recipients": [
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 293,
  "subject": "",
  "body": "Team,\n\nWe've updated some of our company policies. Please review the attached document and acknowledge receipt.\n\nBest regards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-08-04T11:25:52",
  "updated_at": "2022-08-04T11:25:52",
  "recipients": [
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 81,
  "subject": "Project Update: Milestone Achieved",
  "body": "Dear all,\n\nI'm pleased to announce that we've successfully reached a major milestone in the project ahead of schedule. Kudos to the entire team for their hard work and dedication. Let's keep up the momentum as we move into the next phase.\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-05-19T12:18:15",
  "updated_at": "2022-05-19T12:18:15",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 }
]
```


### Environment Interaction 8
----------------------------------------------------------------------------
```python
# Login to Gmail and get access token
gmail_password = [x['password'] for x in apis.supervisor.show_account_passwords() if x['account_name'] == 'gmail'][0]
access_token = apis.gmail.login(username='kat_simp@gmail.com', password=gmail_password)['access_token']

# Define a helper to fetch all pages
def fetch_all(api, **kw):
    out, page = [], 0
    while True:
        r = api(**kw, page_index=page, page_limit=20)
        if not r: break
        out += r
        if len(r) < 20: break
        page += 1
    return out

# Fetch all Gmail drafts
drafts = fetch_all(apis.gmail.show_drafts, access_token=access_token)

# Delete drafts with empty subject or body
for draft in drafts:
    if not draft['subject'] or not draft['body']:
        print(apis.gmail.delete_draft(access_token=access_token, draft_id=draft['draft_id']))

# Verify the deletion
print(fetch_all(apis.gmail.show_drafts, access_token=access_token))
```

```
{"message": "Draft deleted."}
{"message": "Draft deleted."}
{"message": "Draft deleted."}
{"message": "Draft deleted."}
{"message": "Draft deleted."}
{"message": "Draft deleted."}
{"message": "Draft deleted."}
{"message": "Draft deleted."}
[
 {
  "draft_id": 479,
  "subject": "Performance Review Schedules",
  "body": "Hello Adrian,\n\nYour performance review is scheduled for next week. Please prepare any materials or feedback you'd like to discuss.\n\nThanks,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-17T18:36:03",
  "updated_at": "2023-05-17T18:36:03",
  "recipients": [
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 25,
  "subject": "Updated Office Security Protocols",
  "body": "Dear team,\n\nPlease review the updated security protocols for our office. It's important that everyone is aware and compliant. Safety first!\n\nCheers,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-15T13:30:25",
  "updated_at": "2023-05-15T13:30:25",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 26,
  "subject": "Internship Program Applications Open",
  "body": "Hello team,\n\nOur internship program applications are now open! If you know any students or recent graduates who would be interested in joining our team, please share the attached flyer with them. We appreciate your help in spreading the word.\n\nBest regards,\nKatie\n",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-10T15:51:40",
  "updated_at": "2023-05-10T15:51:40",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 210,
  "subject": "Invitation: Diversity and Inclusion Workshop",
  "body": "Team,\n\nWe have organized a Diversity and Inclusion workshop next month. It's highly encouraged for everyone to attend. Please RSVP.\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-03T12:23:52",
  "updated_at": "2023-05-03T12:23:52",
  "recipients": [
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 478,
  "subject": "Upcoming Project Deadlines",
  "body": "Hello team,\n\nA quick reminder about the upcoming project deadlines. Let's ensure we're on track.\n\nBest,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-05-01T10:22:01",
  "updated_at": "2023-05-01T10:22:01",
  "recipients": [
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 473,
  "subject": "Year-End Party Planning Committee",
  "body": "Hi team,\n\nWho would be interested in being part of the year-end party planning committee? We need volunteers!\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2023-04-20T14:49:58",
  "updated_at": "2023-04-20T14:49:58",
  "recipients": [
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 276,
  "subject": "Dinner Plans Tonight?",
  "body": "I'm craving pizza for dinner tonight. Are you up for it? Let's satisfy those taste buds!\n\nHungry hugs,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-12-25T08:04:21",
  "updated_at": "2022-12-25T08:04:21",
  "recipients": [
   {
    "name": "Jeffery Simpson",
    "email": "je.simpson@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 50,
  "subject": "Invitation: Diversity and Inclusion Workshop",
  "body": "Team,\n\nWe have organized a Diversity and Inclusion workshop next month. It's highly encouraged for everyone to attend. Please RSVP.\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-10-08T09:04:00",
  "updated_at": "2022-10-08T09:04:00",
  "recipients": [
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Isaac Miller",
    "email": "ismill@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 },
 {
  "draft_id": 81,
  "subject": "Project Update: Milestone Achieved",
  "body": "Dear all,\n\nI'm pleased to announce that we've successfully reached a major milestone in the project ahead of schedule. Kudos to the entire team for their hard work and dedication. Let's keep up the momentum as we move into the next phase.\n\nRegards,\nKatie",
  "belongs_to_email_thread_id": null,
  "response_to_email_id": null,
  "scheduled_send_at": null,
  "created_at": "2022-05-19T12:18:15",
  "updated_at": "2022-05-19T12:18:15",
  "recipients": [
   {
    "name": "Bradley Ball",
    "email": "bradley_ball@gmail.com"
   },
   {
    "name": "Ronald Harrison",
    "email": "ron.harrison@gmail.com"
   },
   {
    "name": "Miranda Weber",
    "email": "mir-powe@gmail.com"
   },
   {
    "name": "Jeremy Calhoun",
    "email": "jer.calhoun@gmail.com"
   },
   {
    "name": "Mason Smith",
    "email": "masmith@gmail.com"
   },
   {
    "name": "Adrian Burton",
    "email": "adrian_burt@gmail.com"
   }
  ],
  "attachments": []
 }
]
```


### Environment Interaction 9
----------------------------------------------------------------------------
```python
apis.supervisor.complete_task(answer=None, status="success")
```

```
Execution successful.
```


### Environment Interaction 10
----------------------------------------------------------------------------
```python
# Re-read the Gmail drafts
gmail_password = [x['password'] for x in apis.supervisor.show_account_passwords() if x['account_name'] == 'gmail'][0]
access_token = apis.gmail.login(username='kat_simp@gmail.com', password=gmail_password)['access_token']

# Define a helper to fetch all pages
def fetch_all(api, **kw):
    out, page = [], 0
    while True:
        r = api(**kw, page_index=page, page_limit=20)
        if not r: break
        out += r
        if len(r) < 20: break
        page += 1
    return out

# Fetch all Gmail drafts
drafts = fetch_all(apis.gmail.show_drafts, access_token=access_token)

# Check if all drafts have non-empty subject and body
for draft in drafts:
    if not draft['subject'] or not draft['body']:
        print("Error: Draft with empty subject or body found.")
        break
else:
    print("DONE_VERIFIED")
```

```
DONE_VERIFIED
```

