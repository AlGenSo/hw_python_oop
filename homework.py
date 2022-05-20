from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Sequence, Tuple, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    INFO: ClassVar[str] = (
        'Тип тренировки: {training_type:}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Сообщение с типом тренировки и данными"""
        return self.INFO.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MINUTES_PER_HOUR: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Калории просят огня! '
            'Переопределите метод в наследнике - {self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    SPEED_MULTIPLIER: ClassVar[int] = 18
    SUBTRACTED_SPEED: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Расчёт количества потраченных калорий за тренировку"""
        return (
            (self.SPEED_MULTIPLIER
             * self.get_mean_speed()
             - self.SUBTRACTED_SPEED)
            * self.weight / self.M_IN_KM
            * self.duration
            * self.MINUTES_PER_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTUPLIER_1 = 0.035
    WEIGHT_MULTUPLIER_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:

        super().__init__(action,
                         duration,
                         weight,
                         )
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчёт количества потраченных калорий за тренировку"""
        return (
            (self.WEIGHT_MULTUPLIER_1
             * self.weight
             + (self.get_mean_speed() ** 2
                // self.height)
             * self.WEIGHT_MULTUPLIER_2 * self.height)
            * self.duration * self.MINUTES_PER_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    SUMMAND_AVERAGE_SPEED = 1.1
    WIGHT_MULTIPLIER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости"""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Расчёт количества потраченных калорий за тренировку"""
        return (
            (self.get_mean_speed()
             + self.SUMMAND_AVERAGE_SPEED)
            * self.WIGHT_MULTIPLIER
            * self.weight
        )


# Инициализируем словарь как константу
WORKOUTS: Dict[str, Tuple[Type[Training], int]] = {
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4),
    'SWM': (Swimming, 5),
}


def read_package(workout_type: str, data: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUTS:

        raise ValueError(
            f'Тип тренировки {workout_type} отсутствует'
        )
    workout, count_args = WORKOUTS.get(workout_type)
    if count_args != len(data):

        raise ValueError(
            'Количество аргументов {workout_type} '
            'для класса {workout} '
            'не соответствует требованиям!'
        )

    return workout(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
