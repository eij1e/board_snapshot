import json

class ZulipStream:
    def __init__(self, stream: str, topic: str):
        self.stream = stream
        self.topic = topic

class Config:
    def __init__(
        self,
        auditory: str,
        rtsp: str,
        rtsp_435: str,
        rtsp_505: str,
        pc_path: str,
        zulip_private_status: bool,
        zulip_stream_status: bool,
        zulip_private_list: list[str],
        zulip_stream: ZulipStream,
        mail_status: bool,
        mail_list: list[str],
        hotkeys: list[str],
        hotkeys_interim: list[str],
        stop_flag: bool,
        info_435: dict,
        info_505: dict,
        info_other: dict
    ):
        self.auditory = auditory
        self.rtsp = rtsp
        self.rtsp_435 = rtsp_435
        self.rtsp_505 = rtsp_505
        self.pc_path = pc_path
        self.zulip_private_status = zulip_private_status
        self.zulip_stream_status = zulip_stream_status
        self.zulip_private_list = zulip_private_list
        self.zulip_stream = zulip_stream
        self.mail_status = mail_status
        self.mail_list = mail_list
        self.hotkeys = hotkeys
        self.hotkeys_interim = hotkeys_interim
        self.stop_flag = stop_flag
        self.info_435 = info_435
        self.info_505 = info_505
        self.info_other = info_other

    def dump(self):
        json_dict = {
            "auditory": self.auditory,
            "rtsp": self.rtsp,
            "rtsp_435": self.rtsp_435,
            "rtsp_505": self.rtsp_505,
            "pc_path": self.pc_path,
            "zulip_private_status": self.zulip_private_status,
            "zulip_stream_status": self.zulip_stream_status,
            "zulip_private_list": self.zulip_private_list,
            "zulip_stream": {
                "stream": self.zulip_stream.stream,
                "topic": self.zulip_stream.topic,
            },
            "mail_status": self.mail_status,
            "mail_list": self.mail_list,
            "hotkeys": self.hotkeys,
            "hotkeys_interim": self.hotkeys_interim,
            "stop_flag": self.stop_flag,
            "info_435": self.info_435,
            "info_505": self.info_505,
            "info_other": self.info_other
        }
        with open("config.json", "w") as f:
            json.dump(json_dict, f, indent=4)

def new_config(file_path: str) -> Config:
    with open(file_path, "r") as f:
        json_dict = json.load(f)
        return Config(
            auditory=json_dict["auditory"],
            rtsp=json_dict["rtsp"],
            rtsp_435=json_dict["rtsp_435"],
            rtsp_505=json_dict["rtsp_505"],
            pc_path=json_dict["pc_path"],
            zulip_private_status=json_dict["zulip_private_status"],
            zulip_stream_status=json_dict["zulip_stream_status"],
            zulip_private_list=json_dict["zulip_private_list"],
            zulip_stream=ZulipStream(stream=json_dict["zulip_stream"]["stream"], topic=json_dict["zulip_stream"]["topic"]),
            mail_status=json_dict["mail_status"],
            mail_list=json_dict["mail_list"],
            hotkeys=json_dict["hotkeys"],
            hotkeys_interim=json_dict["hotkeys_interim"],
            stop_flag=json_dict["stop_flag"],
            info_435=json_dict["info_435"],
            info_505=json_dict["info_505"],
            info_other=json_dict["info_other"]
        )

config = new_config("config.json")
