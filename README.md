# AI-Powered Customer Support Agent

An intelligent customer support system built with LangChain and LangGraph that automatically processes customer emails, classifies them, searches knowledge bases, drafts responses, and escalates complex cases to human agents.

## Architecture Overview

This system uses a multi-node graph-based workflow with conditional routing:

```
START → Classify Email → Search KB → Draft Response → Decide Escalation
                                                              ↓
                                                    ┌─────────┴─────────┐
                                                    ↓                   ↓
                                              Auto Reply          Escalate to Human
                                                    ↓                   ↓
                                                   END                 END
```

### Nodes

1. **Classify Email**: Analyzes urgency (Low/Medium/High) and topic (Account/Billing/Bug/Feature Request/Technical Issue)
2. **Search KB**: Retrieves relevant information from knowledge base using RAG
3. **Draft Response**: Generates customer-friendly response based on classification and KB results
4. **Decide Escalation**: Determines if human intervention is needed
5. **Auto Reply**: Sends automated response for simple cases
6. **Escalate**: Routes complex cases to human agents

### Conditional Routing

The workflow uses conditional edges based on:
- Escalation decision (true/false)
- Urgency level (High urgency + certain topics trigger escalation)
- Knowledge base match quality
- Issue complexity

## Features

- **Email Classification**: Automatic urgency and topic detection
- **RAG-based Knowledge Base**: Searches relevant documentation
- **Response Generation**: Context-aware, empathetic responses
- **Smart Escalation**: Rules-based escalation logic
- **Follow-up Scheduling**: Automatic follow-up recommendations
- **Graph Visualization**: Visual representation of workflow

## Requirements

Install dependencies:

```bash
pip install langchain-ollama langchain-core langgraph pillow
```

Install Ollama and model:

```bash
ollama pull gemma3:latest
```

## Usage

### 1. Visualize the Workflow Graph

Generate a visual diagram of the agent workflow:

```bash
python visualize_graph.py
```

This creates `support_agent_graph.png` showing all nodes and edges.

### 2. Run Test Scenarios

Test with 5 predefined scenarios:

```bash
python test_scenarios.py
```

This tests:
1. Simple password reset (Low urgency, Account)
2. Bug report with export crash (High urgency, Bug)
3. Urgent billing double charge (High urgency, Billing)
4. Feature request for dark mode (Low urgency, Feature Request)
5. Complex API integration issue (High urgency, Technical Issue)

### 3. Process Custom Email

Use the agent programmatically:

```python
from support_agent import process_email

result = process_email(
    email_content="I can't log into my account",
    sender="customer@email.com"
)

print(result["response_draft"])
print(f"Escalate: {result['escalate']}")
```

## Knowledge Base

The system includes built-in documentation for:

- **Account Management**: Password resets, profile updates, 2FA
- **Billing**: Payment methods, refunds, invoices, subscription changes
- **Bug Reporting**: Process, known issues, workarounds
- **Feature Requests**: Submission process, roadmap, voting
- **Technical Support**: Troubleshooting, API issues, error codes

## Classification Logic

### Urgency Levels

- **Low**: Simple questions, feature requests, general inquiries
- **Medium**: Account issues, standard bugs, clarifications
- **High**: Billing problems, critical bugs, business-impacting issues

### Topics

- **Account**: Login, password, profile, security
- **Billing**: Charges, refunds, subscriptions, invoices
- **Bug**: Software defects, crashes, errors
- **Feature Request**: New capabilities, enhancements
- **Technical Issue**: API problems, integration issues, performance

## Escalation Rules

Cases are escalated to human agents when:

1. Urgency is High AND topic is Billing or Bug
2. Knowledge base lacks sufficient information
3. Issue requires manual intervention
4. Customer shows frustration or anger
5. API/technical issues affecting business operations

Auto-reply is used for:
- Simple questions with clear KB answers
- Low/Medium urgency with good KB match
- Feature requests (logged automatically)
- Standard account management tasks

## Follow-up Schedule

- **none**: Issue resolved with auto-reply
- **24h**: High urgency cases requiring quick check-in
- **48h**: Medium urgency issues needing verification
- **1week**: Feature requests or non-urgent items

## Output Format

Each processed email returns:

```python
{
    "sender": "customer@email.com",
    "email_content": "Original email text",
    "urgency": "High",
    "topic": "Billing",
    "knowledge_base_result": "Relevant KB content",
    "response_draft": "Generated response text",
    "escalate": True,
    "follow_up": "24h",
    "reasoning": "Explanation of decisions"
}
```

## Example Scenarios

### Scenario 1: Simple Password Reset

**Input**: "How do I reset my password?"

**Output**:
- Urgency: Low
- Topic: Account
- Escalate: False
- Action: Auto-reply with KB instructions

### Scenario 2: Critical Bug

**Input**: "The export feature crashes when I select PDF format."

**Output**:
- Urgency: High
- Topic: Bug
- Escalate: True
- Action: Route to human agent with known workaround

### Scenario 3: Billing Issue

**Input**: "I was charged twice for my subscription!"

**Output**:
- Urgency: High
- Topic: Billing
- Escalate: True
- Follow-up: 24h
- Action: Immediate escalation to billing team

## Project Structure

```
Customer_Support/
├── support_agent.py          # Main agent with LangGraph workflow
├── test_scenarios.py         # 5 test cases with sample emails
├── visualize_graph.py        # Graph visualization generator
├── support_agent_graph.png   # Generated workflow diagram
└── README.md                 # Documentation
```

## Design Decisions

1. **Multi-node workflow**: Separates concerns for clarity and maintainability
2. **RAG approach**: Knowledge base search before response generation
3. **Conditional routing**: Dynamic escalation based on multiple factors
4. **Structured state**: TypedDict ensures type safety and clear data flow
5. **LLM-based classification**: Flexible, learns from context vs rigid rules
6. **Error handling**: Fallback values for robustness

## Evaluation Criteria

- **Classification Accuracy**: Multi-factor urgency and topic detection
- **Response Quality**: Context-aware, empathetic, actionable responses
- **Escalation Logic**: Rules-based with LLM assistance for edge cases
- **Code Quality**: Clear structure, type hints, documentation
- **Real-world Practicality**: Handles edge cases, errors, and complex scenarios

## Future Enhancements

- Customer sentiment analysis
- Multi-language support
- Integration with ticketing systems
- Learning from human agent feedback
- A/B testing of response templates
- Performance metrics dashboard

## License

MIT License
