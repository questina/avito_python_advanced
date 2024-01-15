class BasePokemon:
    """BasePokemon class"""

    def __init__(self, name: str, poketype: str):
        self.name = name
        self.poketype = poketype

    def __str__(self) -> str:
        return f'{self.name, self.poketype}'


class PokemonMixin:
    def __init__(self, name: str, poketype: str):
        super().__init__(name, poketype)

    def __str__(self) -> str:
        emoji_dict = {'electric': '⚡', 'grass': '🌿'}
        return f'{self.name}: {emoji_dict[self.poketype]}'


class Pokemon(PokemonMixin, BasePokemon):
    pass


if __name__ == '__main__':
    print(Pokemon('Bulbasaur', 'grass'))
    print(Pokemon('Pikachu', 'electric'))
