def transform(self, x, y):
    # return self.transform_2d(x, y)
    return self.transform_perspective(x, y)


def transform_2d(self, x, y):
    return int(x), int(y)


def transform_perspective(self, x, y):
    lin_y = y * self.perspective_y / self.height
    if lin_y > self.perspective_y:
        lin_y = self.perspective_y

    diff_x = x - self.perspective_x
    diff_y = self.perspective_y - lin_y

    factor_y = diff_y / self.perspective_y
    factor_y = pow(factor_y, 4)

    tr_x = self.perspective_x + diff_x * factor_y
    tr_y = self.perspective_y - factor_y * self.perspective_y

    return int(tr_x), int(tr_y)
