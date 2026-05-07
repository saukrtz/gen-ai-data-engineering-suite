import os
from fpdf import FPDF
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# ---------------------------------------------------------
# 1. Generate 4 Dummy PDF Files
# ---------------------------------------------------------
# pdf_dir = "company_policies"
# os.makedirs(pdf_dir, exist_ok=True)

# policies = {
#     "ACCENTURE": """GLOBAL TECHNOLOGY AND CONSULTING HR GUIDELINES v4.2
# 1. Introduction
# Welcome to Accenture. As a global professional services company with leading capabilities in digital, cloud, and security, we are committed to delivering on the promise of technology and human ingenuity. 
# 2. Technology Stack & Certifications
# Employees in the Advanced Application Engineering division are expected to maintain active certifications in AWS, Azure, or Google Cloud. We highly encourage participation in our internal upskilling programs focusing on microservices architecture, Kubernetes orchestration, and enterprise-scale Java spring boot applications.
# 3. Leave Policies
# 3.1 Annual Leave: Employees accrue 1.5 days of paid time off (PTO) per month, totaling 18 days per year.
# 3.2 Sick Leave: 10 days of fully paid sick leave are granted annually. A medical certificate is required for absences exceeding 3 consecutive days.
# 3.3 Sabbatical: After 5 years of continuous service, employees may apply for a 3-month unpaid sabbatical for personal development.
# 4. Corporate Ethics
# All employees must complete the annual compliance training by Q2. Gifts from clients exceeding $50 in value must be declared to the ethics compliance officer immediately. 
# 5. Remote Work
# Hybrid work models are determined by the project manager. Core hours are 10:00 AM to 4:00 PM local time.""",
#     "NAGARRO": """CARING, AGILE, AND FLAT HIERARCHY
# 1. The Nagarro Way
# At Nagarro, we believe in a fluid, non-hierarchical structure. We focus on Agile methodologies, rapid prototyping, and delivering client-centric software solutions. 
# 2. Interview and Onboarding
# Our interview process emphasizes algorithmic thinking and cultural fit. New hires undergo a 2-week bootcamp focusing on our internal proprietary tools and clean code principles.
# 3. Employee Wellness and Family Programs
# 3.1 Paternity Leave: Nagarro provides 4 weeks of fully paid paternity leave for secondary caregivers. 
# 3.2 Wellness Subsidy: Employees receive a $500 annual stipend for gym memberships, ergonomic home office equipment, or mental health applications.
# 4. Professional Development
# We sponsor up to two major tech conferences per year for our senior engineers. Additionally, employees have free access to O'Reilly learning and Udemy Business.
# 5. Travel Policy
# When traveling for client site visits, daily per diem is set at $75 for domestic and $120 for international travel. Economy class is standard for flights under 6 hours.""",
#     "ERNST & YOUNG (EY)": """TECHNOLOGY CONSULTING AND AI INTERNSHIP GUIDELINES
# 1. Corporate Overview
# EY is dedicated to building a better working world. Our technology consulting arm is rapidly expanding, with a massive focus on Generative AI, machine learning, and data analytics.
# 2. AI Internships and Projects
# Interns joining the Generative AI division will work closely with senior partners to develop cutting-edge LLM integrations for financial auditing and risk assessment. Security and data privacy are paramount; all models must be trained on anonymized, air-gapped data lakes.
# 3. General Leave and Holidays
# 3.1 Public Holidays: EY observes 11 standard national holidays.
# 3.2 Bereavement Leave: Employees are entitled to 5 days of paid leave in the event of the loss of an immediate family member.
# 4. Dress Code
# Client-facing roles require business professional attire. For internal office days, business casual is acceptable. Denim is only permitted on designated "Jeans Fridays."
# 5. Continuing Education
# EY provides tuition reimbursement of up to $5,000 per calendar year for pre-approved graduate degree programs related to finance, business, or data science.""",
#     "SIGMOID": """DATA ENGINEERING AND HR POLICIES 2026
# 1. Engineering Excellence
# Sigmoid specializes in building robust data pipelines and advanced analytics platforms. Our core stack relies heavily on Databricks, Apache Spark, and Delta Lake. We strictly adhere to the Medallion Architecture pattern (Bronze for raw data, Silver for cleansed and conformed data, and Gold for business-level aggregates).
# 2. Data Governance
# All pipelines orchestrated via Apache Airflow must include data quality checks before promoting data to the Gold tier. Personally Identifiable Information (PII) must be masked at the Silver level.
# 3. Sigmoid Family and Leave Policies
# 3.1 Annual PTO: 20 days per year, with a maximum rollover of 5 days into the next calendar year.
# 3.2 Maternity Policy: Sigmoid is committed to supporting new mothers. Eligible female employees are entitled to 26 weeks of fully paid maternity leave. For mothers having two or more surviving children, the paid maternity leave entitlement is reduced to 12 weeks. Furthermore, the policy includes a guaranteed "Return to Work" phase, allowing a mandatory work-from-home option post-maternity leave for up to 3 months, ensuring a smooth transition back into data engineering projects. A one-time maternity medical bonus of $750 is also provided upon submission of hospital bills.
# 3.3 Adoption Leave: 12 weeks of paid leave for the primary adopting parent of a child under the age of 3.
# 4. Infrastructure and Hardware
# Standard issue hardware for data engineers is a 16-inch MacBook Pro (M-series, 32GB RAM). Cloud compute costs must be tagged with the appropriate project billing code in GCP or AWS."""
# }

pdf_dir = "company_policies"
os.makedirs(pdf_dir, exist_ok=True)

policies = {"travel_policy": """Document Title: Travel Policy

Employees must obtain approval before booking business travel.

Economy class is allowed for flights under 5 hours.
Business class is allowed for senior management.

Hotel bookings should be within approved budget limits.

Travel expenses must be submitted within 7 days after travel completion.""", "paternity_policy": """Document Title: Paternity Policy

Male employees are entitled to 10 working days of paternity leave.

This leave must be availed within 3 months of childbirth.
The leave is fully paid.

Employees must inform their reporting manager in advance.""", "maternity_policy": """Document Title: Maternity Policy

Female employees are entitled to 26 weeks of maternity leave.
The leave can be taken before or after childbirth.

Medical insurance covers maternity-related expenses.
Flexible work-from-home options may be provided post leave.

Employees must notify HR at least 8 weeks prior to expected delivery date.""", "it_security_policy": """Document Title: IT Security Policy

All employees must use VPN for remote access.

Passwords must be at least 12 characters long and changed every 60 days.

Sharing credentials is strictly prohibited.
Multi-factor authentication is mandatory.

Access to sensitive systems is logged and monitored.""", "hr_leave_policy": """Document Title: HR Leave Policy

Employees are entitled to 20 paid leaves annually.
Casual leave: 8 days per year.
Sick leave: 12 days per year.

Unused leaves can be carried forward up to 10 days to the next year.
Employees must apply for leave through the HR portal.

Leave approval depends on reporting manager approval.
Leaves exceeding 3 consecutive days require documentation.""", "expense_policy": """Document Title: Expense Reimbursement Policy

Employees can claim reimbursement for business-related expenses.

Valid receipts must be submitted for all claims.

Meal expenses are capped at $50 per day.
Transport expenses should be reasonable and justified.

Reimbursements will be processed within 10 working days."""}

for company, policy in policies.items():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"{company} HR Policy Document", ln=True, align='C')
    pdf.multi_cell(0, 10, txt=policy)
    pdf_path = os.path.join(pdf_dir, f"{company}_policy.pdf")
    pdf.output(pdf_path)
    
print("Successfully generated 4 company PDF files.\n")

# ---------------------------------------------------------
# 2. Load PDFs using PyPDFDirectoryLoader
# ---------------------------------------------------------
loader = PyPDFDirectoryLoader(pdf_dir)
documents = loader.load()
print(f"Loaded {len(documents)} pages from the PDF directory.\n")

# ---------------------------------------------------------
# 3. Chunking & Embedding
# ---------------------------------------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} text chunks.")

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents=chunks, embedding=embedding_model)
print("Embeddings generated and stored in FAISS.\n")

# ---------------------------------------------------------
# 4. RAG Pipeline
# ---------------------------------------------------------
# Initialize the Llama 3 model via Groq
api_key = os.environ.get("llama_key") or os.environ.get("GROQ_API_KEY")
llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=api_key)

query = "What is the password policy?"
print(f"Querying LLM: '{query}'")

# Perform similarity search
results = vectorstore.similarity_search(query, k=2)
context = "\n\n".join([r.page_content for r in results])

# Prompt the LLM
prompt = f"Based on the following Context:\n{context}\n\nQuestion: {query}\nAnswer:"
response = llm.invoke(prompt)

print("\n--- LLM Response ---")
print(response.content)
