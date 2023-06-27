"""Домашнее задание по ООП"""
from dataclasses import dataclass

__author__ = "ml.leskov"


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Принтит сообщение о тренировке"""
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.;"
            f" Дистанция: {self.distance:.3f} км;"
            f" Ср. скорость: {self.speed:.3f} км/ч;"
            f" Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:  # type: ignore
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить расход калорий при беге.

        Notes:
            (18 * средняя_скорость + 1.79) * вес_спортсмена /
            M_IN_KM * время_тренировки_в_минутах"""
        return (
               (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить расход калорий при ходьбе.

        Notes:
            ((0.035 * вес + (средняя_скорость_в_метрах_в_секунду**2
            / рост_в_метрах)* 0.029 * вес) * время_тренировки_в_минутах)
        """

        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
               / (self.height / self.CM_IN_M))
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить расход калорий при плавини.

        Notes:
            (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        """
        return (
               ((self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)
                + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


DICT_TYPE = {"SWM": Swimming,
             "RUN": Running,
             "WLK": SportsWalking}


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return DICT_TYPE[workout_type](*data)
    except KeyError:
        print(f'Тип тренировки {workout_type} не найдет')


def main(training: Training) -> None:
    """Главная функция."""
    return print(training.show_training_info().get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
        ("WL", [9000, 1, 75, 180])
    ]

    for workout, workout_data in packages:
        training_kind = read_package(workout, workout_data)
        if not training_kind:
            continue
        main(training_kind)
