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
        "subject": "Double Charged - IMMEDIATE ACTION REQUIRED",
        "content": "I was charged TWICE for my subscription this month! This is unacceptable. I need a refund immediately or I'm canceling my account!"
    },
    {
        "sender": "feature.lover@email.com",
        "subject": "Feature Request - Dark Mode",
        "content": "Hey team! Love your app. Would be awesome if you could add dark mode to the mobile version. My eyes would really appreciate it."
    },
    {
        "sender": "tech.lead@enterprise.com",
        "subject": "Critical API Integration Issue",
        "content": "Our production API integration is failing intermittently with 504 timeout errors. This is affecting our business operations. We need urgent assistance to resolve this."
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
    
    for item in results:
        print(f"\nTest {item['test_case']}: {item['subject']}")
        print(f"  Urgency: {item['result']['urgency']}")
        print(f"  Topic: {item['result']['topic']}")
        print(f"  Action: {'ESCALATE' if item['result']['escalate'] else 'AUTO-REPLY'}")
        print(f"  Follow-up: {item['result']['follow_up']}")

if __name__ == "__main__":
    run_all_tests()
