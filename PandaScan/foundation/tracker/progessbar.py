import time
import sys


class ProgressBar:
    """Creates a progress bar that can be updated and displayed in the console.
    """
    def __init__(self, total, length=50, fill='█'):
        self.total = total
        self.length = length
        self.fill = fill
        self.progress = 0
        self.start_time = time.perf_counter()

    def reset(self):
        self.progress = 0
        self.start_time = time.perf_counter()

    def update(self, progress):
        """Update the progress bar.

        Args:
            progress (int): the current progress
        """
        self.progress = progress
        if self.progress > self.total:
            self.progress = self.total

    def display(self, prefix='Progress:', suffix='Completed'):
        """Display the progress bar.

        Args:
            prefix (str, optional): name of the progress bar displayed. Defaults to 'Progress:'.
            suffix (str, optional): displayed when the progress bar is finished. Defaults to 'Complete'.
        """
        percent = float(self.progress) / float(self.total)
        fill_length = int(self.length * percent)
        bar_fill = self.fill * fill_length
        bar_empty = ' ' * (self.length - fill_length)
        bar = bar_fill + bar_empty

        elapsed_time = time.perf_counter() - self.start_time
        eta = round(elapsed_time / percent * (1 - percent), 2)
        print('\r%s |%s| %s%% %s (ETA: %s)' % (f"{prefix} [{self.progress}/{self.total}]", bar, round(percent * 100, 2), suffix, eta), end='\r')
        sys.stdout.flush()
        if self.progress == self.total:
            print()
