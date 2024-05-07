from Point import Point
from errs import *


class FigureCircle:
    def __init__(self, algorithm, color, center: Point, r):
        self.r = r
        self.center = center
        self.algorithm = algorithm
        self.color = color
        # self.points = self.get_points_to_draw()

    def draw(self, canvas):
        self.algorithm(self.r, self.r, self.center, canvas, self.color, True)

    # def get_points_to_draw(self):
    #     return self.algorithm(self.r, self.r, self.center)

    def __str__(self):
        return f'FigureCircle(r={self.r}, center={self.center} alg={self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.r == other.r and self.center == other.center


class FigureCircleSpec:
    def __init__(self, algorithm, color, center, beg_r=0, end_r=0, step_r=0, count=0):
        self.algorithm = algorithm
        self.color = color
        self.center = center
        self.begr = beg_r
        self.endr = end_r
        self.stepr = step_r
        self.count = count
        # self.need_circles = []
        # self.err, self.points = self.get_points_to_draw()

    def draw(self, canvas, printing=False): # -> ERR
        if printing: print('\nget_need_circles:')
        if len([filter(lambda x: x == 0, [self.begr, self.endr, self.stepr, self.count])]) != 1:
            raise ErrParamCount

        # need_circles = list()
        if self.begr == 0:
            r = self.endr
            for i in range(self.count):
                if r <= 0:
                    raise ErrStep

                # need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                FigureCircle(self.algorithm, self.color, self.center, r).draw(canvas)
                r -= self.stepr
        elif self.endr == 0:
            r = self.begr
            for i in range(self.count):
                # need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                FigureCircle(self.algorithm, self.color, self.center, r).draw(canvas)
                r += self.stepr
        elif self.stepr == 0:
            if self.begr >= self.endr:
                raise ErrBegEndRadius
            step = (self.endr - self.begr) / self.count
            r = self.begr
            for i in range(self.count - 1):
                # need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                FigureCircle(self.algorithm, self.color, self.center, r).draw(canvas)
                r += step
            # need_circles.append(FigureCircle(self.algorithm, self.color, self.center, self.endr))
            FigureCircle(self.algorithm, self.color, self.center, self.endr).draw(canvas)
        elif self.count == 0:
            if self.begr >= self.endr:
                raise ErrBegEndRadius
            if self.stepr > self.endr - self.begr:
                raise ErrStep

            r = self.begr
            while r <= self.endr:
                # need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                FigureCircle(self.algorithm, self.color, self.center, r).draw(canvas)
                r += self.stepr
        # return OK, need_circles

    # def get_points_to_draw(self):
    #     err, self.need_circles = self.get_need_circles()
    #     if err != OK:
    #         return err, []
    #     points = list()
    #     for circle in self.need_circles:
    #         points.extend(circle.points)
    #     return err, points

    def __str__(self):
        return f'FigureCircleSpec(' \
               f'beg_r={self.begr}, end_r={self.endr}, step_r={self.stepr}, count={self.count}, ' \
               f'{self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()


class FigureEllipse:
    def __init__(self, algorithm, color, center: Point, ra, rb):
        self.ra = ra
        self.rb = rb
        self.center = center
        self.algorithm = algorithm
        self.color = color
        # self.points = self.get_points_to_draw()

    # def get_points_to_draw(self):
    #     return self.algorithm(self.ra, self.rb, self.center)

    def draw(self, canvas):
        self.algorithm(self.ra, self.rb, self.center, canvas, self.color, True)

    def __str__(self):
        return f'FigureEllipse(ra={self.ra}, rb={self.rb}, center={self.center} alg={self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.ra == other.ra and self.rb == other.rb and self.center == other.center


class FigureEllipseSpec:
    def __init__(self, algorithm, color, center, beg_ra, beg_rb, step_ra, step_rb, count):
        self.algorithm = algorithm
        self.color = color
        self.center = center
        self.beg_ra, self.beg_rb = beg_ra, beg_rb
        self.step_ra, self.step_rb = step_ra, step_rb
        self.count = count
        # self.need_ellipse = []
        # self.points = self.get_points_to_draw()

    def draw(self, canvas, printing=False):
        if printing: print('\nget_need_ellipse:')

        # need_ellipse = list()
        ra, rb = self.beg_ra, self.beg_rb
        for i in range(self.count):
            # need_ellipse.append((FigureEllipse(self.algorithm, self.color, self.center, ra, rb)))
            FigureEllipse(self.algorithm, self.color, self.center, ra, rb).draw(canvas)
            ra += self.step_ra
            rb += self.step_rb

        # return need_ellipse

    # def get_points_to_draw(self):
    #     self.need_ellipse = self.get_need_ellipse()
    #     points = list()
    #     for ellipse in self.need_ellipse:
    #         points.extend(ellipse.points)
    #     return points

    def __str__(self):
        return f'FigureEllipseSpec(' \
               f'beg_ra={self.beg_ra}, beg_rb={self.beg_rb}, ' \
               f'step_ra={self.step_ra}, step_rb={self.step_rb}, count={self.count}, ' \
               f'{self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()
