import paho.mqtt.client as mqtt
from redis import Redis
from typing import TypedDict
from enum import Enum


class PrinterInfo(TypedDict):
    """Contains printer info stored in DB"""

    id: str
    ip: str
    access: str
    name: str
    model: str
    serial: str
    outlet: str


class Printer:
    """Class for tracking a printer"""

    redis: Redis
    printer_info: PrinterInfo

    def __init__(
        self,
        id: str,
        redis: Redis,
    ):
        """Initializes printer object"""
        self.redis = redis
        self.printer_info = self.fetch_printer_info(id)

    def fetch_printer_info(self, id: str) -> PrinterInfo:
        """Fetches printer info from DB"""
        return self.redis.hgetall(id)

    def push_printer_info(self):
        """Updates printer info in DB"""
        self.redis.hmset(self.printer_info["id"], self.printer_info)

    def fetch_status_value(self, key: str) -> str:
        """Fetches status value from DB"""
        return self.redis.hget(self.printer_info["id"] + "_state", key)

    def fetch_entire_status(self) -> dict:
        """Fetches entire status from DB"""
        return self.redis.hgetall(self.printer_info["id"] + "_state")

    def push_status_value(self, key: str, value: str):
        """Pushes status value to DB"""
        self.redis.hset(self.printer_info["id"] + "_state", key, value)

    def push_entire_status(self, status: dict):
        """Pushes entire status to DB"""
        self.redis.hmset(self.printer_info["id"] + "_state", status)
