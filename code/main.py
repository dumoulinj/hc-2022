import json

import click

import models
import solver as s

import sys
# from IPython.core import ultratb

# sys.excepthook = ultratb.FormattedTB(
#     color_scheme="Linux", call_pdb=1
# )


@click.command()
@click.argument("infile", type=click.File("r"))
@click.argument("outfile", type=click.File("w"))
@click.argument("metafile", type=click.File("w"))
def main(infile, outfile, metafile):
    problem = models.Problem.parse(infile)

    solvers = [
        # TODO: Add other solvers or alternative configurations here
        s.Naive(),
        #s.Star(),
        #s.Jammed(),
        #s.Checkmate()
    ]

    best, *others = sorted(
        [solver.solve(problem) for solver in solvers],
        key=lambda s: s.score,
        reverse=True,
    )

    click.echo(f"Best: {best.solver}, {best.score}")

    for solver in others:
        click.echo(f" - {solver.solver}, {solver.score}")

    best.write(outfile)
    json.dump({"score": best.score}, metafile)


if __name__ == "__main__":
    main()
