from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils import timezone



def mailer(to, subject_, msg=None, token=None, event=None):
    """
    Send email message
    """
    to = ['{}'.format(to)]
    from_email = "TechSemester Admin <netbraus@gmail.com>"
    if token: #it's not a confirmation of action
        message = f"Your Account Confirmation code is {token}\n\nExpires in 10 minutes."
        subject = subject_ #"SpendWise - Account Confirmation."
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
        return True
    if msg: #It is a confirmation and message will vary so we get the message passed
        if event:
            message = event
        else:
            message = msg
        subject = subject_
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()
        return True
    return False

def sendEmail(user_obj, subject, email_heading, information=None, otp=None):
	"""
	Send email to logged in user with their details
    - email heading stays at the heading part of the email inthe template
    - subject is subject of the email
    - information will be the body of the message if it is not None.
	"""
	try:
		# subject = "e-Duu Designz Store - New Order #{}".format(transaction.id)
		to = [user_obj.email]
		from_email = "TechSemester Admin <netbraus@gmail.com>"
		email_details = {
		'email_heading' : email_heading,
		'otp' : otp,
		'information' : information,
		'user': user_obj,
		'time': timezone.now().date()
		}

		message = get_template('email/email.html').render(email_details)
		msg = EmailMessage(subject, message, to=to, from_email=from_email)
		msg.content_subtype = 'html'
		msg.send()
	except:
		return False

def general_comm(user_obj, subject, email_heading, information=None, channel=None, name=None, email=None):
    """
    Call this funciton in a lop to send email to a group of users
    """

    from_email = "SpendWise Admin <admin@spendwise.ng>"

    if channel == 'audience':
        to = [email]
        email_details = {"user":name}
        message = get_template('email/external_comm.html').render(email_details)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    else:
        try:
            to = [user_obj.email]
            email_details = {
                'email_heading': email_heading,
                'information': information,
                'user': user_obj,
                'time': timezone.now().date()
            }

            if channel == 'comm':
                message = get_template('email/communication.html').render(email_details)
            elif channel == 'news':
                message = get_template('email/newsletter.html').render(email_details)

            msg = EmailMessage(subject, message, to=to, from_email=from_email)
            msg.content_subtype = 'html'
            msg.send()
        except Exception as e:
            print(e)