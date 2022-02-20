import json

import click

import models
import solvers as s

import sys
# from IPython.core import ultratb

# sys.excepthook = ultratb.FormattedTB(
#     color_scheme="Linux", call_pdb=1
# )


@click.command()
@click.argument("infile", type=click.File("r"))
@click.argument("outfile", type=click.File("w"))
@click.argument("metafile", type=click.File("w"))
@click.argument("best_solution", type=click.File("w"), required=False)
def main(infile, outfile, metafile, best_solution):
    problem = models.Problem.parse(infile)

    solvers = [
        # TODO: Add other solvers or alternative configurations here
        s.Naive(),
        s.LikesGTDislikes(),
        s.LikesGTDislikes2()
    ]

    best, *others = sorted(
        [solver.solve(problem) for solver in solvers],
        key=lambda s: s.score,
        reverse=True,
    )

    max_score = problem.get_max_score()

    click.echo(f"Best: {best.solver}, {best.score} / {max_score} ({int(100 * best.score / max_score)}%)")

    for solver in others:
        click.echo(f" - {solver.solver}, {solver.score} / {max_score} ({int(100 * solver.score / max_score)}%)")

    best.write(outfile)
    json.dump({"score": best.score}, metafile)


if __name__ == "__main__":
    main()
