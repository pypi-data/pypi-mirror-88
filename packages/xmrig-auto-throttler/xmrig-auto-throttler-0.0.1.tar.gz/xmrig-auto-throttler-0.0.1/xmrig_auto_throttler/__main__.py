import json
import sys

import time
import logging

from .version import __version__
from .xmrig_api_client import XmrigClient
from .idle import get_idle_time_sec
from .dependencies import check_dependencies
from .args import get_args

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


logger = logging.getLogger()


class AutoThrottler:
    def __init__(
        self,
        interval=5,
        maximum_profile_timeout_sec=60,
        minimum_profile_timeout_sec=10,
        xmrig_host="http://127.0.0.1:8810",
        xmrig_token=None,
    ) -> None:
        super().__init__()
        assert interval < minimum_profile_timeout_sec
        self.interval = interval
        self.max_profile_timeout = maximum_profile_timeout_sec
        self.min_profile_timeout = minimum_profile_timeout_sec
        self.activated = False
        self.xmrig_http_client = XmrigClient(base_url=xmrig_host, token=xmrig_token)

    def is_active(self):
        return self.activated

    def activate(self):
        with open("maximum-config.json") as max_json_file:
            max_config = json.load(max_json_file)
            self.xmrig_http_client.set_config(max_config)
        logger.info("activate")
        self.activated = True

    def deactivate(self):
        with open("minimum-config.json") as min_json_file:
            min_config = json.load(min_json_file)
            self.xmrig_http_client.set_config(min_config)
        logger.info("deactivate")
        self.activated = False

    def run(self):
        while True:
            idle_time_sec = get_idle_time_sec()
            logger.info(f"idle for {idle_time_sec} seconds")

            if idle_time_sec > self.max_profile_timeout:
                if not self.is_active():
                    self.activate()

            if self.is_active():
                if idle_time_sec < self.min_profile_timeout:
                    self.deactivate()

            time.sleep(self.interval)


def main():
    check_dependencies()
    args = get_args()
    throttler = AutoThrottler(
        interval=args.interval,
        maximum_profile_timeout_sec=args.max_profile_timeout,
        minimum_profile_timeout_sec=args.min_profile_timeout,
        xmrig_host=args.xmrig_api_url,
        xmrig_token=args.xmrig_api_token,
    )

    try:
        throttler.run()
    except KeyboardInterrupt:
        logger.info("program stopped by user")


if __name__ == "__main__":
    sys.exit(main())
