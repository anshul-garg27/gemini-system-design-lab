#!/usr/bin/env python3
"""
Configuration file for API keys and settings.
"""

# Google AI API Keys - rotate through these for better rate limiting
API_KEYS = [
    "AIzaSyCO67rfGWXzxeQSqoupwezNw2RiaMxU5nI",
    "AIzaSyAfHg6t0-Udy1KlVinOIU5yFrRunf5iv2g",
    "AIzaSyDSzkrjD3UshtZpXB0pV0rX6O9GaS_Oz0E",
    "AIzaSyCF9wP4mSDbXI3QElmO-VKeevsuscL49cw",
    "AIzaSyBS8unFiuLU-r9ND1TJcbYT32FZeQnGA0s",
    "AIzaSyBivHBwzCgHQu-oHQSEdCqYc6ZvZNurmKQ",
    "AIzaSyAocySVoxeUr-Vx6sAjgg6rhzMy7447TJc",
    "AIzaSyAQBi13-FOhSgYFWNTIjUhtjPsfRJZPP0g",
    "AIzaSyA4Sqnbld4dn1Yk_3Q5GtC1cofkqhW6Pog",
    "AIzaSyDvIFxGFxRSh0DONVmKVbYcLxo_FR1pL0g",
    "AIzaSyBTaogpAnQd4pZ0cS3CxnuQxgIR4w0Qj6M",
    "AIzaSyAocySVoxeUr-Vx6sAjgg6rhzMy7447TJc",
    "AIzaSyAHWjPRSBqxCy_HxZPUdq7jvhMtLMlx1_E",
    "AIzaSyBMpzK0I14Va-xll7UmpFFdp6NThBKmmhc",
    "AIzaSyCQMAtRJi_eRhdncKDlgQps6R3-kV_VUGw",
    "AIzaSyBnH29S1Oh9XrF6kutqo6pmlwz1nsKQkHs",
    "AIzaSyA5bUWQT-cpHfQssIFGcauprtjB8CLS8RE",
    "AIzaSyAN_ylXmdx6zZaeDCwsRZQwbjsKUk7hqE0",
    "AIzaSyBo6p2cdYySWFQ7UScn9jfo8iKcwGZrkow",
    "AIzaSyAXdLlOmVMTlgZxAxHMbzf2UIS9WS-ioXk",
    "AIzaSyA4cjRvVWM4ARmsJTcFBKHGz3rE-XLV4K4",
    "AIzaSyBMxKAL8aHDKjC8b3jnXBuo8f7p7Tx6tl0",
    "AIzaSyBsa52QhnbwcDtatFOe83hGxb6e9OlbKp8",
    "AIzaSyCmZVEBJPWk5tPBwKTRiNJCb3YKUa6k3g8",
    "AIzaSyCCMFwXcF7HThTXavT9Pc9uWycPfFlbHkk",
    "AIzaSyCpux17G-66Mqy7BWrKAGCqSNePAz-ducQ",
    "AIzaSyA2BnCJtL8RexCA59KNLgUuzzKJGltDQOg",
    "AIzaSyBnceretTVjWYmeloNTEQhAiwoZqHSlM94",
    "AIzaSyCQTQYTcUXeLppc_B2Jt4X8-hJqOD6ExXw",
    "AIzaSyDLvr7PxzWS96SbZ1O0PhDCz1yNuOYqvVA",
    "AIzaSyC8_HvX76q6JtOrpCmmHj9xj6Eykvqe6w8",
    "AIzaSyB4bulGtue7NOwonm7Rj0ykzTpN7hfD2Uk",
    "AIzaSyAU6IFwMhGYlk5ymh2zHZKtjZcRsh5c2VE",
    "AIzaSyCK3jfI_5xx-0tLNvE0ltG_sAYRP3VFb0U",
    "AIzaSyB55cVFJBd7IPNCrKQoMi1KaZRGANIa3m0",
    "AIzaSyC550Ee3QwNbs0DIxTP5Ngl0xPAogiNKt4",
    "AIzaSyBiK_zyLuXeGiPhXDblzqs8IYU03SmDBY0",
    "AIzaSyCyFgENG21Od5si0gapOatIaT6WmZX5cWw",
    "AIzaSyBfGQaTYiAk3e8E6We4nc29fPUiVye3hZI",
    "AIzaSyANV0jxBnz_4P8yGKeFNVwazdy-6fO8DSo",
    "AIzaSyAJlhYqlnjZpOmRwHmracp4qy-4i0NXHu8",
    "AIzaSyDaFHxwumIXzL1zQiEf-C3CqPLG8_dVyNk",
    "AIzaSyD-uNhFBmbJ-wGroJVIMl1MTkNj2VqfX48",
    "AIzaSyCOAOk4CKKKe4D0SuOO6S0EcKmAnkdEI_c"
]

# Processing settings
BATCH_SIZE = 5
DELAY_SECONDS = 1.0
OUTPUT_DIR = "output"

# Database settings
DATABASE_PATH = "unified.db"

# Date settings (optional - will use today if not specified)
# CREATED_DATE = "2024-01-15"
# UPDATED_DATE = "2024-01-15"
