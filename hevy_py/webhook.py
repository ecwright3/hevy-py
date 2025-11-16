"""
Webhook handling utilities for Hevy API
"""

from flask import Flask, request, jsonify
from typing import Callable, Optional
import logging
from .models import WebhookNotification

logger = logging.getLogger(__name__)


class HevyWebhookHandler:
    """Handles incoming webhook notifications from Hevy"""

    def __init__(self):
        self.app = Flask(__name__)
        self.notification_callback: Optional[Callable[[WebhookNotification], None]] = None

        @self.app.route('/', methods=['POST'])
        def handle_webhook():
            try:
                data = request.get_json()
                if not data:
                    logger.warning("Received webhook with no JSON data")
                    return jsonify({"error": "Invalid JSON"}), 400

                notification = WebhookNotification(**data)
                logger.info(f"Received webhook notification: workout_id={notification.workout_id}")

                if self.notification_callback:
                    self.notification_callback(notification)
                else:
                    logger.warning("No callback registered for webhook notifications")

                return jsonify({"status": "received"}), 200

            except Exception as e:
                logger.error(f"Error processing webhook: {e}")
                return jsonify({"error": "Internal server error"}), 500

    def register_callback(self, callback: Callable[[WebhookNotification], None]):
        """
        Register a callback function to handle webhook notifications

        Args:
            callback: Function that takes a WebhookNotification and returns None
        """
        self.notification_callback = callback

    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """
        Run the webhook server

        Args:
            host: Host to bind to (default: 0.0.0.0)
            port: Port to listen on (default: 5000)
            debug: Enable debug mode (default: False)
        """
        logger.info(f"Starting webhook server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)