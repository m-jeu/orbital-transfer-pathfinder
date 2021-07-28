class LoadingBarError(Exception):
    """Exception to help point the user towards incorrect LoadingBar usage."""
    def __init__(self):
        super().__init__("Loading bar increments exceeded capacity.")


# FIXME(m-jeu): Probably not terribly efficient, but doesn't really matter because it's just a loading bar.
class LoadingBar:
    """Simple 10-segment progress bar to visualize progress.

    Attributes:
        steps: the total amount of steps required to complete the process.
        current: the current amount of steps completed towards the process.
        threshholds: the numbers at which the progress bar should visualize progress.
        visual_completed: the amount of segments (out of 10) the progress bar has visually completed."""

    def __init__(self, steps: int):
        """Initialize instance with steps, current, threshholds, visual_completed.
        Also call self.visualize()."""
        self.steps: int = steps
        self.current: int = 0
        self.threshholds: list[int] = []
        self.visual_completed: int = 0
        for i in range(1, 11):
            self.threshholds.append(round((i * 0.1) * steps))
        self.visualize()

    def increment(self):
        """Increment the amount of completed steps by 1.
        Call self.visualize() if threshhold in self.threshholds is passed."""
        self.current += 1
        if self.current > self.steps:
            raise LoadingBarError()
        while self.current >= self.threshholds[0]:
            self.visual_completed += 1
            self.visualize()
            if len(self.threshholds) == 1:
                break
            self.threshholds.pop(0)

    def visualize(self):
        """Visualize the current state of the progress bar."""
        print(f"[{'*' * self.visual_completed}{' ' * (10 - self.visual_completed)}] ({self.current}/{self.steps})")
