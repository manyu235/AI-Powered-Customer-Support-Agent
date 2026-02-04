#!/usr/bin/env python
"""Test the support agent with various email scenarios."""

import sys
sys.path.insert(0, '.')

from support_agent import process_email

# Test cases
test_emails = [
    {
        "sender": "john@customer.com",
        "subject": "Simple Password Reset Request",
        "content": "Hi, I forgot my password. Can you help me reset it?"
    },
    {
        "sender": "sarah@company.com",
        "subject": "URGENT: Charged Twice for Subscription",
        "content": """Hi,
        
I was charged TWICE for my subscription this month. I received two charges of $99 each on my credit card. 
This is unacceptable and needs to be resolved immediately. I'm extremely frustrated with your service.

Please refund the duplicate charge right away.

Thanks,
Sarah"""
    },
    {
        "sender": "mike@enterprise.com",
        "subject": "CRITICAL: API Integration Failing in Production",
        "content": """URGENT ISSUE!

Our production environment is down because your API is returning 504 errors intermittently.
We have 50,000 customers unable to access their accounts. 
This is causing severe revenue loss.

We need immediate technical support. Please escalate this to your engineering team NOW.

Error logs attached.
Current status: CRITICAL
Time to resolve needed: IMMEDIATE"""
    },
    {
        "sender": "jane@startup.com",
        "subject": "Feature request: Dark mode",
        "content": "Hi, would you be able to add dark mode to the mobile app? It would be really helpful for nighttime usage."
    }
]

print("CUSTOMER SUPPORT AGENT TEST")
print("=" * 80)

for i, email in enumerate(test_emails, 1):
    print(f"\n\nTEST CASE {i}: {email['subject']}")
    print("-" * 80)
    
    result = process_email(
        email_content=email['content'],
        sender=email['sender']
    )
    
    # Highlight escalation status
    if result['escalate']:
        print("\n✓ ESCALATION TRIGGERED")
        print(f"Follow-up needed: {result['follow_up']}")
    else:
        print("\n✗ Auto-reply will be sent")

print("\n" + "=" * 80)
print("TEST COMPLETED")
