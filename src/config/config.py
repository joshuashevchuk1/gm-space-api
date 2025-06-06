import os
import yaml
import logging
import logging.config


class Config:
    def __init__(self):
        self.g_meet_topic_name = "projects/zd-hackathon-2025/topics/workspace-events"
        self.g_meet_subscription_name= "projects/zd-hackathon-2025/subscriptions/workspace-events-sub"
        self.g_base_host = "localhost"
        self.g_base_port = "8080"
        self.g_space_port = "8010"

    def get_g_meet_topic_name(self):
        return self.g_meet_topic_name

    def get_g_meet_subscription_name(self):
        return self.g_meet_subscription_name

    def get_g_base_host(self):
        return self.g_base_host

    def get_g_base_port(self):
        return self.g_base_port

    def get_g_space_port(self):
        return self.g_space_port

