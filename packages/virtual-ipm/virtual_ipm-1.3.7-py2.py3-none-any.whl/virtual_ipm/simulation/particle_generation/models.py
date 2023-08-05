# -*- coding: utf-8 -*-

#    Virtual-IPM is a software for simulating IPMs and other related devices.
#    Copyright (C) 2017  The IPMSim collaboration <http://ipmsim.gitlab.io/IPMSim>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This module provides components that model the particle generation process.
Models which incorporate ionization can refer to the sub-package :mod:`ionization` which
contains several related classes.
Models which incorporate gas motion can refer to the sub-package :mod:`gas_dynamics` which
contains several related classes.
"""

from __future__ import absolute_import, print_function, unicode_literals

import abc

from anna import Integer, PhysicalQuantity, String, Triplet, depends_on, parametrize
import injector
import numpy
import pandas
import scipy.constants as constants
import six

import virtual_ipm.di as di
from virtual_ipm.components import Model
from virtual_ipm.simulation.simulation import Progress

from .ionization.cross_sections import SimpleDDCS, VoitkivModel


# noinspection PyOldStyleClasses
class ParticleGenerationModel(Model):
    """
    (Abstract) Base class for particle generation models.

    A particle generation model represents a way of how particles enter the simulation cycle.
    For IPM simulations this most frequently incorporates the ionization process induced by
    the interaction of a beam with the rest gas. However other ways of generating particles are
    possible. For example for studying secondary electron emission emerging from ion impact on
    detector elements one would use a model which generates particles based on the output of
    a previous simulation which tracked the ions towards the detector.
    """

    CONFIG_PATH_TO_IMPLEMENTATION = 'ParticleGeneration/Model'
    CONFIG_PATH = 'ParticleGeneration/Parameters'

    def __init__(self, particle_supervisor, configuration=None):
        """
        Initialize the particle generation model.

        Parameters
        ----------
        particle_supervisor : :class:`ParticleSupervisor`
        configuration : :class:`ConfigurationAdaptor` derived class
        """
        super(ParticleGenerationModel, self).__init__(configuration)
        self._particle_supervisor = particle_supervisor

    def create_particle(self, progress, position=None, momentum=None):
        """
        Proxy method for creating a particle via  :method:`ParticleSupervisor.create_particle`.

        Parameters
        ----------
        progress : :class:`Progress`
        position : :class:`~numpy.ndarray` or list or tuple, optional
        momentum : :class:`~numpy.ndarray` or list or tuple, optional
        """
        return self._particle_supervisor.create_particle(
            progress, position=position, momentum=momentum
        )

    @abc.abstractmethod
    def generate_particles(self, progress):
        """
        Generate particles and set the initial values for position and momentum. This method
        must be implemented by particle generation models.

        Parameters
        ----------
        progress : :class:`Progress`
            The current simulation progress at which the particles are generated.
        """
        raise NotImplementedError

Interface = ParticleGenerationModel


# noinspection PyOldStyleClasses
@parametrize(
    Integer(
        'SimulationStep',
        info='The simulation step at which the particle will be created.',
        for_example=0
    ) >= 0,
    Triplet[PhysicalQuantity](
        'Position',
        unit='m',
        info='The position at which the particle will be created.',
        for_example=(0., 0., 0.)
    ).use_container(numpy.array),
    Triplet[PhysicalQuantity](
        'Velocity',
        unit='m/s',
        info='The velocity with which the particle will be created.',
        for_example=(0., 0., 0.)
    ).use_container(numpy.array)
)
class SingleParticle(ParticleGenerationModel):
    """
    This model creates a single particle at the specified simulation step with position and 
    velocity initially set to the specified parameters. This is particularly useful for testing
    setups and quickly observing a particle trajectory.
    """

    @injector.inject(
        configuration=di.components.configuration,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup
    )
    def __init__(self, configuration, particle_supervisor, setup):
        super(SingleParticle, self).__init__(particle_supervisor, configuration)
        self._mass = setup.particle_type.mass

    def generate_particles(self, progress):
        if progress.step == self._simulation_step:
            self.create_particle(progress, self._position, self._mass * self._velocity)


# noinspection PyOldStyleClasses
@parametrize(
    String('Filepath')
)
class DirectPlacement(ParticleGenerationModel):
    """
    This model allows for specifying a set of particles via their initial parameters and they will
    be created accordingly during the simulation. The file needs to be given as a CSV file with
    the following columns (the names need to match, position is arbitrary; don't include spaces in
    the names)::

        simulation step, x, y, z, vx, vy, vz

    Column delimiter is "," (comma). An arbitrary number of lines in this format may be given.
    Particles are created during the specified simulation step with the specified initial position
    and velocity.
    
    .. note::
       The first line is a header line and must reflect the above given column structure.
    
    .. warning::
       Only non-relativistic velocities are allowed.
    """

    # Use `list` and `dict` because in Python 2.x the order of keyword arguments is not preserved
    # (and so `OrderedDict(...)` will result in arbitrary column order).
    column_names = ['simulation step', 'x', 'y', 'z', 'vx', 'vy', 'vz']
    column_types = {'simulation step': int,
                    'x':  float, 'y':  float, 'z':  float,
                    'vx': float, 'vy': float, 'vz': float}

    @injector.inject(
        configuration=di.components.configuration,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup
    )
    def __init__(self, configuration, particle_supervisor, setup):
        super(DirectPlacement, self).__init__(particle_supervisor, configuration)
        self._mass = setup.particle_type.mass
        self._data_frame = pandas.read_csv(self._filepath, dtype=self.column_types)
        if set(self._data_frame.columns) != set(self.column_types):
            raise ValueError(
                'Input file must contain the following columns: {}'.format(self.column_names)
            )
        self._steps = self._data_frame['simulation step'].values

    def as_json(self):
        return super(DirectPlacement, self).as_json()

    def generate_particles(self, progress):
        to_be_generated_indices = numpy.argwhere(self._steps == progress.step).flatten()
        for index in to_be_generated_indices:
            position = self._data_frame.loc[index, ['x', 'y', 'z']].values
            momentum = self._data_frame.loc[index, ['vx', 'vy', 'vz']].values * self._mass
            self.create_particle(progress, position, momentum)


@parametrize(
    Integer(
        'BeamId',
        default=0,
        info='The beam which is "active" for ionization. Only this specified beam will ionize '
             'particles. Beams are numbered starting at 0 and incremented by 1 for each beam. '
             'Note that this only selects the beam for particle generation, the electromagnetic '
             'fields are still collected from all beams. If the results for ionization from '
             'multiple beams are required then this should be split over multiple runs of the '
             'simulation.'
    ) >= 0,
)
class IonizationModel(ParticleGenerationModel):
    """
    (Abstract) Base class for particle generation models which involve ionization.
    
    This class declares a parameter "BeamId". Particle generation through ionization should only
    involve one beam at a time and this parameter specifies the particular beam. Particle 
    generation from multiple beams should be split over multiple runs of the simulation.
    
    Beam ids start at 0 and are incremented by 1 for each other beam.
    """
    def __init__(self, beams, particle_supervisor, configuration):
        super(IonizationModel, self).__init__(particle_supervisor, configuration)

        try:
            self._beam = beams[self._beam_id]
        except IndexError:
            raise IndexError(
                'The specified beam id ({0}) exceeds the number of specified beams ({1}). '
                'Note that beam ids start at zero.'.format(
                    self._beam_id, len(beams)
                )
            )

    @abc.abstractmethod
    def generate_particles(self, progress):
        raise NotImplementedError


# noinspection PyOldStyleClasses
@parametrize(
    PhysicalQuantity('ZPosition', unit='m',
                     info='All particles will be created at this z-position in the lab frame. '
                          'The time at which they will be created depends on the longitudinal '
                          'offset of bunches to the specified position.')
)
class ZeroMomentum(IonizationModel):
    """
    This model generates all particles at a specific z-position with zero momentum (i.e. at rest).
    The transverse positions are sampled according to the Bunch's transverse charge distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup,
        configuration=di.components.configuration
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(ZeroMomentum, self).__init__(beams, particle_supervisor, configuration)
        self._setup = setup
        self._number_of_ionizations = setup.number_of_particles
        self._longitudinal_density_array = None
        self._n_particles_cache = {}

    def prepare(self):
        # noinspection PyUnresolvedReferences
        progresses = list(map(
            lambda step: Progress(step, self._setup.number_of_time_steps, self._setup.time_delta),
            six.moves.range(self._setup.number_of_time_steps)
        ))

        long_density_array = numpy.array(list(map(
            lambda progress: abs(self._beam.linear_charge_density_at(
                numpy.array(
                    [progress.time * constants.speed_of_light, 0., 0., self._z_position]
                )[:, numpy.newaxis],
                progress
            )),
            progresses
        ))).flatten()
        if numpy.sum(long_density_array) > 0.:
            long_density_array /= numpy.sum(long_density_array)
        else:
            self.log.warning(
                'Charge density of beam %s is zero at z=%e during the simulation time range',
                self._beam, self._z_position
            )
        self.log.debug('Longitudinal density array: %s', long_density_array.tolist())
        self._longitudinal_density_array = long_density_array

    def compute_number_of_particles_to_be_created(self, progress):
        # Need to cache result because the number of particles to be created is determined using
        # random number generation for the fractional part and because this function is called from
        # both position and momentum generation it could potentially lead to different numbers.
        if progress.step in self._n_particles_cache:
            return self._n_particles_cache[progress.step]

        n_particles = self._number_of_ionizations * self._longitudinal_density_array[progress.step]
        fraction = n_particles - int(n_particles)
        n_particles = int(n_particles) + (numpy.random.random() < fraction)

        self.log.debug(
            'Creating %s particles at step %d', n_particles, progress.step
        )
        self._n_particles_cache[progress.step] = n_particles
        return n_particles

    def generate_positions(self, progress):
        n_particles = self.compute_number_of_particles_to_be_created(progress)
        if not n_particles:
            return numpy.empty((0,))
        return self._beam.generate_positions_in_transverse_plane(
            progress, n_particles, self._z_position
        )

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def generate_momenta(self, progress):
        n_particles = self.compute_number_of_particles_to_be_created(progress)
        return numpy.zeros((3, n_particles), dtype=float)

    def generate_particles(self, progress):
        positions = self.generate_positions(progress)
        momenta = self.generate_momenta(progress)
        if positions.size == 0:
            assert momenta.size == 0, 'Momenta generated while no positions were generated'
            return
        # noinspection PyUnresolvedReferences
        for nr in six.moves.range(positions.shape[1]):
            self.create_particle(
                progress,
                position=positions[:, nr],
                momentum=momenta[:, nr]
            )


# noinspection PyOldStyleClasses
@depends_on(
    VoitkivModel
)
class VoitkivDDCS(ZeroMomentum):
    """
    This model generates all particles at a specific z-position with momenta sampled from the
    Voitkiv double differential cross section. The transverse positions are sampled according to
    the Bunch's transverse charge distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup,
        configuration=di.components.configuration
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(VoitkivDDCS, self).__init__(
            beams=beams,
            particle_supervisor=particle_supervisor,
            setup=setup,
            configuration=configuration
        )
        self._setup = setup
        self._longitudinal_density_array = None
        self._ionization_cross_section = VoitkivModel(
            self._beam,
            setup,
            configuration.get_configuration(self.CONFIG_PATH)
        )

    def as_json(self):
        return dict(
            super(VoitkivDDCS, self).as_json(),
            ionization_cross_section=self._ionization_cross_section.as_json()
        )

    def prepare(self):
        super(VoitkivDDCS, self).prepare()
        self._ionization_cross_section.prepare()

    def generate_momenta(self, progress):
        n_particles = self.compute_number_of_particles_to_be_created(progress)
        if not n_particles:
            return numpy.empty((0,))
        return self._ionization_cross_section.generate_momenta(n_particles)


# Inherits from ZZeroVoitkivMomentum because it already has the required ionization cross section
# functionality; we simply override the ionization cross sections as they all follow a common
# interface. However this abstract functionality could be moved to a separate class and enabled
# via multiple inheritance. Or alternatively insert this additional ionization cross section class
# above ZZeroVoitkivMomentum in the class hierarchy and make ZZeroGeneratorSimpleDDCS inherit from
# this class rather than from ZZeroVoitkivMomentum.
# noinspection PyOldStyleClasses
@depends_on(
    SimpleDDCS
)
class SimpleDDCS(VoitkivDDCS):
    """
    This model generates all particles at a specific z-position with momenta sampled from a
    decoupled double differential cross section (that is two independent single differential cross
    sections). The transverse positions are sampled according to the Bunch's transverse charge
    distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        configuration=di.components.configuration,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(SimpleDDCS, self).__init__(
            beams=beams,
            particle_supervisor=particle_supervisor,
            setup=setup,
            configuration=configuration
        )
        # Override the ionization cross sections here; the required generate_momenta functionality
        # is generally applicable and already available.
        self._ionization_cross_section = SimpleDDCS(
            setup,
            configuration.get_configuration(self.CONFIG_PATH)
        )

# Because ZZeroSimpleDDCS inherits from ZZeroVoitkivMomentum it retains the dependency on
# VoitkivModel which is not required in this case. Inheritance was applied only for obtaining
# functionality.
setattr(SimpleDDCS, '_depends_on_%s' % VoitkivModel.__name__, None)


@parametrize(
    PhysicalQuantity('Temperature', unit='K'),
    PhysicalQuantity('Mass', unit='kg', info='Rest mass of the gas particles.')
)
class ThermalMotion(ZeroMomentum):
    """
    This model can be used to incorporate the thermal motion of the rest gas. The rest gas is
    treated as an idealized gas and the velocity distribution is described by the Maxwell-Boltzmann
    distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup,
        configuration=di.components.configuration
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(ThermalMotion, self).__init__(
            beams=beams,
            particle_supervisor=particle_supervisor,
            setup=setup,
            configuration=configuration
        )
        self._scale = numpy.sqrt(
            constants.physical_constants['Boltzmann constant'][0]
            * self._temperature
            / self._mass
        )
        self._ionized_particle_mass = setup.particle_type.mass

    def generate_momenta(self, progress):
        n_particles = self.compute_number_of_particles_to_be_created(progress)
        if not n_particles:
            return numpy.empty((0,))

        return (
            numpy.random.normal(scale=self._scale, size=(3, n_particles))
            * self._ionized_particle_mass
        )


@parametrize(
    PhysicalQuantity('Velocity', unit='m/s'),
    PhysicalQuantity('TransverseTemperature', unit='K'),
    PhysicalQuantity('LongitudinalTemperature', unit='K'),
    PhysicalQuantity('Mass', unit='kg', info='Rest mass of the gas particles.')
)
class GasJet(ZeroMomentum):
    """
    This model can be used to simulate (supersonic) gas jets. The gas jet is treated as a
    two-dimensional curtain of homogeneous density which moves along the y-axis. The velocity of
    emerging particles are determined from the gas jet velocity as well as from the transverse and
    longitudinal velocity distributions which are described by the Maxwell-Boltzmann distribution.
    """

    @injector.inject(
        beams=di.components.beams,
        particle_supervisor=di.components.particle_supervisor,
        setup=di.components.setup,
        configuration=di.components.configuration
    )
    def __init__(self, beams, particle_supervisor, setup, configuration):
        super(GasJet, self).__init__(
            beams=beams,
            particle_supervisor=particle_supervisor,
            setup=setup,
            configuration=configuration
        )
        self._transverse_scale = numpy.sqrt(
            constants.physical_constants['Boltzmann constant'][0]
            * self._transverse_temperature
            / self._mass
        )
        self._longitudinal_scale = numpy.sqrt(
            constants.physical_constants['Boltzmann constant'][0]
            * self._longitudinal_temperature
            / self._mass
        )
        self._ionized_particle_mass = setup.particle_type.mass

    def generate_momenta(self, progress):
        n_particles = self.compute_number_of_particles_to_be_created(progress)
        if not n_particles:
            return numpy.empty((0,))

        return numpy.roll(
            numpy.concatenate((
                numpy.random.normal(
                    loc=self._velocity,
                    scale=self._longitudinal_scale,
                    size=(1, n_particles)
                ),
                numpy.random.normal(
                    scale=self._transverse_scale,
                    size=(2, n_particles)
                )
            )),
            # Gas jet moves along y-axis so we need to move the longitudinal velocities from
            # position 0 to position 1 on axis 0 (roll them 1 position forward).
            1, axis=0
        ) * self._ionized_particle_mass
