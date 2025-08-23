from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, Tool
import streamlit as st

# 🔹 Initialize the local Gemma 3B model via Ollama
model = OllamaLLM(model="mistral")

# 🔹 Define the prompt template for step-by-step reasoning
template = """ Question : {question}
Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

def lookup_technical_details(equipment_name):
    # Dummy implementation for retrieving technical details
    normalized = equipment_name.strip().upper()
    if normalized == "EQ12345":
        return "Technical details for EQ12345: Model X, Power: 500W, Dimensions: 50x50x50 cm."
    return f"No technical details found for {equipment_name}."

def fetch_equipment_history(equipment_name):
    # Dummy implementation for fetching equipment history
    normalized = equipment_name.strip().upper()
    if normalized == "EQ12345":
        return "History for EQ12345: Purchased on 2023-01-15, Last serviced on 2024-06-10."
    return f"No history found for {equipment_name}."

def send_email_to_vendor(equipment_name):
    # Dummy implementation for sending an email
    normalized = equipment_name.strip().upper()
    if "EQ12345"== normalized:
        details = "Dummy email content: Dear Vendor, we are reaching out regarding equipment EQ12345. Please provide further details or assistance as needed."
        return f"Email sent to vendor regarding {equipment_name}: {details}"
    return f"Failed to send email for {equipment_name}. Equipment not recognized."

# 🔹 Define tools for the agent
tools = [
    Tool(
        name="Technical Document Lookup",
        func=lookup_technical_details,  # Dummy return for document lookup
        description=(
            "Retrieves technical specifications from equipment documents. "
            "Input should be an equipment code (e.g. EQ12345) to get detailed specs."
        )
    ),
    Tool(
        name="Equipment History",
        func=fetch_equipment_history,  # Dummy return for equipment history
        description=(
            "Fetches the service and purchase history of equipment. "
            "Provide the equipment code (e.g. EQ12345) to look up its history."
        )
    ),
    Tool(
        name="Email Vendor",
        func=send_email_to_vendor,  # Dummy return for email functionality
        description=(
            "Sends an email to the vendor with provided details on technical information and history. "
            "The input should contain the equipment code (e.g. EQ12345) along with any details to be sent."
        )
    )
]

# 🔹 Initialize the agent with tools and the model
agent = initialize_agent(
    tools, 
    model, 
    agent_type="zero-shot-react-description",
    max_iterations=5,  # Increase this value if needed
    verbose=True
)

# 🔹 Streamlit UI for user interaction
st.title("Chatbot with Ollama and Tools")
user_input = st.text_input("Type a question:")

if user_input:
    response = agent.run(user_input)
    st.write("Response:", response)