"""For deserializing the json responses"""
import abc
import math
import random
from collections import OrderedDict
import re

from dateutil.parser import parse

from blaseball_mike import database, reference, chronicler, tables



class Base(abc.ABC):

    _camel_to_snake_re = re.compile(r'(?<!^)(?=[A-Z])')

    def __init__(self, data):
        self.fields = []
        for key, value in data.items():
            self.fields.append(key)
            setattr(self, Base._from_api_conversion(key), value)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.json() == other.json()
        return NotImplemented

    @staticmethod
    def _camel_to_snake(name):
        # Blaseball API uses camelCase for fields, convert to the more Pyhonistic snake_case
        return Base._camel_to_snake_re.sub('_', name).lower()

    @staticmethod
    def _remove_leading_underscores(name):
        # Some fields historically have underscores before them (_id)
        return name.strip('_')

    @staticmethod
    def _from_api_conversion(name):
        return Base._remove_leading_underscores(Base._camel_to_snake(name))

    @staticmethod
    def _custom_key_transform(name):
        # To be implemented by child classes
        return name

    def json(self):
        return {
            f: getattr(self, self._custom_key_transform(self._from_api_conversion(f))) for f in self.fields
        }


class GlobalEvent(Base):

    @classmethod
    def load(cls):
        events = database.get_global_events()
        return [cls(event) for event in events]


class SimulationData(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "league":
            return "_league_id"
        if name == "day":
            return "_day"
        if name == "season":
            return "_season"
        return name

    @classmethod
    def load(cls):
        return cls(database.get_simulation_data())

    @property
    def league(self):
        if self._league:
            return self._league
        self._league = League.load_by_id(self._league_id)
        return self._league

    @league.setter
    def league(self, value):
        self._league = None
        self._league_id = value

    @property
    def next_election_end(self):
        return self._next_election_end

    @next_election_end.setter
    def next_election_end(self, value):
        self._next_election_end = parse(value)

    @property
    def next_phase_time(self):
        return self._next_phase_time

    @next_phase_time.setter
    def next_phase_time(self, value):
        self._next_phase_time = parse(value)

    @property
    def next_season_start(self):
        return self._next_season_start

    @next_season_start.setter
    def next_season_start(self, value):
        self._next_season_start = parse(value)


class Player(Base):

    @staticmethod
    def _custom_key_transform(name):
        lookup_dict = {
            "blood": "_blood_id",
            "coffee": "_coffee_id",
            "bat": "_bat_id",
            "armor": "_armor_id",
            "perm_attr": "_perm_attr_ids",
            "seas_attr": "_seas_attr_ids",
            "week_attr": "_week_attr_ids",
            "game_attr": "_game_attr_ids",
            "tournament_team_id": "_tournament_team_id",
            "league_team_id": "_league_team_id",
        }
        if name in lookup_dict:
            return lookup_dict[name]
        return name

    @classmethod
    def load(cls, *ids):
        """
        Load dictionary of players
        """
        players = database.get_player(list(ids))
        return {
            id_: cls(player) for (id_, player) in players.items()
        }

    @classmethod
    def load_one(cls, id_):
        """
        Load single player.
        """
        return cls.load(id_).get(id_)

    @classmethod
    def load_one_at_time(cls, id_, time):
        if isinstance(time, str):
            time = parse(time)

        players = chronicler.get_player_updates(id_, before=time, order="desc", count=1)
        return cls(dict(players[0]["data"], timestamp=time))

    @classmethod
    def load_history(cls, id_, order='desc'):
        """
        Returns array of Player stat changes with most recent first.
        """
        players = chronicler.get_player_updates(ids=id_, order=order)
        return [cls(dict(p['data'], timestamp=p['firstSeen'])) for p in players]

    @classmethod
    def find_by_name(cls, name):
        """
        Try to find the player by their name (case sensitive) or return None.
        """
        ids = reference.get_player_ids_by_name(name)
        if not ids:
            return None
        return cls.load_one(ids[0])

    @classmethod
    def make_random(cls, name="Random Player", seed=None):
        """
        Generate a completely random player.
        """
        rng = random.Random(seed)
        return Player({
            'name': name,
            'baseThirst': rng.random(),
            'continuation': rng.random(),
            'ground_friction': rng.random(),
            'indulgence': rng.random(),
            'laserlikeness': rng.random(),
            'divinity': rng.random(),
            'martyrdom': rng.random(),
            'moxie': rng.random(),
            'musclitude': rng.random(),
            'patheticism': rng.random(),
            'thwackability': rng.random(),
            'tragicness': rng.random(),
            'anticapitalism': rng.random(),
            'chasiness': rng.random(),
            'omniscience': rng.random(),
            'tenaciousness': rng.random(),
            'watchfulness': rng.random(),
            'coldness': rng.random(),
            'overpowerment': rng.random(),
            'ruthlessness': rng.random(),
            'shakespearianism': rng.random(),
            'unthwackability': rng.random(),
            'buoyancy': rng.random(),
            'cinnamon': rng.random(),
            'deceased': rng.random(),
            'peanutAllergy': rng.random(),
            'pressurization': rng.random(),
            'soul': rng.random(),
            'totalFingers': rng.random(),
        })

    @property
    def hitting_rating(self):
        if getattr(self, "_hitting_rating", None):
            return self._hitting_rating
        return (((1 - self.tragicness) ** 0.01) * ((1 - self.patheticism) ** 0.05) *
                ((self.thwackability * self.divinity) ** 0.35) *
                ((self.moxie * self.musclitude) ** 0.075) * (self.martyrdom ** 0.02))

    @hitting_rating.setter
    def hitting_rating(self, value):
        self._hitting_rating = value

    @property
    def batting_rating(self):
        return self.hitting_rating

    @property
    def pitching_rating(self):
        if getattr(self, "_pitching_rating", None):
            return self._pitching_rating
        return ((self.unthwackability ** 0.5) * (self.ruthlessness ** 0.4) *
                (self.overpowerment ** 0.15) * (self.shakespearianism ** 0.1) * (self.coldness ** 0.025))

    @pitching_rating.setter
    def pitching_rating(self, value):
        self._pitching_rating = value

    @property
    def baserunning_rating(self):
        if getattr(self, "_baserunning_rating", None):
            return self._baserunning_rating
        return ((self.laserlikeness**0.5) *
                ((self.continuation * self.base_thirst * self.indulgence * self.ground_friction) ** 0.1))

    @baserunning_rating.setter
    def baserunning_rating(self, value):
        self._baserunning_rating = value

    @property
    def defense_rating(self):
        if getattr(self, "_defense_rating", None):
            return self._defense_rating
        return (((self.omniscience * self.tenaciousness) ** 0.2) *
                ((self.watchfulness * self.anticapitalism * self.chasiness) ** 0.1))

    @defense_rating.setter
    def defense_rating(self, value):
        self._defense_rating = value

    @staticmethod
    def _rating_to_stars(val):
        return 0.5 * (round(val * 10))

    @property
    def hitting_stars(self):
        return self._rating_to_stars(self.hitting_rating)

    @property
    def batting_stars(self):
        return self.hitting_stars

    @property
    def pitching_stars(self):
        return self._rating_to_stars(self.pitching_rating)

    @property
    def baserunning_stars(self):
        return self._rating_to_stars(self.baserunning_rating)

    @property
    def defense_stars(self):
        return self._rating_to_stars(self.defense_rating)

    def get_vibe(self, day):
        """
        Day is 1-indexed
        """
        return 0.5 * ((self.pressurization + self.cinnamon) *
                      math.sin(math.pi * (2 / (6 + round(10 * self.buoyancy)) * (day - 1) + 0.5)) -
                      self.pressurization + self.cinnamon)

    @property
    def soulscream(self):
        letters = ["A", "E", "I", "O", "U", "X", "H", "A", "E", "I"]
        stats = [self.pressurization, self.divinity, self.tragicness, self.shakespearianism, self.ruthlessness]

        scream = []
        for r in range(self.soul):
            sub_scream = []
            i = 10 ** -r
            for s in stats:
                try:
                    c = math.floor((s % i) / i * 10)
                    sub_scream.append(letters[c])
                except ZeroDivisionError:
                    sub_scream.append("undefined")
            scream.extend(sub_scream + sub_scream + [sub_scream[0]])

        return ''.join(scream)

    @property
    def blood(self):
        if getattr(self, "_blood", None):
            return self._blood
        self._blood = database.get_blood(getattr(self, "_blood_id", None))[0]
        return self._blood

    @blood.setter
    def blood(self, value):
        self._blood = None
        self._blood_id = value

    @property
    def coffee(self):
        if getattr(self, "_coffee", None):
            return self._coffee
        self._coffee = database.get_coffee(getattr(self, "_coffee_id", None))[0]
        return self._coffee

    @coffee.setter
    def coffee(self, value):
        self._coffee = None
        self._coffee_id = value

    @property
    def bat(self):
        if getattr(self, "_bat", None):
            return self._bat
        self._bat = Item.load_one(getattr(self, "_bat_id", None))
        return self._bat

    @bat.setter
    def bat(self, value):
        self._bat = None
        self._bat_id = value

    @property
    def armor(self):
        if getattr(self, "_armor", None):
            return self._armor
        self._armor = Item.load_one(getattr(self, "_armor_id", None))
        return self._armor

    @armor.setter
    def armor(self, value):
        self._armor = None
        self._armor_id = value

    @property
    def perm_attr(self):
        if getattr(self, "_perm_attr", None):
            return self._perm_attr
        if not getattr(self, "_perm_attr_ids", None):
            return []
        self._perm_attr = Modification.load(*self._perm_attr_ids)
        return self._perm_attr

    @perm_attr.setter
    def perm_attr(self, value):
        self._perm_attr = None
        self._perm_attr_ids = value

    @property
    def seas_attr(self):
        if getattr(self, "_seas_attr", None):
            return self._seas_attr
        if not getattr(self, "_seas_attr_ids", None):
            return []
        self._seas_attr = Modification.load(*self._seas_attr_ids)
        return self._seas_attr

    @seas_attr.setter
    def seas_attr(self, value):
        self._seas_attr = None
        self._seas_attr_ids = value

    @property
    def week_attr(self):
        if getattr(self, "_week_attr", None):
            return self._week_attr
        if not getattr(self, "_week_attr_ids", None):
            return []
        self._week_attr = Modification.load(*self._week_attr_ids)
        return self._week_attr

    @week_attr.setter
    def week_attr(self, value):
        self._week_attr = None
        self._week_attr_ids = value

    @property
    def game_attr(self):
        if getattr(self, "_game_attr", None):
            return self._game_attr
        if not getattr(self, "_game_attr_ids", None):
            return []
        self._game_attr = Modification.load(*self._game_attr_ids)
        return self._game_attr

    @game_attr.setter
    def game_attr(self, value):
        self._game_attr = None
        self._game_attr_ids = value

    @property
    def league_team_id(self):
        if getattr(self, "_league_team", None):
            return self._league_team
        if not getattr(self, "_league_team_id", None):
            return None
        self._league_team = Team.load(self._league_team_id)
        return self._league_team

    @league_team_id.setter
    def league_team_id(self, value):
        self._league_team = None
        self._league_team_id = value

    @property
    def league_team(self):
        # alias to league_team_id
        return self.league_team_id

    @property
    def tournament_team_id(self):
        if getattr(self, "_tournament_team", None):
            return self._tournament_team
        if not getattr(self, "_tournament_team_id", None):
            return None
        self._tournament_team = Team.load(self._tournament_team_id)
        return self._tournament_team

    @tournament_team_id.setter
    def tournament_team_id(self, value):
        self._tournament_team = None
        self._tournament_team_id = value

    @property
    def tournament_team(self):
        # alias to tournament_team_id
        return self.tournament_team_id

    def simulated_copy(self, overrides=None, multipliers=None, buffs=None, reroll=None):
        """
        Return a copy of this player with adjusted stats (ie to simulate blessings)
        `overrides` is a dict where the key specifies an attribute to completely overwrite with new value.
        `multipliers` is a dict where key specifies attr to multiply by value
        `buffs` is a dict where key specifies attr to add value
        `reroll` is a dict where the key specifies attr to reroll (value is unused)

        `batting_rating`, `pitching_rating`, `baserunning_rating`, `defense_rating`, and `overall_rating`
        can additionally be passed to `multipliers` and `buffs` to automatically multiply the appropriate
        related stats.
        """
        overrides = overrides or {}
        multipliers = multipliers or {}
        buffs = buffs or {}
        reroll = reroll or {}
        original_json = self.json()

        for override_key, override_value in overrides.items():
            original_json[override_key] = override_value

        for m_key, m_val in multipliers.items():
            if m_key in ('batting_rating', 'overall_rating'):
                original_json['tragicness'] *= (1.0 - m_val)
                original_json['patheticism'] *= (1.0 - m_val)
                original_json['thwackability'] *= (1.0 + m_val)
                original_json['divinity'] *= (1.0 + m_val)
                original_json['moxie'] *= (1.0 + m_val)
                original_json['musclitude'] *= (1.0 + m_val)
                original_json['martyrdom'] *= (1.0 + m_val)
            if m_key in ('pitching_rating', 'overall_rating'):
                original_json['unthwackability'] *= (1.0 + m_val)
                original_json['ruthlessness'] *= (1.0 + m_val)
                original_json['overpowerment'] *= (1.0 + m_val)
                original_json['shakespearianism'] *= (1.0 + m_val)
                original_json['coldness'] *= (1.0 + m_val)
            if m_key in ('baserunning_rating', 'overall_rating'):
                original_json['laserlikeness'] *= (1.0 + m_val)
                original_json['continuation'] *= (1.0 + m_val)
                original_json['baseThirst'] *= (1.0 + m_val)
                original_json['indulgence'] *= (1.0 + m_val)
                original_json['groundFriction'] *= (1.0 + m_val)
            if m_key in ('defense_rating', 'overall_rating'):
                original_json['omniscience'] *= (1.0 + m_val)
                original_json['tenaciousness'] *= (1.0 + m_val)
                original_json['watchfulness'] *= (1.0 + m_val)
                original_json['anticapitalism'] *= (1.0 + m_val)
                original_json['chasiness'] *= (1.0 + m_val)
            if m_key in ('tragicness', 'patheticism'):
                original_json[m_key] *= (1.0 - m_val)
            elif m_key in original_json:
                original_json[m_key] *= (1.0 + m_val)

        for b_key, b_val in buffs.items():
            if b_key in ('batting_rating', 'overall_rating'):
                original_json['tragicness'] = min(0.99, max(0.01, original_json['tragicness'] - b_val))
                original_json['patheticism'] = min(0.99, max(0.01, original_json['patheticism'] - b_val))
                original_json['thwackability'] = max(0.01, original_json['thwackability'] + b_val)
                original_json['divinity'] = max(0.01, original_json['divinity'] + b_val)
                original_json['moxie'] = max(0.01, original_json['moxie'] + b_val)
                original_json['musclitude'] = max(0.01, original_json['musclitude'] + b_val)
                original_json['martyrdom'] = max(0.01, original_json['martyrdom'] + b_val)
            if b_key in ('pitching_rating', 'overall_rating'):
                original_json['unthwackability'] = max(0.01, original_json['unthwackability'] + b_val)
                original_json['ruthlessness'] = max(0.01, original_json['ruthlessness'] + b_val)
                original_json['overpowerment'] = max(0.01, original_json['overpowerment'] + b_val)
                original_json['shakespearianism'] = max(0.01, original_json['shakespearianism'] + b_val)
                original_json['coldness'] = max(0.01, original_json['coldness'] + b_val)
            if b_key in ('baserunning_rating', 'overall_rating'):
                original_json['laserlikeness'] = max(0.01, original_json['laserlikeness'] + b_val)
                original_json['continuation'] = max(0.01, original_json['continuation'] + b_val)
                original_json['baseThirst'] = max(0.01, original_json['baseThirst'] + b_val)
                original_json['indulgence'] = max(0.01, original_json['indulgence'] + b_val)
                original_json['groundFriction'] = max(0.01, original_json['groundFriction'] + b_val)
            if b_key in ('defense_rating', 'overall_rating'):
                original_json['omniscience'] = max(0.01, original_json['omniscience'] + b_val)
                original_json['tenaciousness'] = max(0.01, original_json['tenaciousness'] + b_val)
                original_json['watchfulness'] = max(0.01, original_json['watchfulness'] + b_val)
                original_json['anticapitalism'] = max(0.01, original_json['anticapitalism'] + b_val)
                original_json['chasiness'] = max(0.01, original_json['chasiness'] + b_val)
            if b_key in ('tragicness', 'patheticism'):
                original_json[b_key] = min(0.99, max(0.01, original_json[b_key] - b_val))
            elif b_key in original_json:
                original_json[b_key] = max(0.01, original_json[b_key] + b_val)

        for r_key, _ in reroll.items():
            if r_key in ('batting_rating', 'overall_rating'):
                original_json['tragicness'] = random.uniform(0.01, 0.99)
                original_json['patheticism'] = random.uniform(0.01, 0.99)
                original_json['thwackability'] = random.uniform(0.01, 0.99)
                original_json['divinity'] = random.uniform(0.01, 0.99)
                original_json['moxie'] = random.uniform(0.01, 0.99)
                original_json['musclitude'] = random.uniform(0.01, 0.99)
                original_json['martyrdom'] = random.uniform(0.01, 0.99)
            if r_key in ('pitching_rating', 'overall_rating'):
                original_json['unthwackability'] = random.uniform(0.01, 0.99)
                original_json['ruthlessness'] = random.uniform(0.01, 0.99)
                original_json['overpowerment'] = random.uniform(0.01, 0.99)
                original_json['shakespearianism'] = random.uniform(0.01, 0.99)
                original_json['coldness'] = random.uniform(0.01, 0.99)
            if r_key in ('baserunning_rating', 'overall_rating'):
                original_json['laserlikeness'] = random.uniform(0.01, 0.99)
                original_json['continuation'] = random.uniform(0.01, 0.99)
                original_json['baseThirst'] = random.uniform(0.01, 0.99)
                original_json['indulgence'] = random.uniform(0.01, 0.99)
                original_json['groundFriction'] = random.uniform(0.01, 0.99)
            if r_key in ('defense_rating', 'overall_rating'):
                original_json['omniscience'] = random.uniform(0.01, 0.99)
                original_json['tenaciousness'] = random.uniform(0.01, 0.99)
                original_json['watchfulness'] = random.uniform(0.01, 0.99)
                original_json['anticapitalism'] = random.uniform(0.01, 0.99)
                original_json['chasiness'] = random.uniform(0.01, 0.99)
            if r_key in ('tragicness', 'patheticism'):
                original_json[r_key] = random.uniform(0.01, 0.99)
            elif r_key in original_json:
                original_json[r_key] = random.uniform(0.01, 0.99)

        # Clear database-provided ratings to force a recalculation
        original_json['hittingRating'] = None
        original_json['pitchingRating'] = None
        original_json['baserunningRating'] = None
        original_json['defenseRating'] = None

        return Player(original_json)


class Team(Base):

    @staticmethod
    def _custom_key_transform(name):
        lookup_dict = {
            "lineup": "_lineup_ids",
            "rotation": "_rotation_ids",
            "bench": "_bench_ids",
            "bullpen": "_bullpen_ids",
            "perm_attr": "_perm_attr_ids",
            "seas_attr": "_seas_attr_ids",
            "week_attr": "_week_attr_ids",
            "game_attr": "_game_attr_ids",
            "card": "_card",
        }
        if name in lookup_dict:
            return lookup_dict[name]
        return name

    @classmethod
    def load(cls, id_):
        return cls(database.get_team(id_))

    @classmethod
    def load_all(cls):
        """
        Returns dictionary keyed by team ID
        """
        return {
            id_: cls(team) for id_, team in database.get_all_teams().items()
        }

    @classmethod
    def load_by_name(cls, name):
        """
        Name can be full name or nickname, case insensitive.
        """
        teams = cls.load_all().values()
        name = name.lower()
        for team in teams:
            if name in team.full_name.lower():
                return team
        return None

    @classmethod
    def load_at_time(cls, id_, time):
        if isinstance(time, str):
            time = parse(time)

        team = chronicler.get_team_updates(id_, before=time, order="desc", count=1)
        return cls(dict(team[0]["data"], timestamp=time))

    @property
    def lineup(self):
        if self._lineup:
            return self._lineup
        if getattr(self, "timestamp", None):
            self._lineup = [Player.load_one_at_time(x, self.timestamp) for x in self._lineup_ids]
        else:
            players = Player.load(*self._lineup_ids)
            self._lineup = [players.get(id_) for id_ in self._lineup_ids]
        return self._lineup

    @lineup.setter
    def lineup(self, value):
        self._lineup = None
        self._lineup_ids = value

    @property
    def rotation(self):
        if self._rotation:
            return self._rotation
        if getattr(self, "timestamp", None):
            self._rotation = [Player.load_one_at_time(x, self.timestamp) for x in self._rotation_ids]
        else:
            players = Player.load(*self._rotation_ids)
            self._rotation = [players.get(id_) for id_ in self._rotation_ids]
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = None
        self._rotation_ids = value

    @property
    def bullpen(self):
        if self._bullpen:
            return self._bullpen
        if getattr(self, "timestamp", None):
            self._bullpen = [Player.load_one_at_time(x, self.timestamp) for x in self._bullpen_ids]
        else:
            players = Player.load(*self._bullpen_ids)
            self._bullpen = [players.get(id_) for id_ in self._bullpen_ids]
        return self._bullpen

    @bullpen.setter
    def bullpen(self, value):
        self._bullpen = None
        self._bullpen_ids = value

    @property
    def bench(self):
        if self._bench:
            return self._bench
        if getattr(self, "timestamp", None):
            self._bench = [Player.load_one_at_time(x, self.timestamp) for x in self._bench_ids]
        else:
            players = Player.load(*self._bench_ids)
            self._bench = [players.get(id_) for id_ in self._bench_ids]
        return self._bench

    @bench.setter
    def bench(self, value):
        self._bench = None
        self._bench_ids = value

    @property
    def perm_attr(self):
        if getattr(self, "_perm_attr", None):
            return self._perm_attr
        if not getattr(self, "_perm_attr_ids", None):
            return []
        self._perm_attr = Modification.load(*self._perm_attr_ids)
        return self._perm_attr

    @perm_attr.setter
    def perm_attr(self, value):
        self._perm_attr = None
        self._perm_attr_ids = value

    @property
    def seas_attr(self):
        if getattr(self, "_seas_attr", None):
            return self._seas_attr
        if not getattr(self, "_seas_attr_ids", None):
            return []
        self._seas_attr = Modification.load(*self._seas_attr_ids)
        return self._seas_attr

    @seas_attr.setter
    def seas_attr(self, value):
        self._seas_attr = None
        self._seas_attr_ids = value

    @property
    def week_attr(self):
        if getattr(self, "_week_attr", None):
            return self._week_attr
        if not getattr(self, "_week_attr_ids", None):
            return []
        self._week_attr = Modification.load(*self._week_attr_ids)
        return self._week_attr

    @week_attr.setter
    def week_attr(self, value):
        self._week_attr = None
        self._week_attr_ids = value

    @property
    def game_attr(self):
        if getattr(self, "_game_attr", None):
            return self._game_attr
        if not getattr(self, "_game_attr_ids", None):
            return []
        self._game_attr = Modification.load(*self._game_attr_ids)
        return self._game_attr

    @game_attr.setter
    def game_attr(self, value):
        self._game_attr = None
        self._game_attr_ids = value

    @property
    def card(self):
        if not getattr(self, "_card", None):
            return None
        return tables.Tarot(self._card)

    @card.setter
    def card(self, value):
        self._card = value


class Division(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "teams":
            return "_team_ids"
        return name

    @classmethod
    def load(cls, id_):
        return cls(database.get_division(id_))

    @classmethod
    def load_all(cls):
        """
        Returns dictionary keyed by division ID
        """
        return {
            id_: cls(div) for id_, div in database.get_all_divisions().items()
        }

    @classmethod
    def load_by_name(cls, name):
        """
        Name can be full name or nickname, case insensitive.
        """
        divisions = cls.load_all()
        for division in divisions.values():
            if name in division.name:
                return division
        return None

    @property
    def teams(self):
        """
        Comes back as dictionary keyed by team ID
        """
        if self._teams:
            return self._teams
        self._teams = {id_: Team.load(id_) for id_ in self._team_ids}
        return self._teams

    @teams.setter
    def teams(self, value):
        self._teams = None
        self._team_ids = value


class Subleague(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "divisions":
            return "_division_ids"
        return name

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @classmethod
    def load(cls, id_):
        return cls(database.get_subleague(id_))

    @property
    def divisions(self):
        if self._divisions:
            return self._divisions
        self._divisions = {id_: Division.load(id_) for id_ in self._division_ids}
        return self._divisions

    @divisions.setter
    def divisions(self, value):
        self._divisions = None
        self._division_ids = value

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for division in self.divisions.values():
            self._teams.update(division.teams)
        return self._teams


class League(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "subleagues":
            return "_subleague_ids"
        if name == "tiebreakers":
            return "_tiebreakers_id"
        return name

    def __init__(self, data):
        super().__init__(data)
        self._teams = {}

    @classmethod
    def load(cls):
        return cls(database.get_league())

    @classmethod
    def load_by_id(cls, id_):
        return cls(database.get_league(id_))

    @property
    def subleagues(self):
        if self._subleagues:
            return self._subleagues
        self._subleagues = {id_: Subleague.load(id_) for id_ in self._subleague_ids}
        return self._subleagues

    @subleagues.setter
    def subleagues(self, value):
        self._subleagues = None
        self._subleague_ids = value

    @property
    def teams(self):
        if self._teams:
            return self._teams
        for subleague in self.subleagues.values():
            self._teams.update(subleague.teams)
        return self._teams

    @property
    def tiebreakers(self):
        if self._tiebreakers:
            return self._tiebreakers
        self._tiebreakers = Tiebreaker.load(self._tiebreakers_id)
        return self._tiebreakers

    @tiebreakers.setter
    def tiebreakers(self, value):
        self._tiebreakers = None
        self._tiebreakers_id = value


class Game(Base):

    @staticmethod
    def _custom_key_transform(name):
        lookup_dict = {
            "base_runners": "_base_runner_ids",
            "home_team": "_home_team_id",
            "away_team": "_away_team_id",
            "home_pitcher": "_home_pitcher_id",
            "away_pitcher": "_away_pitcher_id",
            "home_batter": "_home_batter_id",
            "away_batter": "_away_batter_id",
            "weather": "_weather",
            "statsheet": "_statsheet_id",
            "season": "_season",
            "day": "_day",
            "inning": "_inning",
            "base_runner_mods": "_base_runner_mod_ids",
            "home_pitcher_mod": "_home_pitcher_mod_id",
            "home_batter_mod": "_home_batter_mod_id",
            "away_pitcher_mod": "_away_pitcher_mod_id",
            "away_batter_mod": "_away_batter_mod_id",
        }
        if name in lookup_dict:
            return lookup_dict[name]
        return name

    @classmethod
    def load_by_id(cls, id_):
        return cls(database.get_game_by_id(id_))

    @classmethod
    def load_by_day(cls, season, day):
        return {
            id_: cls(game) for id_, game in database.get_games(season, day).items()
        }

    @classmethod
    def load_tournament_by_day(cls, tournament, day):
        return {
            id_: cls(game) for id_, game in database.get_tournament(tournament, day).items()
        }

    @classmethod
    def load_by_season(cls, season, team_id=None, day=None):
        return {
            game["gameId"]: cls(game["data"]) for game in chronicler.get_games(team_ids=team_id, season=season, day=day)
        }

    @classmethod
    def load_by_tournament(cls, tournament, team_id=None, day=None):
        return {
            game["gameId"]: cls(game["data"]) for game in chronicler.get_games(team_ids=team_id, tournament=tournament, day=day)
        }

    @property
    def winning_team(self):
        return self.home_team if self.home_score > self.away_score else self.away_team

    @property
    def winning_team_name(self):
        return self.home_team_name if self.home_score > self.away_score else self.away_team_name

    @property
    def winning_team_nickname(self):
        return self.home_team_nickname if self.home_score > self.away_score else self.away_team_nickname

    @property
    def losing_team(self):
        return self.home_team if self.home_score < self.away_score else self.away_team

    @property
    def losing_team_name(self):
        return self.home_team_name if self.home_score < self.away_score else self.away_team_name

    @property
    def losing_team_nickname(self):
        return self.home_team_nickname if self.home_score < self.away_score else self.away_team_nickname

    @property
    def winning_score(self):
        return self.home_score if self.home_score > self.away_score else self.away_score

    @property
    def losing_score(self):
        return self.home_score if self.home_score < self.away_score else self.away_score

    @property
    def base_runners(self):
        if self._base_runners:
            return self._base_runners
        if not self._base_runner_ids:
            return []
        players = Player.load(*self._base_runner_ids)
        self._base_runners = [players.get(id_) for id_ in self._base_runner_ids]
        return self._base_runners

    @base_runners.setter
    def base_runners(self, value):
        if getattr(self, '_base_runner_ids', None) == value:
            return
        self._base_runners = None
        self._base_runner_ids = value

    @property
    def weather(self):
        return tables.Weather(self._weather)

    @weather.setter
    def weather(self, value):
        self._weather = value

    @property
    def home_team(self):
        if self._home_team:
            return self._home_team
        self._home_team = Team.load(self._home_team_id)
        return self._home_team

    @home_team.setter
    def home_team(self, value):
        self._home_team = None
        self._home_team_id = value

    @property
    def away_team(self):
        if self._away_team:
            return self._away_team
        self._away_team = Team.load(self._away_team_id)
        return self._away_team

    @away_team.setter
    def away_team(self, value):
        self._away_team = None
        self._away_team_id = value

    @property
    def home_pitcher(self):
        if self._home_pitcher:
            return self._home_pitcher
        self._home_pitcher = Player.load_one(self._home_pitcher_id)
        return self._home_pitcher

    @home_pitcher.setter
    def home_pitcher(self, value):
        self._home_pitcher = None
        self._home_pitcher_id = value

    @property
    def away_pitcher(self):
        if self._away_pitcher:
            return self._away_pitcher
        self._away_pitcher = Player.load_one(self._away_pitcher_id)
        return self._away_pitcher

    @away_pitcher.setter
    def away_pitcher(self, value):
        self._away_pitcher = None
        self._away_pitcher_id = value

    @property
    def home_batter(self):
        if not self._home_batter_id:
            return None
        if self._home_batter:
            return self._home_batter
        self._home_batter = Player.load_one(self._home_batter_id)
        return self._home_batter

    @home_batter.setter
    def home_batter(self, value):
        self._home_batter = None
        self._home_batter_id = value

    @property
    def away_batter(self):
        if not self._away_batter_id:
            return None
        if self._away_batter:
            return self._away_batter
        self._away_batter = Player.load_one(self._away_batter_id)
        return self._away_batter

    @away_batter.setter
    def away_batter(self, value):
        self._away_batter = None
        self._away_batter_id = value

    @property
    def at_bat_team(self):
        if self.top_of_inning:
            return self.away_team
        else:
            return self.home_team

    @property
    def at_bat_team_name(self):
        if self.top_of_inning:
            return self.away_team_name
        else:
            return self.home_team_name

    @property
    def at_bat_team_nickname(self):
        if self.top_of_inning:
            return self.away_team_nickname
        else:
            return self.home_team_nickname

    @property
    def pitching_team(self):
        if self.top_of_inning:
            return self.home_team
        else:
            return self.away_team

    @property
    def pitching_team_name(self):
        if self.top_of_inning:
            return self.home_team_name
        else:
            return self.away_team_name

    @property
    def pitching_team_nickname(self):
        if self.top_of_inning:
            return self.home_team_nickname
        else:
            return self.away_team_nickname

    @property
    def current_pitcher(self):
        if self.top_of_inning:
            return self.home_pitcher
        else:
            return self.away_pitcher

    @property
    def current_pitcher_name(self):
        if self.top_of_inning:
            return self.home_pitcher_name
        else:
            return self.away_pitcher_name

    @property
    def current_batter(self):
        if self.top_of_inning:
            return self.away_batter
        else:
            return self.home_batter

    @property
    def current_batter_name(self):
        if self.top_of_inning:
            return self.away_batter_name
        else:
            return self.home_batter_name

    @property
    def season(self):
        return self._season

    @season.setter
    def season(self, value):
        self._season = value + 1

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        self._day = value + 1

    @property
    def inning(self):
        return self._inning

    @inning.setter
    def inning(self, value):
        self._inning = value + 1

    @property
    def statsheet(self):
        if self._statsheet:
            return self._statsheet
        self._statsheet = GameStatsheet.load(self._statsheet_id)[self._statsheet_id]
        return self._statsheet

    @statsheet.setter
    def statsheet(self, value):
        self._statsheet = None
        self._statsheet_id = value

    @property
    def base_runner_mods(self):
        if getattr(self, "_base_runner_mods", None):
            return self._base_runner_mods
        if not getattr(self, "_base_runner_mod_ids", None):
            return []
        self._base_runner_mods = Modification.load(*self._base_runner_mod_ids)
        return self._base_runner_mods

    @base_runner_mods.setter
    def base_runner_mods(self, value):
        self._base_runner_mods = None
        self._base_runner_mod_ids = value

    @property
    def home_pitcher_mod(self):
        if getattr(self, "_home_pitcher_mod", None):
            return self._home_pitcher_mod
        self._home_pitcher_mod = Modification.load_one(getattr(self, "_home_pitcher_mod_id", None))
        return self._home_pitcher_mod

    @home_pitcher_mod.setter
    def home_pitcher_mod(self, value):
        self._home_pitcher_mod = None
        self._home_pitcher_mod_id = value

    @property
    def home_batter_mod(self):
        if getattr(self, "_home_batter_mod", None):
            return self._home_batter_mod
        self._home_batter_mod = Modification.load_one(getattr(self, "_home_batter_mod_id", None))
        return self._home_batter_mod

    @home_batter_mod.setter
    def home_batter_mod(self, value):
        self._home_batter_mod = None
        self._home_batter_mod_id = value

    @property
    def away_pitcher_mod(self):
        if getattr(self, "_away_pitcher_mod", None):
            return self._away_pitcher_mod
        self._away_pitcher_mod = Modification.load_one(getattr(self, "_away_pitcher_mod_id", None))
        return self._away_pitcher_mod

    @away_pitcher_mod.setter
    def away_pitcher_mod(self, value):
        self._away_pitcher_mod = None
        self._away_pitcher_mod_id = value

    @property
    def away_batter_mod(self):
        if getattr(self, "_away_batter_mod", None):
            return self._away_batter_mod
        self._away_batter_mod = Modification.load_one(getattr(self, "_away_batter_mod_id", None))
        return self._away_batter_mod

    @away_batter_mod.setter
    def away_batter_mod(self, value):
        self._away_batter_mod = None
        self._away_batter_mod_id = value


class Fight(Game):
    pass  # will probalby need this eventually.


class DecreeResult(Base):

    @classmethod
    def load(cls, *ids):
        decrees = database.get_offseason_decree_results(list(ids))
        return {
            id_: cls(decree) for (id_, decree) in decrees.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)


class BlessingResult(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "team_id":
            return "_team_id"
        if name == "highest_team":
            return "_highest_team_id"
        return name

    @classmethod
    def load(cls, *ids):
        blessings = database.get_offseason_bonus_results(list(ids))
        return {
            id_: cls(blessing) for (id_, blessing) in blessings.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)

    @property
    def team_id(self):
        if self._team:
            return self._team
        if not self._team_id:
            return None
        self._team = Team.load(self._team_id)
        return self._team

    @team_id.setter
    def team_id(self, value):
        self._team = None
        self._team_id = value

    # team is an alias to team_id
    @property
    def team(self):
        return self.team_id

    # Note: highest_team not present for Season 1
    @property
    def highest_team(self):
        if self._highest_team:
            return self._highest_team
        if not self._highest_team_id:
            return None
        self._highest_team = Team.load(self._highest_team_id)
        return self._highest_team

    @highest_team.setter
    def highest_team(self, value):
        self._highest_team = None
        self._highest_team_id = value

    # blessing_title is an alias to bonus_title
    @property
    def blessing_title(self):
        return self.bonus_title

    # blessing_id is an alias to bonus_id
    @property
    def blessing_id(self):
        return self.bonus_id


class TidingResult(Base):

    @classmethod
    def load(cls, *ids):
        event = database.get_offseason_event_results(list(ids))
        return {
            id_: cls(event) for (id_, event) in event.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)

EventResult = TidingResult


class ElectionResult(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "bonus_results":
            return "_bonus_results_ids"
        if name == "decree_results":
            return "_decree_results_ids"
        if name == "event_results":
            return "_event_results_ids"
        return name

    @classmethod
    def load_by_season(cls, season):
        return cls(database.get_offseason_recap(season))

    @property
    def bonus_results(self):
        if self._bonus_results:
            return self._bonus_results
        if not self._bonus_results_ids:
            return []
        blessings = BlessingResult.load(*self._bonus_results_ids)
        self._bonus_results = [blessings.get(id_) for id_ in self._bonus_results_ids]
        return self._bonus_results

    @bonus_results.setter
    def bonus_results(self, value):
        self._bonus_results = None
        self._bonus_results_ids = value

    # blessing_results is an alias to bonus_results
    @property
    def blessing_results(self):
        return self.bonus_results

    @property
    def decree_results(self):
        if self._decree_results:
            return self._decree_results
        if not self._decree_results_ids:
            return []
        decrees = DecreeResult.load(*self._decree_results_ids)
        self._decree_results = [decrees.get(id_) for id_ in self._decree_results_ids]
        return self._decree_results

    @decree_results.setter
    def decree_results(self, value):
        self._decree_results = None
        self._decree_results_ids = value

    @property
    def event_results(self):
        if self._event_results:
            return self._event_results
        if not self._event_results_ids:
            return []
        events = TidingResult.load(*self._event_results_ids)
        self._event_results = [events.get(id_) for id_ in self._event_results_ids]
        return self._event_results

    @event_results.setter
    def event_results(self, value):
        self._event_results = None
        self._event_results_ids = value

    # tiding_results is an alias to event_results
    @property
    def tiding_results(self):
        return self.event_results

OffseasonResult = ElectionResult


class Playoff(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "rounds":
            return "_rounds_ids"
        if name == "winner":
            return "_winner_id"
        if name == "season":
            return "_season"
        return name

    @classmethod
    def load_by_season(cls, season):
        playoff = database.get_playoff_details(season)
        return cls(playoff)

    @property
    def rounds(self):
        if self._rounds:
            return self._rounds
        self._rounds = [PlayoffRound.load(id_) for id_ in self._rounds_ids]
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        self._rounds = None
        self._rounds_ids = value

    def get_round_by_number(self, round_number):
        """
        Get games from a specific round of playoffs
        Round number is 1-indexed
        """
        num = round_number - 1
        if num >= len(self._rounds_ids) or num < 0:
            return None
        return self.rounds[num]

    @property
    def winner(self):
        if self._winner:
            return self._winner
        self._winner = Team.load(self._winner_id)
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = None
        self._winner_id = value


class PlayoffRound(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "games":
            return "_game_ids_ids"
        if name == "matchups":
            return "_matchups_ids"
        if name == "winners":
            return "_winners_ids"
        return name

    @classmethod
    def load(cls, id_):
        round_ = database.get_playoff_round(id_)
        return cls(round_)

    @property
    def games(self):
        """
        Get all games
        Lots of endpoint calls, not recommended
        """
        if all(self._games):
            return self._games
        for day, games in enumerate(self._games_ids):
            if self._games[day]:
                continue
            self._games[day] = [Game.load_by_id(id_) for id_ in games if id_ != "none"]
        return self._games

    @games.setter
    def games(self, value):
        self._games = [None] * len(value)
        self._games_ids = value

    def get_games_by_number(self, game_number):
        """
        Get games by game number in series (IE: Game 1 of 5)
        Game number is 1-indexed
        """
        num = game_number - 1
        if num >= len(self._games_ids) or num < 0:
            return []
        if self._games[num]:
            return self._games[num]
        self._games[num] = [Game.load_by_id(id_) for id_ in self._games_ids[num] if id_ != "none"]
        return self._games[num]

    @property
    def matchups(self):
        if self._matchups:
            return self._matchups
        matchups = PlayoffMatchup.load(*self._matchups_ids)
        self._matchups = [matchups.get(id_) for id_ in self._matchups_ids]
        return self._matchups

    @matchups.setter
    def matchups(self, value):
        self._matchups = None
        self._matchups_ids = value

    @property
    def winners(self):
        if self._winners:
            return self._winners
        self._winners = [Team.load(x) for x in self._winners_ids]
        return self._winners

    @winners.setter
    def winners(self, value):
        self._winners = None
        self._winners_ids = value


class PlayoffMatchup(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "home_team":
            return "_home_team_id"
        if name == "away_team":
            return "_away_team_id"
        return name

    @classmethod
    def load(cls, *ids_):
        matchups = database.get_playoff_matchups(list(ids_))
        return {
            id_: cls(matchup) for (id_, matchup) in matchups.items()
        }

    @classmethod
    def load_one(cls, id_):
        return cls.load(id_).get(id_)

    @property
    def away_team(self):
        if self._away_team:
            return self._away_team
        self._away_team = Team.load(self._away_team_id)
        return self._away_team

    @away_team.setter
    def away_team(self, value):
        self._away_team = None
        self._away_team_id = value

    @property
    def home_team(self):
        if self._home_team:
            return self._home_team
        self._home_team = Team.load(self._home_team_id)
        return self._home_team

    @home_team.setter
    def home_team(self, value):
        self._home_team = None
        self._home_team_id = value


class Election(Base):

    @classmethod
    def load(cls):
        offseason = database.get_offseason_election_details()
        return cls(offseason)

OffseasonSetup = Election


class Standings(Base):

    @classmethod
    def load(cls, id_):
        standings = database.get_standings(id_)
        return cls(standings)

    def get_standings_by_team(self, id_):
        return {"wins": self.wins.get(id_, None), "losses": self.losses.get(id_, None)}


class Season(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "league":
            return "_league_id"
        if name == "standings":
            return "_standings_id"
        if name == "stats":
            return "_stats_id"
        if name == "season_number":
            return "_season_number"
        return name

    @classmethod
    def load(cls, season_number):
        season = database.get_season(season_number)
        return cls(season)

    @property
    def league(self):
        if self._league:
            return self._league
        self._league = League.load_by_id(self._league_id)
        return self._league

    @league.setter
    def league(self, value):
        self._league = None
        self._league_id = value

    @property
    def standings(self):
        if self._standings:
            return self._standings
        self._standings = Standings.load(self._standings_id)
        return self._standings

    @standings.setter
    def standings(self, value):
        self._standings = None
        self._standings_id = value

    @property
    def stats(self):
        if self._stats:
            return self._stats
        self._stats = SeasonStatsheet.load(self._stats_id)[self._stats_id]
        return self._stats

    @stats.setter
    def stats(self, value):
        self._stats_id = value
        self._stats = None


class Tiebreaker(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "order":
            return "_order_ids"
        return name

    @classmethod
    def load(cls, id):
        tiebreakers = database.get_tiebreakers(id)
        return {
            id_: cls(tiebreaker) for (id_, tiebreaker) in tiebreakers.items()
        }

    @property
    def order(self):
        if self._order:
            return self._order
        self._order = OrderedDict()
        for id_ in self._order_ids:
            self._order[id_] = Team.load(id_)
        return self._order

    @order.setter
    def order(self, value):
        self._order = None
        self._order_ids = value


class Idol(Base):

    @classmethod
    def load(cls):
        idols = database.get_idols()
        idols_dict = OrderedDict()
        for idol in idols:
            idols_dict[idol['playerId']] = cls(idol)
        return idols_dict

    @property
    def player(self):
        if getattr(self, '_player', None):
            return self._player
        self._player = Player.load_one(self.player_id)
        return self._player

    @player.setter
    def player(self, value):
        self._player = value


class Tribute(Base):

    @classmethod
    def load(cls):
        tributes = database.get_tributes()
        tributes_dict = OrderedDict()
        for tribute in tributes:
            tributes_dict[tribute['playerId']] = cls(tribute)
        return tributes_dict

    @classmethod
    def load_at_time(cls, time):
        if isinstance(time, str):
            time = parse(time)

        tributes = chronicler.get_tribute_updates(before=time, order="desc", count=1)

        # Sort output by number of peanuts
        tributes = tributes[0]["players"]
        data = OrderedDict(sorted(tributes.items(), key=lambda t: t[1], reverse=True))

        tributes_dict = OrderedDict()
        for key, value in data.items():
            tributes_dict[key] = cls({"player_id": key, "peanuts": value, "timestamp": time})
        return tributes_dict

    @property
    def player(self):
        if getattr(self, '_player', None):
            return self._player
        if getattr(self, "timestamp", None):
            self._player = Player.load_one_at_time(self.player_id, self.timestamp)
        else:
            self._player = Player.load_one(self.player_id)
        return self._player

    @player.setter
    def player(self, value):
        self._player = value


class PlayerStatsheet(Base):

    @classmethod
    def load(cls, ids):
        stats = database.get_player_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict


class TeamStatsheet(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "player_stats":
            return "_player_stat_ids"
        return name

    @classmethod
    def load(cls, ids):
        stats = database.get_team_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict

    @property
    def player_stats(self):
        if self._player_stats:
            return self._player_stats
        self._player_stats = list(PlayerStatsheet.load(self._player_stat_ids).values())
        return self._player_stats

    @player_stats.setter
    def player_stats(self, ids):
        self._player_stat_ids = ids
        self._player_stats = None


class SeasonStatsheet(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "team_stats":
            return "_team_stat_ids"
        return name

    @classmethod
    def load(cls, ids):
        stats = database.get_season_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict

    @classmethod
    def load_by_season(cls, season):
        """Season is 1 indexed."""
        season = Season.load(season)
        return season.stats

    @property
    def team_stats(self):
        if self._team_stats:
            return self._team_stats
        self._team_stats = list(TeamStatsheet.load(self._team_stat_ids).values())
        return self._team_stats

    @team_stats.setter
    def team_stats(self, value):
        self._team_stats = None
        self._team_stat_ids = value


class GameStatsheet(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "home_team_stats":
            return "_home_team_stats_id"
        if name == "away_team_stats":
            return "_away_team_stats_id"
        return name

    @classmethod
    def load(cls, ids):
        stats = database.get_game_statsheets(ids)
        stats_dict = OrderedDict()
        for k, v in stats.items():
            stats_dict[k] = cls(v)
        return stats_dict

    @classmethod
    def load_by_day(cls, season, day):
        games = Game.load_by_day(season, day)
        return {k: g.statsheet for k, g in games.items()}

    def team_stats(self):
        if getattr(self, '_team_stats', None):
            return self._team_stats
        self._team_stats = TeamStatsheet.load([
            self._home_team_stats_id,
            self._away_team_stats_id,
        ])
        return self._team_stats

    @property
    def away_team_stats(self):
        return self.team_stats()[self._away_team_stats_id]

    @away_team_stats.setter
    def away_team_stats(self, value):
        self._away_team_stats_id = value
        self._team_stats = None

    @property
    def home_team_stats(self):
        return self.team_stats()[self._home_team_stats_id]

    @home_team_stats.setter
    def home_team_stats(self, value):
        self._home_team_stats_id = value
        self._team_stats = None


class Modification(Base):

    @classmethod
    def load(cls, *ids):
        return [cls(mod) for mod in database.get_attributes(list(ids))]

    @classmethod
    def load_one(cls, id_):
        if id_ in (None, "NONE", ""):
            return None
        return cls.load(id_)[0]


class Item(Base):

    @staticmethod
    def _custom_key_transform(name):
        if name == "attr":
            return "_attr"
        return name

    @classmethod
    def load(cls, *ids):
        return [cls(item) for item in database.get_items(list(ids))]

    @classmethod
    def load_one(cls, id_):
        if id_ is None:
            return cls({"id": id_, "name": "None?", "attr": "NONE"})
        if id_ == "":
            return cls({"id": id_, "name": "None", "attr": "NONE"})
        return cls.load(id_)[0]

    @property
    def attr(self):
        return Modification.load_one(self._attr)

    @attr.setter
    def attr(self, value):
        self._attr = value
