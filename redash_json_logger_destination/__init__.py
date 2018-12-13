import json
import logging
from datetime import datetime

from redash.destinations import BaseDestination, register


class JSONLogger(BaseDestination):
    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                },
            },
            "required": ["path"],
        }

    @classmethod
    def icon(cls):
        return "fa-file"

    def notify(self, alert, query, user, new_state, app, host, options):
        try:
            data = {
                "datetime": datetime.now().isoformat(),
                "new_state": new_state,
                "alert": {
                    "id": alert.id,
                    "name": alert.name,
                },
                "query": {
                    "id": query.id,
                    "name": query.name,
                },
            }
            f = open(options.get("path"), "a")
            f.write("{}\n".format(json.dumps(data)))
        except:
            logging.exception("JSON write ERROR.")
        finally:
            if f:
                f.close()


register(JSONLogger)
