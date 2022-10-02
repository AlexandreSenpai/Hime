from flask import Flask

from manga_translator.utils.logging import Log

log = Log()

APP = Flask(__name__)

import manga_translator.infra.entrypoints.rest.routes.api
import manga_translator.infra.entrypoints.rest.routes.error