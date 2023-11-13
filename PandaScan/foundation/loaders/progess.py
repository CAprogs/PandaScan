import time
import sys


class ProgressBar:
    def __init__(self, total, length=50, fill='#'):
        self.total = total
        self.length = length
        self.fill = fill
        self.progress = 0
        self.start_time = time.perf_counter()

    def reset(self):
        self.progress = 0
        self.start_time = time.perf_counter()

    def update(self, progress):
        self.progress = progress
        if self.progress > self.total:
            self.progress = self.total

    def display(self, prefix='Progress:', suffix='Complete'):
        percent = float(self.progress) / float(self.total)
        fill_length = int(self.length * percent)
        bar_fill = self.fill * fill_length
        bar_empty = ' ' * (self.length - fill_length)
        bar = bar_fill + bar_empty

        elapsed_time = time.perf_counter() - self.start_time
        eta = round(elapsed_time / percent * (1 - percent), 2)

        print('\r%s |%s| %s%% %s (ETA: %s)' % (prefix, bar, round(percent * 100, 2), suffix, eta), end='\r')
        sys.stdout.flush()
        if self.progress == self.total:
            print()


if __name__ == '__main__':
    tour_length = 10
    a = 0

    progress_bar = ProgressBar(tour_length)

    for i in range(tour_length):
        a += 1
        progress_bar.update(a)
        progress_bar.display()
        time.sleep(1)
