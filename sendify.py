from twilio.rest import Client
import imaplib
import email
import time
from win10toast import ToastNotifier

def send_whatsapp_notification(email_content):
    try:
        # Twilio credentials
        account_sid = 'AC08dac1484f5054458b2bd3ffdff03d6e'
        auth_token = '68b90fab2ee96dc1b92f74d57fb61746'
        twilio_number = 'whatsapp:+14155238886'  # Your Twilio WhatsApp number

        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Extract email content from the first part of the email payload (assuming plain text format)
        email_text = email_content[0].as_string()

        # Truncate email content if it exceeds the character limit
        if len(email_text) > 1600:
            email_text = email_text[:1600]  # Truncate to 1600 characters

        # Send WhatsApp message with truncated email content
        message = client.messages.create(
            from_=twilio_number,
            body=email_text,  # Include truncated email content in the WhatsApp message body
            to='whatsapp:+2349133273608'  # Recipient's WhatsApp number
        )

        print("WhatsApp notification sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending WhatsApp notification: {e}")

def check_emails(username, app_specific_password):
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL('imap.hostinger.com', 993)

        # Login with the app-specific password
        mail.login(username, app_specific_password)

        # Select the mailbox (in this case, Inbox)
        mail.select('inbox')

        # Search for unseen emails
        result, data = mail.search(None, 'UNSEEN')

        # Initialize the toast notifier
        toaster = ToastNotifier()

        # Iterate through each email found
        for num in data[0].split():
            # Fetch the email
            result, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Extract information like sender, subject, etc.
            sender = email.utils.parseaddr(email_message['From'])[1]
            subject = email_message['Subject']

            # Notify yourself about the new email
            toast_text = f"New email from {sender}: {subject}"
            toaster.show_toast("New Email Notification", toast_text, duration=10)

            # Send WhatsApp notification
            send_whatsapp_notification(email_message.get_payload())  # Pass email content to the function

        # Close the connection
        mail.close()
        mail.logout()
    except Exception as e:
        print(f"An error occurred: {e}")

# Your email credentials
username = 'admin@swiftsendify.com'
app_specific_password = 'Javacc#php1!'  # Use the app-specific password generated

# Main loop
while True:
    check_emails(username, app_specific_password)
    # Check every 60 seconds
    time.sleep(60)
