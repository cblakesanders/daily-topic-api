from fastapi import FastAPI
from services.topic_service import TopicService
from services.llm_service import LlmService
from services.video_service import VideoService

app = FastAPI(title="Daily Topics API")

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
    sentences = llm_service.get_topic_sentences(topic)
    video_url = video_service.get_video(topic)
    return {
        "topic": topic,
        "paragraph": paragraph,
        "sentences": sentences,
        "video_url": video_url,
        "status": "FastAPI is working!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)