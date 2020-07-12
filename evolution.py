import argparse
from string import ascii_lowercase
from random import choice
from typing import List, Tuple


class PhraseCreature:
    def __init__(self, phrase, genes):
        self.phrase = phrase
        self.genes = genes

    def __lt__(self, other):
        if self.phrase < other.phrase:
            return True
        return False

    def __str__(self):
        return str(self.phrase)


def create_random_string(string_length: int) -> str:
    """Метод для того чтобы создать изначальную случайную строку

    :param string_length: длинна строки
    """
    out_str = []
    for i in range(0, string_length):
        out_str.append(choice(ascii_lowercase + " "))

    return "".join(out_str)


def match(offspring_object: PhraseCreature, selection_phrase: str) -> int:
    """Метод для того чтобы определить коло-во правильных вхождений букв у наследника
    
    :param offspring_object: Объект наследника
    :param selection_phrase: Правильная фраза
    """
    mismatch = 0
    # проверям совпадения по буквенно
    for c1, c2 in zip(offspring_object.phrase, selection_phrase):
        if c1 != c2:
            mismatch += 1
    return mismatch


def mutate(parent) -> PhraseCreature:
    """Метод для мутации каждого наследника
        Мутация - берем случайную букву из фразы родителя и меняем её на случайную букву
        из ascii_letters

    :param parent: Объект родителя
    """
    parent_string = parent.phrase

    genes = parent.genes
    genes.append(parent_string)

    # переделываем фразу в список из букв
    parent_string = list(parent_string)

    # выбираем по какому номеру будет произведена замена символа
    mutated_index = choice(range(0, len(parent_string)))
    # выбираем какой символ будет заменен
    mutation_char = choice(ascii_lowercase + " ")

    parent_string[mutated_index] = mutation_char
    mutated_string = "".join(parent_string)

    # создаем новый объект
    return PhraseCreature(mutated_string, genes)


def create_offsprings(parent: PhraseCreature,
                      number_of_offsprings: int = 100) -> List[PhraseCreature]:
    """Создаем 100 потомков для родителя

    :param parent: родитель
    :param number_of_offsprings: количество потомков, по дефолту 100
    """
    output = []
    for i in range(0, number_of_offsprings):
        # мутируем и создаем потомков от каждого родителя
        output.append(mutate(parent))
    return output


def select(offsprings: List, selection_word: str,
           survival_size: int = 10) -> List[PhraseCreature]:
    """Метод для того чтобы сделать выборку из лучших 10 наследников

    :param offsprings: список из 1000 наследников
    :param selection_word: правильная фраза
    :param survival_size: размер выживших наследников, по дефолту 10
    """
    # определяем сколько приавильных вхождений букв есть в каждом наследнике
    survival_value = map(lambda x: (match(x, selection_word), x), offsprings)
    # фильтруем по последним 10ти по правильным вхождениям
    return list(map(lambda x: x[1], sorted(survival_value)[:survival_size]))


def create_next_generation(generation: List, selection_word: str) -> List[PhraseCreature]:
    """Создаем следующее поколение

    :param generation: текущее поколение
    :param selection_word: правильное слово
    """
    offsprings = []
    for parent in generation:
        # для каждого объекта из поколения создаем 100 наследников
        # в сумме получается 10 родителей * 100 наследников = 1000 наследников
        offsprings += create_offsprings(parent)

    # из всех наследников делаем выборку из 10, которые выжили и оказались самыми лучшими
    next_generation = select(offsprings, selection_word)
    return next_generation


def is_present(selection_word: str, generation: List) -> bool:
    """Проверям содержит ли популяция правильный ответ

    :param selection_word: правильная фраза
    :param generation: список объектов текущей популяции
    """
    # получаем список фраз из каждого объекта в популяции
    generation_words = list(map(lambda x: x.phrase, generation))
    return True if selection_word in generation_words else False


def evolution(selection_phrase, show_output: bool,
              max_num_generations=2000) -> Tuple[PhraseCreature, int]:
    """Реализация генетического алгоритма
    
    :param show_output:
    :param selection_phrase: фраза которую нужно создать
    :param max_num_generations: максимальное коло-во поколений, по дефолту 2000
    """
    selection_phrase = selection_phrase.lower()
    # создаем случайную строку
    random_string = create_random_string(len(selection_phrase))

    generation = [PhraseCreature(random_string, [])]
    generation_index = 1

    # главный цикл
    while True:
        # создаем следующее поколение
        generation = create_next_generation(generation, selection_phrase)
        if show_output:
            print(generation_index, generation[0].phrase)
        # если входящая фраза есть в текущем поколении - останавливаем итерацию
        if is_present(selection_phrase, generation):
            break

        generation_index += 1
        if generation_index > max_num_generations:
            raise Exception("Maximum count of iterations was reached")
    return generation[0], generation_index


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process genetic algorithm.')
    parser.add_argument('phrase', type=str, help='input phrase')
    parser.add_argument('--show_output', '--output', action='store_true',
                        help="shows output")
    args = parser.parse_args()
    result = evolution(args.phrase, args.show_output)

    if not args.show_output:
        print(result[0].phrase)
