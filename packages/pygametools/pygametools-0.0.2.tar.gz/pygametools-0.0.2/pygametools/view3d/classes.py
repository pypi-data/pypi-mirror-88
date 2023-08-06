#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame
import numpy
from math import pi, radians, sqrt, sin, cos, atan


class CameraOrtho:
    def __init__(self, angle=(0, 0, 0), size=5, offset=(0, 0)):
        """
        Initializes camera.
        :param angle: Angle of the camera in (latitude, longitude, roll)
        :type angle: Tuple[float, float, float]
        :param size: Orthographic X size of camera.
        :type size: float
        :param offset: Offset of camera in (x, y)
        :type offset: Tuple[float, float]
        """
        self.angle = angle
        self.size = size
        self.offset = offset

    def render(self, mesh, res, bg_col, matcap=None):
        """
        Renders a mesh.
        :param mesh: Mesh to render.
        :type mesh: pygametools.view3d.Mesh
        :param res: Resolution
        :type res: Tuple[int, int]
        :param bg_col: Background color of render in (R, G, B, [A])
        :type bg_col: Tuple[int]
        :param matcap: Material capture to render.
        :type matcap: pygame.Surface
        """
        surface = pygame.Surface(res, pygame.SRCALPHA)
        surface.fill(bg_col)

        for face in mesh.prepare_render():
            normal = self._calc_pixel(self._calc_normal(face))
            if matcap is None:
                color = (128, 128, 128)
            else:
                color = matcap.get_at(normal[0])
            
            if normal[1]:
                locations = []
                for vert in face:
                    locations.append(self._project(vert, res))

                pygame.draw.polygon(surface, color, locations)
        
        return surface

    def _project(self, vert, res):
        size_hor = self.size
        size_ver = self.size / res[0] * res[1]
        loc_x, loc_y, loc_z = vert
        view_ver = radians(self.angle[0])
        view_hor = radians(self.angle[1])

        px_hor = loc_x*cos(view_hor) + loc_y*sin(view_hor)
        px_hor *= res[0] / size_hor
        px_hor += res[0] / 2
        px_hor -= self.offset[0]

        px_ver = loc_z*sin(view_ver) - loc_x*sin(view_hor)*cos(view_ver) + loc_y*cos(view_hor)*cos(view_ver)
        px_ver *= res[1] / size_ver
        px_ver += res[1] / 2
        px_ver -= self.offset[1]

        return (px_hor, px_ver)

    def _calc_normal(self, verts):
        p1, p2, p3 = map(numpy.array, verts)
        direction = numpy.cross((p2 - p1), (p3 - p1))
        return direction / len(direction)

    def _calc_pixel(self, normal, dim):
        theta = atan(normal[0] / normal[2])
        radius = -2 * atan(abs(normal[1])) / pi + 1
        return ((int(radius*dim*sin(theta)), int(radius*dim*cos(theta))), True)


class Mesh:
    def __repr__(self):
        return f"Mesh with {len(self.faces)} faces"

    def parse_faces(self, faces, verts):
        self.faces = []
        for face in faces:
            curr_face = []
            for index in face:
                curr_face.append(verts[index])
            self.faces.append(curr_face)

        return self

    def prepare_render(self):
        """
        Returns a list that the renderer can understand. This should only be called by the renderer.
        """
        faces = []
        for face in self.faces:
            if len(face) == 3:
                faces.append(face)
            else:
                for vert in range(1, len(face)-1):
                    faces.append((face[0], face[vert], face[vert+1]))

        return faces