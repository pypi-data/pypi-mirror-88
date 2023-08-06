import argparse


def get_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="xmrig-auto-throttler")
    parser.add_argument(
        "--interval",
        dest="interval",
        default=5,
        help="Interval in seconds between (not)idle checks. This must be smaller than min-profile-timeout",
        type=int,
    )
    parser.add_argument(
        "--max-profile-timeout",
        dest="max_profile_timeout",
        default=60,
        const=True,
        nargs="?",
        help="When minimum-profile is active (PC is being used by you), your idle time must be above min-profile-timeout to switch to maximum-profile.",
        type=int,
    )
    parser.add_argument(
        "--min-profile-timeout",
        dest="min_profile_timeout",
        default=10,
        const=True,
        nargs="?",
        help="When maximum-profile is active (PC not used), your idle time must be below min-profile-timeout to switch to minimum-profile. This must be bigger than interval.",
        type=int,
    )
    parser.add_argument(
        "--xmrig-api-url",
        dest="xmrig_api_url",
        default="http://127.0.0.1:8000",
        nargs="?",
        help="xmrig host url, for example http://127.0.0.1:8000",
    )
    parser.add_argument(
        "--xmrig-api-token",
        dest="xmrig_api_token",
        default="",
        nargs="?",
        help="xmrig api token",
    )

    return parser.parse_args(args)
