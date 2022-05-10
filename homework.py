class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
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
    """Базовый класс тренировки."""#Добавляю атрибуты класса
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
        Dist = self.action*self.LEN_STEP/self.M_IN_KM
        return Dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        Dist = self.action*self.LEN_STEP/self.M_IN_KM
        aver_Speed:float = Dist/self.duration
        return aver_Speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_Message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(), 
                                   self.get_mean_speed(),
                                   self.get_spent_calories())     
        return info_Message


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, 
                 action: int, 
                 duration: float, 
                 weight: float, 
                 ) -> None:
        #наследуем функциональность конструктора из класса-родителя
        super().__init__(action, 
                         duration, 
                         weight, 
                         )

    #метод расчёта калорий 
    def get_spent_calories(self) -> float:
        
        COEF_CAL_RUN_1 = 18
        COEF_CAL_RUN_2 = 20
        aver_Speed_Run = Training.get_mean_speed(self)
        time_Train_min_Run = self.duration*60
        #Назначение переменной формулы расчёта калорий при беге
        Cal_calculation_Run: float = ((COEF_CAL_RUN_1 * float(aver_Speed_Run) - COEF_CAL_RUN_2)
                        *self.weight / self.M_IN_KM * time_Train_min_Run)
        return Cal_calculation_Run

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int, 
                 duration: float, 
                 weight: float,
                 height: float, #дополнительный параметр height — рост спортсмена. 
                 ) -> None:
        #наследуем функциональность конструктора из класса-родителя
        super().__init__(action, 
                         duration, 
                         weight, 
                         )
        self.height = height

    #метод расчёта калорий 
    def get_spent_calories(self) -> float:
        
        COEF_CAL_SpWalk_1 = 0.035
        COEF_CAL_SpWalk_2 = 0.029
        aver_Speed_SpWak = Training.get_mean_speed(self)
        time_Train_min_SpWalk = self.duration*60
        #Назначение переменной формулы расчёта калорий при спортивной ходьбе
        Cal_calculation_SpWalk: float = ((COEF_CAL_SpWalk_1*self.weight+(aver_Speed_SpWak**2//self.height)
                                  *COEF_CAL_SpWalk_2*self.height)*time_Train_min_SpWalk)
        return Cal_calculation_SpWalk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    def __init__(self,
                 action: int, 
                 duration: float, 
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 LEN_STEP: float = 1.38 
                 ) -> None:
        super().__init__(action, 
                         duration, 
                         weight, 
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = LEN_STEP
    #расчёт средней скорости <<длина_бассейна * count_pool / M_IN_KM / время_тренировки>>
    def get_mean_speed(self) -> float:

        aver_Speed_Swim_pool: float = self.length_pool*self.count_pool/self.M_IN_KM/self.duration
        return aver_Speed_Swim_pool

    #расчёт израсходованных калорий <<(средняя_скорость + 1.1) * 2 * вес  >>
    def get_spent_calories(self) -> float:

        COEF_CAL_SWIM_1 = 1.1
        COEF_CAL_SWIM_2 = 2
        aver_Speed_Swim_cal = self.get_mean_speed()
        Cal_Caculation_Swim: float = (aver_Speed_Swim_cal + COEF_CAL_SWIM_1)*COEF_CAL_SWIM_2*self.weight
        return Cal_Caculation_Swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    #Создаю словарь, в котором сопоставляются коды тренировок и классы
    Dict_workout = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }  
    #Проверяем, есть ли входящий аргумент в списке ключей.
    #И если есть, выполняем код.
    if workout_type in Dict_workout:
        training = Dict_workout[workout_type](*data)
    return training                 
    

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print (info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

