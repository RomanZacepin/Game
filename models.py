
import random
from abc import ABC, abstractmethod
from datetime import datetime


class GameEntity(ABC):
    # Базовый класс для всего, что есть в игре
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Имя не может быть пустым")
        self._name = value

    @abstractmethod
    def describe(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self._name})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self._name!r})"

    def __eq__(self, other):
        if not isinstance(other, GameEntity):
            return NotImplemented
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)


class Card(GameEntity):
    # Одна карточка на поле
    def __init__(self, value, back_icon, card_id):
        super().__init__(f"Card-{card_id}")
        self._value = value
        self._back_icon = back_icon
        self._revealed = False
        self._matched = False
        self._card_id = card_id

    @property
    def value(self):
        return self._value

    @property
    def revealed(self):
        return self._revealed

    @revealed.setter
    def revealed(self, v):
        self._revealed = bool(v)

    @property
    def matched(self):
        return self._matched

    @matched.setter
    def matched(self, v):
        self._matched = bool(v)

    @property
    def card_id(self):
        return self._card_id

    def describe(self):
        return f"Карточка #{self._card_id} со значением {self._value}"

    def open(self):
        self._revealed = True

    def close(self):
        self._revealed = False

    def match(self):
        self._matched = True
        self._revealed = True

    def __eq__(self, other):
        # Две карточки равны, если у них одинаковое значение
        if not isinstance(other, Card):
            return NotImplemented
        return self._value == other._value

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self._card_id < other._card_id

    def __hash__(self):
        return hash(self._card_id)

    def __str__(self):
        return f"Card({self._card_id}, value={self._value!r})"

    def __repr__(self):
        return f"Card(value={self._value!r}, id={self._card_id})"


class Deck(GameEntity):
    # Колода: набор парных карточек
    def __init__(self, icons, pairs, back_icon):
        super().__init__(f"Deck-{pairs}pairs")
        self._pairs = pairs
        self._back_icon = back_icon
        self._cards = self._build(icons, pairs, back_icon)

    @property
    def pairs(self):
        return self._pairs

    @property
    def cards(self):
        return self._cards

    @property
    def size(self):
        return len(self._cards)

    @staticmethod
    def _build(icons, pairs, back_icon):
        # Берём случайные иконки, дублируем и перемешиваем
        selected = random.sample(icons, pairs)
        values = selected * 2
        random.shuffle(values)
        return [
            Card(value=v, back_icon=back_icon, card_id=i)
            for i, v in enumerate(values)
        ]

    def describe(self):
        return f"Колода из {self._pairs} пар ({self.size} карточек)"

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return iter(self._cards)

    def __getitem__(self, idx):
        return self._cards[idx]

    def __str__(self):
        return f"Deck(pairs={self._pairs}, cards={self.size})"


class GameRecord(GameEntity):
    # Результат одной сыгранной игры
    def __init__(self, level, time_sec, moves, errors):
        super().__init__(f"Record-{level}")
        self._level = level
        self._time_sec = int(time_sec)
        self._moves = int(moves)
        self._errors = int(errors)

    @property
    def level(self):
        return self._level

    @property
    def time_sec(self):
        return self._time_sec

    @property
    def moves(self):
        return self._moves

    @property
    def errors(self):
        return self._errors

    def describe(self):
        return (
            f"{self._level}: {self._time_sec} сек, "
            f"{self._moves} ходов, {self._errors} ошибок"
        )

    def __lt__(self, other):
        if not isinstance(other, GameRecord):
            return NotImplemented
        return self._time_sec < other._time_sec

    def __eq__(self, other):
        if not isinstance(other, GameRecord):
            return NotImplemented
        return (
            self._time_sec == other._time_sec
            and self._moves == other._moves
        )

    def __str__(self):
        return self.describe()


class ScoreCollection(GameEntity):
    # Список рекордов. Сделан специально вместо dict
    def __init__(self):
        super().__init__("Scores")
        self._records = []

    @property
    def records(self):
        return list(self._records)

    def add(self, record):
        # Если для этого уровня уже есть результат — оставляем лучший
        for i, existing in enumerate(self._records):
            if existing.level == record.level:
                if record < existing:
                    self._records[i] = record
                    return True
                return False

        self._records.append(record)
        return True

    def get(self, level):
        for r in self._records:
            if r.level == level:
                return r
        return None

    def sorted_by_time(self):
        return sorted(self._records, key=lambda r: r.time_sec)

    def describe(self):
        return f"Коллекция рекордов ({len(self._records)} записей)"

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        return iter(self._records)

    def __contains__(self, level):
        return any(r.level == level for r in self._records)

    def __str__(self):
        return f"ScoreCollection({len(self._records)} records)"


class Player(GameEntity):
    # Игрок — нужен для отчёта
    def __init__(self, name="Player"):
        super().__init__(name)
        self._time_in = datetime.now()
        self._time_out = None

    @property
    def time_in(self):
        return self._time_in

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def describe(self):
        return (
            f"Игрок {self._name} "
            f"(вошёл в {self._time_in:%d.%m.%Y %H:%M:%S})"
        )

    def __str__(self):
        return f"Player({self._name})"
