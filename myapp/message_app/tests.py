from django.test import TestCase
from .models import Message
from datetime import datetime
from .service import MessageService

class MessageServiceTest(TestCase):
    def setUp(self):
        Message.objects.create(content = "Test case1", emission_time = datetime(2022, 6, 14), author = "User1", target = "User2")
        Message.objects.create(content = "Test case2", emission_time = datetime(2022, 6, 15), author = "User2", target = "User1")
        Message.objects.create(content = "Test case3", emission_time = datetime(2022, 6, 16), author = "User1", target = "User2")
        
    def test_get_message(self):
        message_service = MessageService()
        messages = message_service.get_messages(author = "User1", target = "User2")
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0].get_author(), "User1")
        self.assertEqual(messages[0].get_target(), "User2")
        self.assertEqual(messages[0].get_content(), "Test case1")
        self.assertEqual(messages[1].get_author(), "User2")
        self.assertEqual(messages[1].get_target(), "User1")
        self.assertEqual(messages[1].get_content(), "Test case2")
        self.assertEqual(messages[2].get_author(), "User1")
        self.assertEqual(messages[2].get_target(), "User2")
        self.assertEqual(messages[2].get_content(), "Test case3")

    def test_create_message(self):
        message_service = MessageService()
        message_service.create_message(author = "User2", target = "User1", content = "Test case creation")
        last_message = message_service.get_messages(author = "User1", target = "User2").last()
        self.assertEqual(last_message.get_content(), "Test case creation")

    def test_get_targets_and_last_messages(self):
        message_service = MessageService()
        target_message = message_service.get_targets_and_last_messages(user = "User1")
        self.assertEqual(len(target_message), 1)
        self.assertEqual(target_message[0].target, "User2")
        self.assertEqual(target_message[0].message.content, "Test case3")

    def test_get_targets_last_message(self):
        message_service = MessageService()
        target_messages = message_service.get_targets_last_message(user = "User1", targets = ("User1", "User2"))
        self.assertEqual(len(target_messages), 2)
        self.assertEqual(target_messages[0].target, "User1")
        self.assertEqual(target_messages[0].message, None)
        self.assertEqual(target_messages[1].target, "User2")
        self.assertEqual(target_messages[1].message.content, "Test case3")

    def test_count_message_sent_by_username(self):
        message_service = MessageService()
        self.assertEqual(message_service.count_message_sent_by_username(username = "User1"), 2)


    def test_count_message_sent_to_username(self):
        message_service = MessageService()
        self.assertEqual(message_service.count_message_sent_to_username(username = "User1"), 1)