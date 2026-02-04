from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Literal
import operator
import json

llm = ChatOllama(model="gemma3:latest")

class EmailState(TypedDict):
    email_content: str
    sender: str
    urgency: str
    topic: str
    knowledge_base_result: str
    response_draft: str
    escalate: bool
    follow_up: str
    reasoning: str

def classify_email(state: EmailState) -> EmailState:
    """Classify email by urgency and topic"""
    
    classification_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an email classifier for customer support.
        
Classify the email by:
1. Urgency: Low, Medium, High
2. Topic: Account, Billing, Bug, Feature Request, Technical Issue

Return valid JSON only:
{
  "urgency": "Low/Medium/High",
  "topic": "Account/Billing/Bug/Feature Request/Technical Issue",
  "reasoning": "brief explanation"
}"""),
        ("human", "Classify this email:\n\nFrom: {sender}\n\n{email_content}")
    ])
    
    try:
        response = llm.invoke(classification_prompt.format(
            sender=state["sender"],
            email_content=state["email_content"]
        ))
        
        result = json.loads(response.content)
        state["urgency"] = result.get("urgency", "Medium")
        state["topic"] = result.get("topic", "Technical Issue")
        state["reasoning"] = result.get("reasoning", "")
        
    except Exception as e:
        state["urgency"] = "Medium"
        state["topic"] = "Technical Issue"
        state["reasoning"] = f"Classification error: {str(e)}"
    
    print(f"Classification: Urgency={state['urgency']}, Topic={state['topic']}")
    return state

def search_knowledge_base(state: EmailState) -> EmailState:
    """Search knowledge base for relevant information"""
    
    knowledge_base = {
        "Account": """
Account Management:
- Password Reset: Go to Settings > Security > Reset Password. Click the link sent to your email.
- Account Deletion: Contact support@company.com with subject 'Account Deletion Request'
- Profile Updates: Settings > Profile > Edit Information
- Two-Factor Authentication: Settings > Security > Enable 2FA
        """,
        "Billing": """
Billing Information:
- Payment Methods: We accept credit cards, PayPal, and wire transfer
- Refund Policy: 30-day money-back guarantee for annual plans
- Billing Cycle: Charges occur on the same date each month
- Invoice Access: Account > Billing > Download Invoice
- Subscription Changes: Account > Subscription > Manage Plan
- Double Charge Resolution: Contact billing@company.com immediately with transaction IDs
        """,
        "Bug": """
Bug Reporting Process:
- Document the steps to reproduce the issue
- Note your browser/app version and operating system
- Capture screenshots or error messages if possible
- Check our status page at status.company.com for known issues
- Critical bugs are prioritized and typically fixed within 24-48 hours
- Export Feature: Known issue with PDF format on Chrome - use Firefox as temporary workaround
        """,
        "Feature Request": """
Feature Request Guidelines:
- Submit requests through our feedback portal at feedback.company.com
- Include use case and expected behavior
- Features are evaluated quarterly
- Popular requests are prioritized based on user votes
- Dark Mode: Currently in development for mobile app - expected Q2 2026
- API Rate Limits: Can be increased for enterprise plans
        """,
        "Technical Issue": """
Technical Support:
- Check system requirements at docs.company.com/requirements
- Clear browser cache and cookies
- Try incognito/private mode
- Disable browser extensions temporarily
- API Issues: Check API status at status.company.com/api
- 504 Errors: Usually indicate timeout - check your network connection and retry
- For persistent API issues, contact api-support@company.com with error logs
        """
    }
    
    topic = state.get("topic", "Technical Issue")
    state["knowledge_base_result"] = knowledge_base.get(topic, "No specific documentation found.")
    
    print(f"Knowledge base searched for topic: {topic}")
    return state

def draft_response(state: EmailState) -> EmailState:
    """Draft response based on classification and knowledge base"""
    
    response_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful customer support agent.

Draft a professional, empathetic email response based on:
- Customer email
- Urgency level
- Topic classification
- Knowledge base information

Guidelines:
- Be concise and friendly
- Address the specific issue
- Provide actionable steps
- If information is insufficient, acknowledge the issue and mention escalation
- Do not make up information not in the knowledge base

Return only the email response text, no JSON."""),
        ("human", """Customer Email:
From: {sender}
Content: {email_content}

Classification:
Urgency: {urgency}
Topic: {topic}

Knowledge Base Information:
{knowledge_base_result}

Draft a response:""")
    ])
    
    try:
        response = llm.invoke(response_prompt.format(
            sender=state["sender"],
            email_content=state["email_content"],
            urgency=state["urgency"],
            topic=state["topic"],
            knowledge_base_result=state["knowledge_base_result"]
        ))
        
        state["response_draft"] = response.content
        
    except Exception as e:
        state["response_draft"] = f"Error generating response: {str(e)}"
    
    print("Response drafted")
    return state

def decide_escalation(state: EmailState) -> EmailState:
    """Decide if email should be escalated to human agent"""
    
    escalation_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an escalation decision system.

Decide if this customer support case should be escalated to a human agent.

Escalate if:
- Urgency is High AND topic is Billing or Bug
- The knowledge base doesn't provide sufficient information
- The issue is complex or requires manual intervention
- Customer is frustrated or angry (detected from tone)
- API or technical issues affecting business operations

Return valid JSON only:
{
  "escalate": true/false,
  "follow_up": "none/24h/48h/1week",
  "reasoning": "brief explanation"
}"""),
        ("human", """Evaluate this case:

Email: {email_content}
Urgency: {urgency}
Topic: {topic}
Knowledge Base Match: {knowledge_base_result}

Should this be escalated?""")
    ])
    
    try:
        response = llm.invoke(escalation_prompt.format(
            email_content=state["email_content"],
            urgency=state["urgency"],
            topic=state["topic"],
            knowledge_base_result=state["knowledge_base_result"]
        ))
        
        result = json.loads(response.content)
        state["escalate"] = result.get("escalate", False)
        state["follow_up"] = result.get("follow_up", "none")
        
        escalation_reasoning = result.get("reasoning", "")
        if state["reasoning"]:
            state["reasoning"] += f" | Escalation: {escalation_reasoning}"
        else:
            state["reasoning"] = escalation_reasoning
        
    except Exception as e:
        state["escalate"] = state["urgency"] == "High"
        state["follow_up"] = "48h" if state["urgency"] == "High" else "none"
    
    print(f"Escalation decision: {state['escalate']}, Follow-up: {state['follow_up']}")
    return state

def should_escalate(state: EmailState) -> Literal["escalate", "auto_reply"]:
    """Router function for conditional branching"""
    return "escalate" if state["escalate"] else "auto_reply"

def auto_reply_node(state: EmailState) -> EmailState:
    """Final node for auto-reply cases"""
    print("Action: Sending auto-reply to customer")
    return state

def escalate_node(state: EmailState) -> EmailState:
    """Final node for escalated cases"""
    print("Action: Escalating to human agent")
    return state

def build_support_graph():
    """Build the LangGraph workflow"""
    
    workflow = StateGraph(EmailState)
    
    workflow.add_node("classify", classify_email)
    workflow.add_node("search_kb", search_knowledge_base)
    workflow.add_node("draft", draft_response)
    workflow.add_node("decide", decide_escalation)
    workflow.add_node("auto_reply", auto_reply_node)
    workflow.add_node("escalate", escalate_node)
    
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "search_kb")
    workflow.add_edge("search_kb", "draft")
    workflow.add_edge("draft", "decide")
    workflow.add_conditional_edges(
        "decide",
        should_escalate,
        {
            "auto_reply": "auto_reply",
            "escalate": "escalate"
        }
    )
    workflow.add_edge("auto_reply", END)
    workflow.add_edge("escalate", END)
    
    return workflow.compile()

def process_email(email_content: str, sender: str):
    """Process a customer support email through the workflow"""
    
    print("=" * 80)
    print(f"Processing email from: {sender}")
    print("=" * 80)
    
    graph = build_support_graph()
    
    initial_state = EmailState(
        email_content=email_content,
        sender=sender,
        urgency="",
        topic="",
        knowledge_base_result="",
        response_draft="",
        escalate=False,
        follow_up="",
        reasoning=""
    )
    
    result = graph.invoke(initial_state)
    
    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)
    print(f"From: {result['sender']}")
    print(f"Urgency: {result['urgency']}")
    print(f"Topic: {result['topic']}")
    print(f"Escalate: {result['escalate']}")
    print(f"Follow-up: {result['follow_up']}")
    print(f"\nReasoning: {result['reasoning']}")
    print(f"\nResponse Draft:\n{result['response_draft']}")
    print("=" * 80)
    
    return result
