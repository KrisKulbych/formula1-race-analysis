import click

from display import generate_report


@click.group()
def f1_racing_results() -> None:
    pass


f1_racing_results.add_command(generate_report)


if __name__ == "__main__":
    f1_racing_results()
