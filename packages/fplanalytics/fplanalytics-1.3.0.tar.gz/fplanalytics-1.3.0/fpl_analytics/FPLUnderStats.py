import codecs
import json
import re
import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import threading

NAME_LOOKUP = {
    'Rui Patrício': 'Rui Pedro dos Santos Patrício',
    'Nélson Semedo': 'Nélson Cabral Semedo',
    'Joelinton': 'Joelinton Cássio Apolinário de Lira',
    'Aleksandar Mitrovic': 'Aleksandar Mitrović',
    'João Moutinho': 'João Filipe Iria Santos Moutinho',
    'Bobby Reid': 'Bobby Decordova-Reid',
    'Emiliano Martinez': 'Emiliano Martínez',
    'Kepa': 'Kepa Arrizabalaga',
    'Dara O&#039;Shea': "Dara O'Shea",
    'Willian': 'Willian Borges Da Silva',
    'Richarlison': 'Richarlison de Andrade',
    'Eddie Nketiah': 'Edward Nketiah',
    'Solly March': 'Solomon March',
    'Caglar Söyüncü': 'Çaglar Söyüncü',
    'N&#039;Golo Kanté': "N'Golo Kanté",
    'Dele Alli': 'Bamidele Alli',
    'Semi Ajayi': 'Oluwasemilogo Adesewo Ibidapo Ajayi',
    'Oriol Romeu': 'Oriol Romeu Vidal',
    'Franck Zambo': 'André-Frank Zambo Anguissa',
    'Tanguy NDombele Alvaro': 'Tanguy Ndombele',
    'Alisson': 'Alisson Ramses Becker',
    'Ivan Cavaleiro': 'Ivan Ricardo Neves Abreu Cavaleiro',
    'Hélder Costa': 'Hélder Wander Sousa de Azevedo e Costa',
    'Bruno Fernandes': 'Bruno Miguel Borges Fernandes',
    'Felipe Anderson': 'Felipe Anderson Pereira Gomes',
    'Ferrán Torres': 'Ferran Torres',
    'Ederson': 'Ederson Santana de Moraes',
    'Nicolas Pepe': 'Nicolas Pépé',
    'Pablo Hernández': 'Pablo Hernández Domínguez',
    'Ian Poveda-Ocampo': 'Ian Carlo Poveda-Ocampo',
    'Dani Ceballos': 'Daniel Ceballos Fernández',
    'Lucas Moura': 'Lucas Rodrigues Moura da Silva',
    'Gabriel Jesus': 'Gabriel Fernando de Jesus',
    'Mohamed Elneny': 'Mohamed Naser El Sayed Elneny',
    'Son Heung-Min': 'Heung-Min Son',
    'Rúben Vinagre': 'Rúben Gonçalo Silva Nascimento Vinagre',
    'Thiago Alcántara': 'Thiago Alcántara do Nascimento',
    'Daniel Podence': 'Daniel Castelo Podence',
    'Pedro Neto': 'Pedro Lomba Neto',
    'Douglas Luiz': 'Douglas Luiz Soares de Paulo',
    'Gabriel': 'Gabriel Magalhães',
    'Fabinho': 'Fabio Henrique Tavares',
    'Jorginho': 'Jorge Luiz Frello Filho',
    'André Gomes': 'André Filipe Tavares Gomes',
    'Fernandinho': 'Fernando Luiz Rosa',
    'Vitinha': 'Vitor Ferreira',
    'David Luiz': 'David Luiz Moreira Marinho',
    'Trézéguet': 'Mahmoud Ahmed Ibrahim Hassan',
    'Thiago Silva': 'Thiago Thiago',
    'Allan': 'Allan Marques Loureiro',
    'Romain Saiss': 'Romain Saïss',
    'Rúben Neves': 'Rúben Diogo da Silva Neves',
    'Fred': 'Frederico Rodrigues de Paula Santos',
    'Jack O&#039;Connell': "Jack O'Connell",
    'Mat Ryan': 'Mathew Ryan',
    'Ben Chilwell': 'Benjamin Chilwell',
    'Rúben Dias': 'Rúben Santos Gato Alves Dias',
    'Rodrigo' : 'Rodrigo Hernandez',
    'Bernardo Silva' : 'Bernardo Mota Veiga de Carvalho e Silva',
}

LEAGUE_URL = "https://understat.com/league/{}/{}"
PLAYER_URL = "https://understat.com/player/{}"
TEAM_URL = "https://understat.com/team/{}/{}"
MATCH_URL = "https://understat.com/match/{}/"
PATTERN = r"{}\s+=\s+JSON.parse\(\'(.*?)\'\)"

def to_league_name(league_name):
    """Maps league name to the league name used by Understat for ease of use.
    """

    league_mapper = {
        "epl": "EPL",
        "la_liga": "La_liga",
        "bundesliga": "Bundesliga",
        "serie_a": "Serie_A",
        "ligue_1": "Ligue_1",
        "rfpl": "RFPL"
    }
    try:
        return league_mapper[league_name]
    except KeyError:
        return league_name


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def find_match(scripts, pattern):
    """Returns the first match found in the given scripts."""

    for script in scripts:
        match = re.search(pattern, script.string)
        if match:
            break

    return match


def decode_data(match):
    """Returns data in the match's first group decoded to JSON."""

    byte_data = codecs.escape_decode(match.group(1))
    json_data = json.loads(byte_data[0].decode("utf-8"))

    return json_data

async def get_data(session, url, data_type):
    """Returns data from the given URL of the given data type."""

    html = await fetch(session, url)
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")

    pattern = re.compile(PATTERN.format(data_type))
    match = find_match(scripts, pattern)
    data = decode_data(match)

    return data


def filter_data(data, options):
    """Filters the data by the given options."""
    if not options:
        return data

    return [item for item in data if
            all(key in item and options[key] == item[key]
                for key in options.keys())]


def filter_by_positions(data, positions):
    """Filter data by positions."""
    relevant_stats = []

    for position, stats in data.items():
        if not positions or position in positions:
            stats["position"] = position
            relevant_stats.append(stats)

    return relevant_stats

class Understat():
    def __init__(self, session):
        self.session = session

    async def get_stats(self, options=None, **kwargs):
        """Returns a list containing stats of every league, grouped by month.
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of dictionaries.
        :rtype: list
        """

        stats = await get_data(self.session, BASE_URL, "statData")

        if options:
            kwargs = options

        filtered_data = filter_data(stats, kwargs)

        return filtered_data

    async def get_teams(self, league_name, season, options=None, **kwargs):
        """Returns a list containing information about all the teams in
        the given league in the given season.
        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :type season: str or int
        :return: A list of the league's table as seen on Understat's
            league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        teams_data = await get_data(self.session, url, "teamsData")

        if options:
            kwargs = options

        filtered_data = filter_data(list(teams_data.values()), kwargs)

        return filtered_data

    async def get_league_players(
            self, league_name, season, options=None, **kwargs):
        """Returns a list containing information about all the players in
        the given league in the given season.
        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :type season: str or int
        :return: A list of the players as seen on Understat's league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        players_data = await get_data(self.session, url, "playersData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data

    async def get_league_results(
            self, league_name, season, options=None, **kwargs):
        """Returns a list containing information about all the results
        (matches) played by the teams in the given league in the given season.
        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :type season: str or int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: A list of the results as seen on Understat's league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        dates_data = await get_data(self.session, url, "datesData")
        results = [r for r in dates_data if r["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(results, kwargs)

        return filtered_data

    async def get_league_fixtures(
            self, league_name, season,  options=None, **kwargs):
        """Returns a list containing information about all the upcoming
        fixtures of the given league in the given season.
        :param league_name: The league's name.
        :type league_name: str
        :param season: The season.
        :type season: str or int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: A list of the fixtures as seen on Understat's league overview.
        :rtype: list
        """

        url = LEAGUE_URL.format(to_league_name(league_name), season)
        dates_data = await get_data(self.session, url, "datesData")
        fixtures = [f for f in dates_data if not f["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(fixtures, kwargs)

        return filtered_data

    async def get_player_shots(self, player_id, options=None, **kwargs):
        """Returns the player with the given ID's shot data.
        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the player's shot data.
        :rtype: list
        """

        url = PLAYER_URL.format(player_id)
        shots_data = await get_data(self.session, url, "shotsData")

        if options:
            kwargs = options

        filtered_data = filter_data(shots_data, kwargs)

        return filtered_data

    async def get_player_matches(self, player_id, options=None, **kwargs):
        """Returns the player with the given ID's matches data.
        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the player's matches data.
        :rtype: list
        """
        url = PLAYER_URL.format(player_id)
        matches_data = await get_data(self.session, url, "matchesData")

        if options:
            kwargs = options

        filtered_data = filter_data(matches_data, kwargs)

        return filtered_data

    async def get_player_stats(self, player_id, positions=None):
        """Returns the player with the given ID's min / max stats, per
        position(s).
        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :param positions: Positions to filter the data by, defaults to None.
        :param positions: list, optional
        :return: List of the player's stats per position.
        :rtype: list
        """
        url = PLAYER_URL.format(player_id)
        player_stats = await get_data(self.session, url, "minMaxPlayerStats")

        player_stats = filter_by_positions(player_stats, positions)

        return player_stats

    async def get_player_grouped_stats(self, player_id):
        """Returns the player with the given ID's grouped stats (as seen at
        the top of a player's page).
        :param player_id: The player's Understat ID.
        :type player_id: int or str
        :return: Dictionary of the player's grouped stats.
        :rtype: dict
        """
        url = PLAYER_URL.format(player_id)
        player_stats = await get_data(self.session, url, "groupsData")

        return player_stats

    async def get_team_stats(self, team_name, season):
        """Returns a team's stats, as seen on their page on Understat, in the
        given season.
        :param team_name: A team's name, e.g. Manchester United.
        :type team_name: str
        :param season: A season / year, e.g. 2018.
        :type season: int or str
        :return: A dictionary containing a team's stats.
        :rtype: dict
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        team_stats = await get_data(self.session, url, "statisticsData")

        return team_stats

    async def get_team_results(
            self, team_name, season, options=None, **kwargs):
        """Returns a team's results in the given season.
        :param team_name: A team's name.
        :type team_name: str
        :param season: The season.
        :type season: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the team's results in the given season.
        :rtype: list
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        dates_data = await get_data(self.session, url, "datesData")
        results = [r for r in dates_data if r["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(results, kwargs)

        return filtered_data

    async def get_team_fixtures(
            self, team_name, season, options=None, **kwargs):
        """Returns a team's upcoming fixtures in the given season.
        :param team_name: A team's name.
        :type team_name: str
        :param season: The season.
        :type season: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the team's upcoming fixtures in the given season.
        :rtype: list
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        dates_data = await get_data(self.session, url, "datesData")
        fixtures = [f for f in dates_data if not f["isResult"]]

        if options:
            kwargs = options

        filtered_data = filter_data(fixtures, kwargs)

        return filtered_data

    async def get_team_players(
            self, team_name, season, options=None, **kwargs):
        """Returns a team's player statistics in the given season.
        :param team_name: A team's name.
        :type team_name: str
        :param season: The season.
        :type season: int or str
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: List of the team's players' statistics in the given season.
        :rtype: list
        """

        url = TEAM_URL.format(team_name.replace(" ", "_"), season)
        players_data = await get_data(self.session, url, "playersData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data

    async def get_match_players(self, match_id, options=None, **kwargs):
        """Returns a dictionary containing information about the players who
        played in the given match.
        :param fixture_id: A match's ID.
        :type fixture_id: int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: Dictionary containing information about the players who played
            in the match.
        :rtype: dict
        """

        url = MATCH_URL.format(match_id)
        players_data = await get_data(self.session, url, "rostersData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data

    async def get_match_shots(self, match_id, options=None, **kwargs):
        """Returns a dictionary containing information about shots taken by
        the players in the given match.
        :param fixture_id: A match's ID.
        :type fixture_id: int
        :param options: Options to filter the data by, defaults to None.
        :param options: dict, optional
        :return: Dictionary containing information about the players who played
            in the match.
        :rtype: dict
        """

        url = MATCH_URL.format(match_id)
        players_data = await get_data(self.session, url, "shotsData")

        if options:
            kwargs = options

        filtered_data = filter_data(players_data, kwargs)

        return filtered_data

class GetStats:
    
    def __init__(self):
        self.players = []
        
    async def async_get_league_player(self, league_name = 'epl', season = '2020'):
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            players = await understat.get_league_players(
                    league_name,
                    season,
                )
            players = pd.DataFrame(players)
            players['player_name'] =  players[['player_name']].apply(lambda x, lookup: lookup.get(x['player_name'], x['player_name']), axis =1, lookup = NAME_LOOKUP)
            self.players = players
    
    def get_league_players(self, league_name = 'epl', season = '2020'):
        
        #loop = asyncio.get_event_loop()
        #loop.create_task(self.async_get_league_player(league_name, season))
        t1 = threading.Thread(target=asyncio.run, args=(self.async_get_league_player(league_name, season), ))
        t1.start()
        t1.join()
        #asyncio.run_coroutine_threadsafe(self.async_get_league_player(league_name, season), loop)
        

