from Point import Point


class FigureCircle:
    def __init__(self, algorithm, color, center: Point, r):
        self.r = r
        self.center = center
        self.algorithm = algorithm
        self.color = color
        self.points = self.get_points_to_draw()

    def get_points_to_draw(self):
        return self.algorithm(self.r, self.r, self.center)

    def __str__(self):
        return f'FigureCircle(r={self.r}, center={self.center} alg={self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.r == other.r and self.center == other.center


OK = 0
ERR_PARAM_COUNT = 1
ERR_PARAM = 2
ERR_BEG_END_R = 3
ERR_STEP = 4
ERRS_FIGURE = {
    ERR_PARAM_COUNT: 'Неверное количество параметров класса\n',
    ERR_PARAM: 'По заданным параметра нельзя построит спектр\n',
    ERR_BEG_END_R: 'Начальный радиус не может быть больше конечного или равен ему\n',
    ERR_STEP: 'Слишком большой шаг изменения радиуса\n'
}


class FigureCircleSpec:
    def __init__(self, algorithm, color, center, beg_r=0, end_r=0, step_r=0, count=0):
        self.algorithm = algorithm
        self.color = color
        self.center = center
        self.begr = beg_r
        self.endr = end_r
        self.stepr = step_r
        self.count = count
        self.need_circles = []
        self.err, self.points = self.get_points_to_draw()

    def get_need_circles(self, printing=False):
        if printing: print('\nget_need_circles:')
        if len([filter(lambda x: x == 0, [self.begr, self.endr, self.stepr, self.count])]) != 1:
            return ERR_PARAM_COUNT, []

        need_circles = list()
        if self.begr == 0:
            r = self.endr
            for i in range(self.count):
                if r <= 0:
                    return ERR_STEP, []

                need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                r -= self.stepr
        elif self.endr == 0:
            r = self.begr
            for i in range(self.count):
                need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                r += self.stepr
        elif self.stepr == 0:
            if self.begr >= self.endr:
                return ERR_BEG_END_R, []
            step = (self.endr - self.begr) / self.count
            r = self.begr
            for i in range(self.count - 1):
                need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                r += step
            need_circles.append(FigureCircle(self.algorithm, self.color, self.center, self.endr))
        elif self.count == 0:
            if self.begr >= self.endr:
                return ERR_BEG_END_R, []
            if self.stepr > self.endr - self.begr:
                return ERR_STEP, []

            r = self.begr
            while r <= self.endr:
                need_circles.append(FigureCircle(self.algorithm, self.color, self.center, r))
                r += self.stepr
        return OK, need_circles

    def get_points_to_draw(self):
        err, self.need_circles = self.get_need_circles()
        if err != OK:
            return err, []
        points = list()
        for circle in self.need_circles:
            points.extend(circle.points)
        return err, points

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
        self.points = self.get_points_to_draw()

    def get_points_to_draw(self):
        return self.algorithm(self.ra, self.rb, self.center)

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
        self.need_ellipse = []
        self.points = self.get_points_to_draw()

    def get_need_ellipse(self, printing=False):
        if printing: print('\nget_need_ellipse:')

        need_ellipse = list()
        ra, rb = self.beg_ra, self.beg_rb
        for i in range(self.count):
            need_ellipse.append((FigureEllipse(self.algorithm, self.color, self.center, ra, rb)))
            ra += self.step_ra
            rb += self.step_rb

        return need_ellipse

    def get_points_to_draw(self):
        self.need_ellipse = self.get_need_ellipse()
        points = list()
        for ellipse in self.need_ellipse:
            points.extend(ellipse.points)
        return points

    def __str__(self):
        return f'FigureEllipseSpec(' \
               f'beg_ra={self.beg_ra}, beg_rb={self.beg_rb}, ' \
               f'step_ra={self.step_ra}, step_rb={self.step_rb}, count={self.count}, ' \
               f'{self.algorithm.__name__}, color={self.color.name()})'

    def __repr__(self):
        return self.__str__()
