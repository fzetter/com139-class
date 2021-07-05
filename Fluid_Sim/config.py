import math

# int: interval
# dir: direction
# pos: position

class Config:

    def __init__(self):
        self.data = {
            "densities": [
                {
                    "value": 200,
                    "pos": {
                        "x": {"start": 15, "end": 20},
                        "y": {"start": 15, "end": 20}
                    }
                },
                {
                    "value": 400,
                    "pos": {
                        "x": {"start": 40, "end": 50},
                        "y": {"start": 15, "end": 25}
                    }
                },
                {
                    "value": 600,
                    "pos": {
                        "x": {"start": 20, "end": 35},
                        "y": {"start": 30, "end": 40}
                    }
                }
            ],
            "velocities": [
                {
                    "int": [0,60],
                    "dir": {"x": "0", "y": "5",
                    },
                    "pos": {
                        "x": "30+int(math.cos(i)*10)",
                        "y": "i",
                    }
                },
                {
                    "int": [-1,-1],
                    "dir": {
                        "x": "15 * math.cos(i)",
                        "y": "15 * math.sin(i)"
                    },
                    "pos": {
                        "x": "int(15 * math.cos(i) + 30)",
                        "y": "int(15 * math.sin(i) + 30)",
                    }
                },
                {
                    "int": [0,30],
                    "dir": {"x": "-2", "y": "2",
                    },
                    "pos": {
                        "x": "-2*i",
                        "y": "2*i",
                    }
                },
                {
                    "int": [0,30],
                    "dir": {"x": "-2", "y": "-2",
                    },
                    "pos": {
                        "x": "-2*i",
                        "y": "-2*i",
                    }
                }
            ],
            "objects": [
                {
                    "pos": { "x": 30, "y": 30},
                    "len": 10
                },
                {
                    "pos": { "x": 0, "y": 0},
                    "len": 10
                },
                {
                    "pos": { "x": 0, "y": 40},
                    "len": 10
                }
            ]
        }
