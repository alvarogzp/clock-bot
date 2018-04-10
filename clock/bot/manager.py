from bot.action.core.action import ActionGroup
from bot.action.core.command import CommandAction
from bot.action.core.filter import MessageAction, TextMessageAction, NoPendingAction, PendingAction, InlineQueryAction, \
    ChosenInlineResultAction, EditedMessageAction
from bot.action.standard.about import AboutAction, VersionAction
from bot.action.standard.admin import RestartAction, EvalAction, AdminActionWithErrorMessage, HaltAction
from bot.action.standard.admin.config_status import ConfigStatusAction
from bot.action.standard.admin.fail import FailAction
from bot.action.standard.admin.instance import InstanceAction
from bot.action.standard.admin.state import StateAction
from bot.action.standard.answer import AnswerAction
from bot.action.standard.asynchronous import AsynchronousAction
from bot.action.standard.benchmark import BenchmarkAction, WorkersAction
from bot.action.standard.internationalization import InternationalizationAction
from bot.action.standard.logger import LoggerAction
from bot.action.standard.perchat import PerChatAction
from bot.bot import Bot

from clock import project_info
from clock.bot.commands.admin.locale_cache import LocaleCacheAction
from clock.bot.commands.help import HelpAction
from clock.bot.commands.start import StartAction
from clock.bot.commands.troubleshoot import TroubleshootAction
from clock.bot.inline.chosen_result import ChosenInlineResultClockAction
from clock.bot.inline.query.action import InlineQueryClockAction
from clock.bot.save.command import SaveCommandAction
from clock.bot.save.message import SaveMessageAction


class BotManager:
    def __init__(self):
        self.bot = Bot(project_info.name)

    def setup_actions(self):
        self.bot.set_action(
            ActionGroup(
                LoggerAction(reuse_max_length=2000, reuse_max_time=1, reuse_max_number=10).then(

                    InlineQueryAction().then(
                        AsynchronousAction(
                            "inline_query",
                            min_workers=int(self.bot.config.min_query_workers or 1),
                            max_workers=int(self.bot.config.max_query_workers or 8),
                            max_seconds_idle=300
                        ).then(
                            InlineQueryClockAction()
                        )
                    ),

                    ChosenInlineResultAction().then(
                        ChosenInlineResultClockAction()
                    ),

                    EditedMessageAction().then(
                        SaveMessageAction()
                    ),

                    MessageAction().then(
                        PerChatAction().then(

                            SaveMessageAction(),

                            InternationalizationAction().then(
                                TextMessageAction().then(

                                    CommandAction("start").then(
                                        SaveCommandAction(),
                                        StartAction()
                                    ),

                                    CommandAction("help").then(
                                        SaveCommandAction(),
                                        HelpAction()
                                    ),

                                    CommandAction("troubleshooting").then(
                                        SaveCommandAction(),
                                        TroubleshootAction()
                                    ),

                                    CommandAction("about").then(
                                        SaveCommandAction(),
                                        AboutAction(
                                            project_info.name,
                                            authors=project_info.authors_credits,
                                            is_open_source=project_info.is_open_source,
                                            url=project_info.url,
                                            license_name=project_info.license_name,
                                            license_url=project_info.license_url,
                                            donation_addresses=project_info.donation_addresses
                                        )
                                    ),

                                    CommandAction("version").then(
                                        SaveCommandAction(),
                                        VersionAction(
                                            project_info.name,
                                            project_info.url + "/releases"
                                        )
                                    ),

                                    CommandAction("benchmark").then(
                                        AdminActionWithErrorMessage().then(
                                            AsynchronousAction("benchmark").then(
                                                SaveCommandAction(),
                                                BenchmarkAction()
                                            )
                                        )
                                    ),
                                    CommandAction("cache").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            LocaleCacheAction()
                                        )
                                    ),
                                    CommandAction("restart").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            RestartAction()
                                        )
                                    ),
                                    CommandAction("halt").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            HaltAction()
                                        )
                                    ),
                                    CommandAction("eval").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            EvalAction()
                                        )
                                    ),
                                    CommandAction("state").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            StateAction()
                                        )
                                    ),
                                    CommandAction("config").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            ConfigStatusAction()
                                        )
                                    ),
                                    CommandAction("instance").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            InstanceAction()
                                        )
                                    ),
                                    CommandAction("workers").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            WorkersAction()
                                        )
                                    ),
                                    CommandAction("fail").then(
                                        AdminActionWithErrorMessage().then(
                                            SaveCommandAction(),
                                            FailAction()
                                        )
                                    )

                                )
                            )
                        )
                    ),

                    NoPendingAction().then(
                        MessageAction().then(
                            PerChatAction().then(
                                TextMessageAction().then(
                                    CommandAction("ping").then(
                                        SaveCommandAction(),
                                        AnswerAction("Up and running, sir!")
                                    )
                                )
                            )
                        )
                    ),

                    PendingAction().then(
                        MessageAction().then(
                            PerChatAction().then(
                                TextMessageAction().then(
                                    CommandAction("ping").then(
                                        SaveCommandAction(),
                                        AnswerAction("I'm back! Sorry for the delay...")
                                    )
                                )
                            )
                        )
                    )

                )
            )
        )

    def run(self):
        self.bot.run()
