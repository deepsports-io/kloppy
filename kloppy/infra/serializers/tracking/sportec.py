import logging
from collections import defaultdict
from typing import Dict, Tuple

from kloppy.domain import (
    AttackingDirection,
    BallState,
    DatasetFlag,
    Dimension,
    Frame,
    Ground,
    Metadata,
    Orientation,
    Period,
    PitchDimensions,
    Player,
    Point,
    Provider,
    Team,
    TrackingDataset,
    attacking_direction_from_frame,
)
from kloppy.utils import Readable, performance_logging
from lxml import objectify

from . import TrackingDataSerializer

logger = logging.getLogger(__name__)


class SportecSerializer(TrackingDataSerializer):
    # @classmethod
    # def _frame_from_line(cls, teams, period, line, frame_rate):
    #     line = str(line)
    #     frame_id, players, ball = line.strip().split(":")[:3]

    #     players_coordinates = {}

    #     for player_data in players.split(";")[:-1]:
    #         team_id, target_id, jersey_no, x, y, speed = player_data.split(",")
    #         team_id = int(team_id)

    #         if team_id == 1:
    #             team = teams[0]
    #         elif team_id == 0:
    #             team = teams[1]
    #         else:
    #             # it's probably -1, but make sure it doesn't crash
    #             continue

    #         player = team.get_player_by_jersey_number(jersey_no)

    #         if not player:
    #             player = Player(
    #                 player_id=f"{team.ground}_{jersey_no}",
    #                 team=team,
    #                 jersey_no=int(jersey_no),
    #             )
    #             team.players.append(player)

    #         players_coordinates[player] = Point(float(x), float(y))

    #     (
    #         ball_x,
    #         ball_y,
    #         ball_z,
    #         ball_speed,
    #         ball_owning_team,
    #         ball_state,
    #     ) = ball.rstrip(";").split(",")[:6]

    #     frame_id = int(frame_id)

    #     if ball_owning_team == "H":
    #         ball_owning_team = teams[0]
    #     elif ball_owning_team == "A":
    #         ball_owning_team = teams[1]
    #     else:
    #         raise Exception(f"Unknown ball owning team: {ball_owning_team}")

    #     if ball_state == "Alive":
    #         ball_state = BallState.ALIVE
    #     elif ball_state == "Dead":
    #         ball_state = BallState.DEAD
    #     else:
    #         raise Exception(f"Unknown ball state: {ball_state}")

    #     return Frame(
    #         frame_id=frame_id,
    #         timestamp=frame_id / frame_rate - period.start_timestamp,
    #         ball_coordinates=Point(float(ball_x), float(ball_y)),
    #         ball_state=ball_state,
    #         ball_owning_team=ball_owning_team,
    #         players_coordinates=players_coordinates,
    #         period=period,
    #     )

    @staticmethod
    def __validate_inputs(inputs: Dict[str, Readable]):
        if "metadata" not in inputs:
            raise ValueError("Please specify a value for 'metadata'")
        if "raw_data" not in inputs:
            raise ValueError("Please specify a value for 'raw_data'")

    def deserialize(
        self, inputs: Dict[str, Readable], options: Dict = None
    ) -> TrackingDataset:
        pass

        self.__validate_inputs(inputs)

        if not options:
            options = {}

        # sample_rate = float(options.get("sample_rate", 25.0))
        #     limit = int(options.get("limit", 0))
        #     only_alive = bool(options.get("only_alive", True))

        #     # TODO: also used in Metrica, extract to a method
        #     home_team = Team(team_id="home", name="home", ground=Ground.HOME)
        #     away_team = Team(team_id="away", name="away", ground=Ground.AWAY)
        #     teams = [home_team, away_team]

        with performance_logging("Loading metadata", logger=logger):
            match = objectify.fromstring(inputs["metadata"].read())

        #         frame_rate = int(match.attrib["iFrameRateFps"])
        #         pitch_size_width = float(match.attrib["fPitchXSizeMeters"])
        #         pitch_size_height = float(match.attrib["fPitchYSizeMeters"])

        #         periods = []
        #         for period in match.iterchildren(tag="period"):
        #             start_frame_id = int(period.attrib["iStartFrame"])
        #             end_frame_id = int(period.attrib["iEndFrame"])
        #             if start_frame_id != 0 or end_frame_id != 0:
        #                 periods.append(
        #                     Period(
        #                         id=int(period.attrib["iId"]),
        #                         start_timestamp=start_frame_id / frame_rate,
        #                         end_timestamp=end_frame_id / frame_rate,
        #                     )
        #                 )

        with performance_logging("Loading data", logger=logger):
            raw_data_root = objectify.fromstring(inputs["raw_data"].read())
            # pitch = PitchDimension()
            print(dir(raw_data_root))
            frames = defaultdict(dict)
            print(raw_data_root.tag)
            print(raw_data_root.Positions)
            for frameSet in raw_data_root.Positions.FrameSet:
                print(frameSet.attrib)
                for frame in frameSet.Frame:
                    pass
                    # frames[frame.attrib["N"]]
                    # print(frame.N)
                    # print(frame.tag)
                #    print()
                # print(frameSet.tag)
                # print(frameSet.attrib)
            # print(dir(raw_data_root.FrameSet))

        metadata = Metadata(
            teams=None,
            periods=None,
            pitch_dimensions=None,
            score=None,
            frame_rate=None,
            orientation=None,
            provider=Provider.SPORTEC,
            flags=None,
        )

        return TrackingDataset(
            records=frames,
            metadata=metadata,
        )

    def serialize(self, dataset: TrackingDataset) -> Tuple[str, str]:
        raise NotImplementedError
