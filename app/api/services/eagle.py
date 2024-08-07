import threading
from app.core.config import settings
from watchdog.observers import Observer
from app.api.services.multiplexer import HLSStreaming
from watchdog.events import FileSystemEventHandler, FileSystemEvent


def generate_hls_stream(file):
    HLSStreaming(file).generate_stream()


class HeartBeat(FileSystemEventHandler):
    # def on_modified(self, event: FileSystemEvent) -> None:
    #     print(f"File modify - {event.src_path}")

    def on_created(self, event: FileSystemEvent) -> None:
        print(f"File Created - {event.src_path}")
        if event.src_path.endswith(".mp4"):
            print("Generating HLS stream")
            generate_stream = threading.Thread(target=generate_hls_stream, name="Streaming", kwargs={'file': event.src_path})
            generate_stream.start()

    # def on_deleted(self, event: FileSystemEvent) -> None:
    #     pass


path = str(settings.BASE_PATH.joinpath('uploads/'))
event_handler = HeartBeat()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)


def system_heart_beat(status=None):
    if status:
        observer.start()
    else:
        observer.stop()
