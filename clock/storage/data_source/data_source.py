class StorageDataSource:
    def init(self):
        raise NotImplementedError()

    def save_query(self, user_id: int, timestamp: str, query: str, offset: str, language_code: str, locale: str,
                   results_found_len: int, results_sent_len: int, processing_seconds: float):
        raise NotImplementedError()

    def save_chosen_result(self, user_id: int, timestamp: str, chosen_zone_name: str, query: str,
                           choosing_seconds: float):
        raise NotImplementedError()

    def save_command(self, message_id: int, command: str, command_args: str):
        raise NotImplementedError()

    def save_message(self, chat_id: int, message_id: int, user_id: int, date: int, is_forward: bool,
                     reply_to_message: int, is_edit: bool, text: str, new_chat_member: int, left_chat_member: int,
                     group_chat_created: bool, migrate_to_chat_id: int, migrate_from_chat_id: int):
        raise NotImplementedError()

    def get_message_id(self, chat_id: int, message_id: int):
        raise NotImplementedError()

    def save_chat(self, chat_id: int, chat_type: str, title: str, username: str):
        raise NotImplementedError()

    def save_user(self, user_id: int, first_name: str, last_name: str, username: str, language_code: str, is_bot: bool):
        raise NotImplementedError()

    def set_active_chat(self, chat_id: int):
        raise NotImplementedError()

    def set_inactive_chat(self, chat_id: int, reason: str):
        raise NotImplementedError()

    def get_recent_queries_language_codes(self, limit: int):
        raise NotImplementedError()

    def context_manager(self):
        raise NotImplementedError()
