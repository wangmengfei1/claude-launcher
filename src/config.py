import json
import os


class Config:
    """配置管理类，负责保存和加载用户配置"""

    DEFAULT_CONFIG = {
        "last_folder": "",
        "last_mode": "-c"
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """从 JSON 文件加载配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.config.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

    def save(self):
        """保存配置到 JSON 文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    @property
    def last_folder(self):
        return self.config.get("last_folder", "")

    @last_folder.setter
    def last_folder(self, value):
        self.config["last_folder"] = value
        self.save()

    @property
    def last_mode(self):
        return self.config.get("last_mode", "-c")

    @last_mode.setter
    def last_mode(self, value):
        self.config["last_mode"] = value
        self.save()
