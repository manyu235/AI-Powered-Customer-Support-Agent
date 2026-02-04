from support_agent import process_email

test_emails = [
    {
        "sender": "john.doe@email.com",
        "subject": "Password Reset Issue",
        "content": "Hi, I forgot my password and need help resetting it. How do I do that?"
    },
    {
        "sender": "sarah.smith@company.com",
        "subject": "URGENT: Export Feature Crash",
        "content": "The export feature crashes every time I try to select PDF format. This is blocking my work. Please help immediately!"
    },
    {
        "sender": "angry.customer@email.com",
        "subject": "CRITICAL: Double Charged - IMMEDIATE REFUND REQUIRED",
        "content": """I am EXTREMELY upset and frustrated!

I was charged TWICE for my subscription this month. Two charges of $99 each hit my credit card today.

This is completely unacceptable and I need IMMEDIATE action:
1. Full refund of the duplicate charge ($99)
2. Confirmation that this won't happen again
3. Some compensation for this inconvenience

If this is not resolved within 24 hours, I am canceling my account and posting negative reviews everywhere.

Transaction IDs: TXN-55443 and TXN-55444
Account: ACC-89012

This needs to be escalated NOW to someone with authority to process refunds.

Sincerely,
An upset customer"""
    },
    {
        "sender": "feature.lover@email.com",
        "subject": "Feature Request - Dark Mode",
        "content": "Hey team! Love your app. Would be awesome if you could add dark mode to the mobile version. My eyes would really appreciate it."
    },
    {
        "sender": "tech.lead@enterprise.com",
        "subject": "CRITICAL: Production API Integration Failure",
        "content": """URGENT - PRODUCTION OUTAGE

Our production environment is experiencing critical failures with your API integration.

Details:
- 504 timeout errors occurring intermittently
- Affecting 50,000+ active users
- Business-critical transactions are failing
- Revenue impact is severe

Status: CRITICAL - Business operations halted
Time Sensitivity: IMMEDIATE resolution required
Impact: Production environment down

We need escalation to your engineering team RIGHT NOW.

Error logs and transaction IDs available.

Contact: ops@enterprise.com
Phone: +1-555-0123"""
    }
]

def run_all_tests():
    print("Running all test scenarios...")
    print("\n")
    
    results = []
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n{'#' * 80}")
        print(f"TEST CASE {i}: {email['subject']}")
        print(f"{'#' * 80}\n")
        
        result = process_email(email["content"], email["sender"])
        results.append({
            "test_case": i,
            "subject": email["subject"],
            "result": result
        })
        
        if i < len(test_emails):
            input("\nPress Enter to continue to next test case...")
    
    print("\n\n" + "=" * 80)
    print("SUMMARY OF ALL TEST CASES")
    print("=" * 80)
    
    escalated_count = 0
    for item in results:
        escalated = item['result']['escalate']
        action = 'ESCALATE ⬆️' if escalated else 'AUTO-REPLY ✓'
        if escalated:
            escalated_count += 1
        
        print(f"\nTest {item['test_case']}: {item['subject']}")
        print(f"  Urgency: {item['result']['urgency']}")
        print(f"  Topic: {item['result']['topic']}")
        print(f"  Action: {action}")
        print(f"  Follow-up: {item['result']['follow_up']}")
    
    print(f"\n{'=' * 80}")
    print(f"ESCALATION SUMMARY: {escalated_count} out of {len(results)} cases escalated to human agent")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    run_all_tests()
