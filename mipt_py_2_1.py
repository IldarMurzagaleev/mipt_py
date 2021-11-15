import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = 'car'


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__(brand, photo_file_name, carrying)
        b_l, b_w, b_h = self.parse_lwh(body_lwh)
        self.body_length = b_l
        self.body_width = b_w
        self.body_height = b_h
        self.car_type = 'truck'

    @staticmethod
    def parse_lwh(body_lwh):
        res_lwh = [0.0, 0.0, 0.0]
        if body_lwh != '':
            parts = body_lwh.split('x')
            if len(parts) == 3:
                for i, part in enumerate(parts):
                    if isfloat(part):
                        res_lwh[i] = float(part)
        return res_lwh

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            flag = False
            if len(row) == 7 and row[0] != '':
                brand = row[1]
                photo_file_name = row[3]
                carrying = row[5]
                if brand and is_correct(photo_file_name) and isfloat(carrying):
                    flag = True
                if row[0] == 'car':
                    passenger_seats_count = row[2]
                    if isfloat(passenger_seats_count) and flag:
                        car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))
                elif row[0] == 'truck':
                    body_lwh = row[4]
                    if flag:
                        car_list.append(Truck(brand, photo_file_name, carrying, body_lwh))
                elif row[0] == 'spec_machine':
                    extra = row[6]
                    if extra and flag:
                        car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))
        return car_list


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_correct(filename):
    parts = filename.split('.')
    if len(parts) == 2 and parts[0] and parts[1]:
        return True
    else:
        return False
