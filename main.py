from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from services.topic_service import TopicService
from services.llm_service import LlmService
from services.video_service import VideoService
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

app = FastAPI(title="Daily Topics API")

# Load environment variables
load_dotenv()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Contact form model
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

topic_service = TopicService()
llm_service = LlmService()
video_service = VideoService()

@app.get("/")
def read_root():
    return {"message": "Welcome to Daily Topics API!"}

@app.get("/daily-topic")
def get_daily_topic():
    topic = topic_service.get_topic()
    paragraph = llm_service.get_topic_paragraph(topic)
    grammar_exercise, grammar_answer_key = llm_service.get_grammar_exercise_with_answers(topic)
    video_url = video_service.get_video(topic)
    return {
        "topic": topic,
        "paragraph": paragraph,
        "grammar_exercise": grammar_exercise,
        "grammar_answer_key": grammar_answer_key,
        "video_url": video_url,
        "status": "FastAPI is working!"
    }

def send_email(contact_data: ContactForm):
    """Send email using Gmail SMTP"""
    try:
        # Get email credentials from environment variables
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL", gmail_user)  # Default to sender if not specified
        
        if not gmail_user or not gmail_password:
            raise Exception("Gmail credentials not configured")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = "Daily Topics User"
        msg['To'] = recipient_email
        msg['Subject'] = f"Daily Topics Contact: {contact_data.subject}"
        
        # Create email body
        body = f"""
        New contact form submission from Daily Topics:
        
        Name: {contact_data.name}
        Email: {contact_data.email}
        Subject: {contact_data.subject}
        
        Message:
        {contact_data.message}
        
        ---
        Sent from Daily Topics Contact Form
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, recipient_email, text)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.post("/send-email")
def send_contact_email(contact_data: ContactForm):
    """Send contact form email"""
    try:
        # Basic validation
        if not contact_data.name.strip() or not contact_data.message.strip():
            raise HTTPException(status_code=400, detail="Name and message are required")
        
        # Send email
        success = send_email(contact_data)
        
        if success:
            return {"message": "Email sent successfully!", "success": True}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)