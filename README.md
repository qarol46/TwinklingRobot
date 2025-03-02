# TwinklingRobot
# Проектная практика: Робот-исследователь

![Робот](photo_2023-05-26_15-04-25.jpg)  

## Описание проекта

Робот, созданный в рамках **проектной практики** на втором семестре. 

Задача робота заключалась в следующем:
- **Объезд препятствий**: Робот способен обнаруживать и объезжать препятствия на своем пути.
- **Поиск цветной клетки**: Робот ищет цветную клетку заданного цвета.
- **Коммуникация между роботами**: Для координации действий используется протокол **ESP-NOW**, который позволяет роботам-сокомандникам обмениваться информацией о найденных цветных клетках.
- **Цель проекта**: Найти комплект цветных клеток, состоящий из 4 различных цветов.

## Технические детали

- **Основные компоненты**:
  - Микроконтроллер ESP32
  - Датчики расстояния (например, ультразвуковые HC-SR04)
  - Цветовой датчик для распознавания цветов
  - Колесный привод для движения
  
- **Программное обеспечение**:
  - Язык программирования: MicroPython
  - Библиотеки: ESP-NOW для беспроводной связи между роботами

## Инструкция по запуску

1. Установите необходимые библиотеки для работы с ESP32.
2. Загрузите код на микроконтроллер.
3. Настройте параметры связи между роботами через ESP-NOW.
4. Проверьте работу датчиков и камеры.
