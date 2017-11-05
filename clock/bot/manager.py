from bot.action.core.action import ActionGroup
from bot.action.core.command import CommandAction
from bot.action.core.filter import MessageAction, TextMessageAction, NoPendingAction, PendingAction, InlineQueryAction, \
    ChosenInlineResultAction
from bot.action.standard.about import AboutAction, VersionAction
from bot.action.standard.admin import RestartAction, EvalAction, AdminActionWithErrorMessage, AdminAction, HaltAction
from bot.action.standard.admin.config_status import ConfigStatusAction
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


class BotManager:
    def __init__(self):
        self.bot = Bot()

    def setup_actions(self):
        self.bot.set_action(
            ActionGroup(
                LoggerAction().then(

                    ChosenInlineResultAction().then(
                        ChosenInlineResultClockAction()
                    ),

                    InlineQueryAction().then(
                        AsynchronousAction(
                            "inline_query",
                            min_workers=1,
                            max_workers=8,
                            max_seconds_idle=300
                        ).then(
                            InlineQueryClockAction()
                        )
                    ),

                    MessageAction().then(
                        PerChatAction().then(
                            InternationalizationAction().then(
                                TextMessageAction().then(

                                    CommandAction("start").then(
                                        StartAction()
                                    ),

                                    CommandAction("help").then(
                                        HelpAction()
                                    ),

                                    CommandAction("troubleshooting").then(
                                        TroubleshootAction()
                                    ),

                                    CommandAction("about").then(
                                        AboutAction(
                                            project_info.name,
                                            author_handle=project_info.author_handle,
                                            is_open_source=True,
                                            source_url=project_info.source_url,
                                            license_name=project_info.license_name)
                                    ),

                                    CommandAction("version").then(
                                        VersionAction(
                                            project_info.name,
                                            project_info.source_url + "/releases"
                                        )
                                    ),

                                    CommandAction("ping").then(
                                        AnswerAction("Up and running, sir!")
                                    ),

                                    CommandAction("benchmark").then(
                                        AdminActionWithErrorMessage().then(
                                            AsynchronousAction("benchmark").then(
                                                BenchmarkAction()
                                            )
                                        )
                                    ),
                                    CommandAction("cache").then(
                                        AdminActionWithErrorMessage().then(
                                            LocaleCacheAction()
                                        )
                                    ),
                                    CommandAction("restart").then(
                                        AdminActionWithErrorMessage().then(
                                            RestartAction()
                                        )
                                    ),
                                    CommandAction("halt").then(
                                        AdminActionWithErrorMessage().then(
                                            HaltAction()
                                        )
                                    ),
                                    CommandAction("eval").then(
                                        AdminActionWithErrorMessage().then(
                                            EvalAction()
                                        )
                                    ),
                                    CommandAction("state").then(
                                        AdminActionWithErrorMessage().then(
                                            StateAction()
                                        )
                                    ),
                                    CommandAction("config").then(
                                        AdminActionWithErrorMessage().then(
                                            ConfigStatusAction()
                                        )
                                    ),
                                    CommandAction("instance").then(
                                        AdminActionWithErrorMessage().then(
                                            InstanceAction()
                                        )
                                    ),
                                    CommandAction("workers").then(
                                        AdminActionWithErrorMessage().then(
                                            WorkersAction()
                                        )
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
                                        AnswerAction("I'm back! Sorry for the delay...")
                                    ),

                                    AdminAction().then(
                                        CommandAction("restart").then(
                                            RestartAction()
                                        ),
                                        CommandAction("halt").then(
                                            HaltAction()
                                        )
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
