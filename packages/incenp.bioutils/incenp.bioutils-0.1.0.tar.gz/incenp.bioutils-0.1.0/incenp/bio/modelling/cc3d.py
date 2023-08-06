# -*- coding: utf-8 -*-
# Incenp.Bioutils - Incenp.org's utilities for computational biology
# Copyright © 2020 Damien Goutte-Gattat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Wrapper to run parameterized CC3D simulations."""

from json import load, dump
from os import getenv, mkdir
from os.path import dirname, exists, join
from subprocess import run
from time import sleep

import click


@click.command()
@click.argument('simfile', type=click.Path(exists=True))
@click.option('--cc3d-home', '-C', default='/opt/cc3d',
              type=click.Path(file_okay=False, dir_okay=True, exists=True),
              help="Path to the CC3D install directory.")
@click.option('--output-dir', '-o',
              default='{}/cc3d-runs'.format(getenv('HOME', default='.')),
              type=click.Path(file_okay=False, dir_okay=True),
              help="Path to the output directory.")
@click.option('--runs', '-n', default=10, help="Number of runs to perform.")
@click.option('--parameters', '-p', type=click.Path(exists=True),
              help="Path to a parameter file.")
def main(simfile, cc3d_home, output_dir, runs, parameters):
    """Run CC3D simulations."""

    simdir = dirname(simfile)
    paramfile = join(simdir, 'Simulation', 'parameters.json')
    cc3dbin = join(cc3d_home, 'runScript.sh')

    if not exists(cc3dbin):
        raise click.ClickException(f"CC3d script runner {cc3dbin} not found.")

    command = [
            cc3dbin,
            '-i', simfile,
            '--current-dir', simdir,
            '-o', output_dir
            ]

    if parameters:
        with open(parameters, 'r') as f:
            try:
                parameters = load(f)
            except Exception as e:
                raise click.ClickException(f"Cannot parse param file: {e}")
    else:
        parameters = [{}]

    try:
        if not exists(output_dir):
            mkdir(output_dir)
        for parameter_set in parameters:
            with open(paramfile, 'w') as f:
                dump(parameter_set, f)

            for _ in range(runs):
                run(command)
                sleep(2)
    except Exception as e:
        raise click.ClickException(f"Cannot run simulation: {e}")


if __name__ == '__main__':
    main()
