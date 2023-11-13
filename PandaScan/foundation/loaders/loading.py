import time


class LoadingBar:
    def __init__(self, emoji):
        self.emoji = emoji

    def start_load(self, duration=100):
        for i in range(duration):
            print(f"\rLoading {'.' * i}{self.emoji} ", end="")
            time.sleep(0.5)

    def end_load(self):
        print("\rCompleted ✅                                                             ")


loading = LoadingBar("🍃")

if __name__ == "__main__":
    loading.start_load(50)
    loading.end_load()
