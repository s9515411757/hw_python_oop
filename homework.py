from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вернуть текст сообщения"""
        return self.INFO_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.one_step = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIE_RATIO_1: int = 18
    CALORIE_RATIO_2: int = 20

    def __init__(self, action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        c_1 = self.CALORIE_RATIO_1
        c_2 = self.CALORIE_RATIO_2
        average_speed = self.get_mean_speed()
        weight = self.weight
        m_in_km = self.M_IN_KM
        m_in_h = self.MIN_IN_HOUR
        dur = self.duration
        return (c_1 * average_speed - c_2) * weight / m_in_km * dur * m_in_h


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.calorie_ratio_1: float = 0.035
        self.calorie_ratio_2: float = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        d_min = self.duration * self.MIN_IN_HOUR
        calorie_ratio_1 = self.calorie_ratio_1
        calorie_ratio_2 = self.calorie_ratio_2
        weight = self.weight
        height = self.height
        a_speed = self.get_mean_speed()

        return ((calorie_ratio_1 * weight +
                 (a_speed**2 // height)
                 * calorie_ratio_2 * weight) * d_min)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.calorie_ratio_1: float = 1.1
        self.calorie_ratio_2: int = 2

    def get_distance(self) -> float:
        """Получить дистанцию в км, которую преодолел спортсмен."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_spent_calories(self) -> float:
        """Получить количество израсходованных калорий."""
        a_speed = self.get_mean_speed()
        c_1 = self.calorie_ratio_1
        c_2 = self.calorie_ratio_2

        return (a_speed + c_1) * c_2 * self.weight

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        length_pool = self.length_pool
        count_pool = self.count_pool
        m_in_km = self.M_IN_KM
        duration = self.duration

        return length_pool * count_pool / m_in_km / duration


def read_package(workout_type: str, *data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code: dict[str, type(Training)] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    try:
        return training_code[workout_type](data)
    except KeyError as error:
        print(f"Некорректный пакет: {error}")


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)