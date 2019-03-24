from jobsync.models import Candidate, Match
import sys, datetime

EMAIL_SUBJECT = "Your latest JobSync matches!"
EMAIL_FROM_ADDRESS = "updates@jobsync.com"

thresholds = {'weekly':7, 'bi-weekly':14, 'monthly':31, 'never': sys.maxint}

def email_candidates():
    candidates = Candidate.objects.all()
    for candidate in candidates:
        if (is_email_needed (candidate.email_preference, candidate.last_email_time)):
            matches = Match.objects.filter(candidate__pk=candidate.pk)
            msg = ""
            for match in matches:
                msg += "Match %s: %s \n" % (match.job, match.candidate_score)
            send_email (msg, [candidate.email])
            candidate.last_email_time = datetime.datetime.now()
            candidate.save()
        
def is_email_needed(email_preference, last_email_time):
    now = datetime.datetime.now()
    threshold = thresholds[email_preference]
    timedelta = now - last_email_time
    if timedelta.days > threshold:
        return True
    return False

def send_email(msg, recipients):
    send_mail((EMAIL_SUBJECT, msg, EMAIL_FROM_ADDRESS, recipients)
