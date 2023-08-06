from typing import Any, cast
import urllib

from terminado import NamedTermManager, TermSocket
import tornado.web


class AnyscaleTermSocket(TermSocket):  # type: ignore
    def check_origin(self, origin: Any) -> bool:
        parsed_origin = urllib.parse.urlparse(origin)
        if self.application.settings["deploy_environment"] == "development":
            return True
        elif self.application.settings["deploy_environment"] == "staging":
            return cast(bool, parsed_origin.netloc.endswith("anyscale.dev"))
        else:
            return cast(bool, parsed_origin.netloc.endswith("beta.anyscale.com"))


class TerminalPageHandler(tornado.web.RequestHandler):
    """Render the /ttyX pages"""

    def delete(self, term_name: str) -> None:
        term_manager = self.application.settings["term_manager"]

        term_manager.kill(term_name)
        del term_manager.terminals[term_name]


class TerminalListHandler(tornado.web.RequestHandler):
    """List active terminals."""

    def get(self) -> None:
        term_manager = self.application.settings["term_manager"]

        data = {
            "terminals": [
                {"id": terminal} for terminal in term_manager.terminals.keys()
            ]
        }

        self.write(data)


class NewTerminalHandler(tornado.web.RequestHandler):
    """Create new unused terminal"""

    def get(self) -> None:
        self.application.settings["term_manager"].new_named_terminal()


def make_application(deploy_environment: str) -> tornado.web.Application:
    term_manager = NamedTermManager(shell_command=["bash"], max_terminals=100)

    handlers: Any = [
        (
            r"/webterminal/_websocket/(\w+)",
            AnyscaleTermSocket,
            {"term_manager": term_manager},
        ),
        (r"/webterminal/new/?", NewTerminalHandler),
        (r"/webterminal/list", TerminalListHandler),
        (r"/webterminal/(\w+)/?", TerminalPageHandler),
    ]
    return tornado.web.Application(
        handlers, term_manager=term_manager, deploy_environment=deploy_environment,
    )


def main(deploy_environment: str) -> None:
    application = make_application(deploy_environment)

    port = 8700
    application.listen(port, "localhost")
    print("Listening on localhost:{}".format(port))
    loop = tornado.ioloop.IOLoop.instance()

    try:
        loop.start()
    except KeyboardInterrupt:
        print(" Shutting down on SIGINT")
    finally:
        application.settings["term_manager"].shutdown()
        loop.close()
