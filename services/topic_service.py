from data.topics import TOPICS


class TopicService:
    def __init__(self):
        self.topics = TOPICS
        self.index = 0

    def get_topic(self):
        topic = self.topics[self.index % len(self.topics)]

        self.index += 1

        return topic
