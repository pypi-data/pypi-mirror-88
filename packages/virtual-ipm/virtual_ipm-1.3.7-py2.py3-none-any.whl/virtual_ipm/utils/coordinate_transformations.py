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

from __future__ import absolute_import, unicode_literals

import numpy
from scipy.constants import physical_constants


_SPEED_OF_LIGHT = physical_constants['speed of light in vacuum'][0]


class CoordinateTransformation(object):
    def __init__(self):
        super(CoordinateTransformation, self).__init__()


class LorentzTransformation(CoordinateTransformation):
    def __init__(self, transformation_matrix):
        super(LorentzTransformation, self).__init__()
        self.transformation_matrix = transformation_matrix

    def apply(self, tensor):
        return self.transformation_matrix.dot(tensor)


class LorentzBoost(LorentzTransformation):
    def __init__(self, beta_vector):
        beta = numpy.linalg.norm(beta_vector)
        gamma = 1. / numpy.sqrt((1. + beta) * (1. - beta))
        nx, ny, nz = beta_vector / beta
        super(LorentzBoost, self).__init__(numpy.array(
            [
                [gamma,          -gamma*beta*nx,          -gamma*beta*ny,          -gamma*beta*nz],
                [-gamma*beta*nx, 1. + (gamma - 1.)*nx**2, (gamma - 1.)*nx*ny,      (gamma - 1.)*nx*nz],
                [-gamma*beta*ny, (gamma - 1.)*nx*ny,      1. + (gamma - 1.)*ny**2, (gamma - 1.)*ny*nz],
                [-gamma*beta*nz, (gamma - 1.)*nx*nz,      (gamma - 1.)*ny*nz,      1. + (gamma - 1.)*nz**2],
            ]
        ))


class LorentzBoostAlongZ(LorentzBoost):
    def __init__(self, beta_z):
        super(LorentzBoostAlongZ, self).__init__(numpy.array([0., 0., beta_z]))
        self.beta = numpy.abs(beta_z)
        self.gamma = 1. / numpy.sqrt((1. + self.beta) * (1. - self.beta))

    def apply(self, vector):
        return numpy.array([
            self.gamma * (vector[0] - self.beta*vector[3]),
            vector[1],
            vector[2],
            self.gamma * (vector[3] - self.beta*vector[0])
        ])


class LorentzBoostAlongZForElectricField(LorentzBoostAlongZ):
    def __init__(self, beta_z):
        super(LorentzBoostAlongZForElectricField, self).__init__(beta_z)

    def apply(self, tensor):
        """Transform electric field assuming that magnetic field is zero.

        Calculation in SI units.

        :param tensor: numpy.ndarray of shape (3, N) representing the electric field
        :return: tuple where the first component is the transformed electric field and the second component is the
                 transformed magnetic field
        """
        e_field = numpy.array([
            self.gamma * tensor[0],
            self.gamma * tensor[1],
            tensor[2]
        ])
        b_field = numpy.stack((
            -(self.beta * self.gamma * tensor[1]),
            self.beta * self.gamma * tensor[0],
            numpy.zeros(tensor.shape[1], dtype=float)
        )) / _SPEED_OF_LIGHT
        return e_field, b_field
