from rich.console import Group
from rich.panel import Panel
from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


class ProgressManager:
    def __init__(self):
        # Progress bar for individual steps
        self.step_progress = Progress(
            TextColumn("  "),
            TimeElapsedColumn(),
            TextColumn("[bold purple]{task.fields[action]}"),
            SpinnerColumn("simpleDots"),
        )

        # Progress bar for app-level steps
        self.app_steps_progress = Progress(
            TextColumn(
                "[bold blue]Progress for app {task.fields[name]}: {task.percentage:.0f}%"
            ),
            BarColumn(),
            TextColumn("({task.completed} of {task.total} steps done)"),
        )

        # Overall progress bar
        self.overall_progress = Progress(
            TimeElapsedColumn(), BarColumn(), TextColumn("{task.description}")
        )

        # Group all progress bars
        self.progress_group = Group(
            Panel(Group(self.step_progress, self.app_steps_progress)),
            self.overall_progress,
        )

        self.live = None

    def start(self, total_apps):
        """Start the live progress display."""
        self.live = Live(self.progress_group, refresh_per_second=10)
        self.live.start()
        self.overall_task_id = self.overall_progress.add_task("", total=total_apps)

    def stop(self):
        """Stop the live progress display."""
        if self.live:
            self.live.stop()

    def add_app(self, app_name, total_steps):
        """Add a new app to the progress bar."""
        app_steps_task_id = self.app_steps_progress.add_task(
            "", total=total_steps, name=app_name
        )
        return app_steps_task_id

    def update_overall(self, description, advance=0):
        """Update the overall progress bar."""
        self.overall_progress.update(
            self.overall_task_id, description=description, advance=advance
        )

    def add_step(self, app_name, action):
        """Add a new step to the progress bar."""
        step_task_id = self.step_progress.add_task("", action=action, name=app_name)
        return step_task_id

    def complete_step(self, step_task_id):
        """Mark a step as complete."""
        self.step_progress.stop_task(step_task_id)
        self.step_progress.update(step_task_id, visible=False)

    def advance_app(self, app_steps_task_id):
        """Advance the app-level progress bar."""
        self.app_steps_progress.update(app_steps_task_id, advance=1)