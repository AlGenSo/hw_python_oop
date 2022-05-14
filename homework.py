class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
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

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Калории просят огня, ' % (self.__class__.__name__)
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


class Running(Training):
    """Тренировка: бег."""

    SPEED_MULTIPLIER = 18
    SUBTRACTED_CONSTANT = 20
    MINUTES_PER_HOUR = 60

    def get_spent_calories(self) -> float:
        '''Расчёт количества потраченных калорий за тренировку'''
        return (
            (self.SPEED_MULTIPLIER
             * Training.get_mean_speed(self)
             - self.SUBTRACTED_CONSTANT)
            * self.weight / self.M_IN_KM
            * self.duration
            * self.MINUTES_PER_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTUPLIER_1 = 0.035
    WEIGHT_MULTUPLIER_2 = 0.029
    MINUTES_PER_HOUR = 60

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
        '''Расчёт количества потраченных калорий за тренировку'''
        return (
            (self.WEIGHT_MULTUPLIER_1
             * self.weight
             + (Training.get_mean_speed(self) ** 2
                // self.height)
             * self.WEIGHT_MULTUPLIER_2 * self.height)
            * self.duration * self.MINUTES_PER_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SUMMAND_AVERAGE_SPEED = 1.1
    SUMM_MULTIPLIER = 2

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
        '''Расчёт средней скорости'''
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        '''Расчёт количества потраченных калорий за тренировку'''
        return (
            (self.get_mean_speed()
             + self.SUMMAND_AVERAGE_SPEED)
            * self.SUMM_MULTIPLIER
            * self.weight
        )


'''Инициализируем словарь как константу'''
DICT_WORKOUT = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in DICT_WORKOUT:
        raise ValueError(
            f'Тип тренировки {workout_type} отсутствует'
        )
    else:
        return DICT_WORKOUT[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
