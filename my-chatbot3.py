from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, Tool, AgentType
import streamlit as st
import re

# 🔹 Initialize local Llama 3.2 via Ollama (update comment)
llm = OllamaLLM(model="llama3.2:3b", temperature=0)

# (Optional) If you want the model to reason briefly, build it into the question instead of CoT:
def normalize_question(q: str) -> str:
    return f"{q}\n\nAnswer succinctly. If a tool is needed, pick exactly one tool and explain briefly why."

def lookup_technical_details(equipment_name: str):
    code = equipment_name.strip().upper()
    if code in {"EQ12345", "EQ67890"}:
        return f"Technical details for {code}: Model X, Power: 999 W, Dimensions: 50x50x50 cm."
    return f"No technical details found for {equipment_name}."

def fetch_equipment_history(equipment_name: str):
    code = equipment_name.strip().upper()
    if code == "EQ12345":
        return "History for EQ12345: Purchased on 2023-01-15, Last serviced on 2024-06-10."
    return f"No history found for {equipment_name}."

def send_email_to_vendor(text: str):
    # allow "send email to vendor for EQ12345 about calibration" etc.
    code_match = re.search(r"\bEQ\d{5}\b", text.upper())
    code = code_match.group(0) if code_match else None
    if code == "EQ12345":
        details = text
        return (f"Email sent to vendor regarding {code}.\n"
                f"Body: Dear Vendor, we are reaching out regarding equipment {code}. "
                f"Context: {details}")
    elif code:
        return f"Failed to send email for {code}. Equipment not recognized in demo (only EQ12345 is enabled)."
    return "Failed to send email. No valid equipment code found (expected pattern EQ#####)."

tools = [
    Tool(
        name="Technical Document Lookup",
        func=lookup_technical_details,
        description=(
            "Use to retrieve technical specifications for an equipment code "
            "(pattern EQ#####). Input must be just the equipment code."
        ),
    ),
    Tool(
        name="Equipment History",
        func=fetch_equipment_history,
        description=(
            "Use to fetch service/purchase history for an equipment code "
            "(pattern EQ#####). Input must be just the equipment code."
        ),
    ),
    Tool(
        name="Email Vendor",
        func=send_email_to_vendor,
        description=(
            "Use to draft/send an email to the vendor about an equipment. "
            "Input can be natural language and should include the equipment code "
            "(pattern EQ#####) and any message details."
        ),
    ),
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=5,
    verbose=True,
)

# 🔹 Streamlit UI
st.title("Chatbot with Ollama and Tools")
user_input = st.text_input("Type a question (e.g., 'Technical details for EQ67890', 'History EQ12345', 'Send email to vendor for EQ12345 about calibration'):")

if user_input:
    response = agent.run(normalize_question(user_input))
    st.write("Response:", response)
