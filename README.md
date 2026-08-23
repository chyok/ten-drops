# Ten Drops

![GitHub License](https://img.shields.io/github/license/chyok/ten-drops)
![PyPI - Version](https://img.shields.io/pypi/v/ten-drops)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ten-drops)

A ten drops game written in pygame-ce.  
Click on these water droplets to make them explode until the screen is cleared.

The inspiration and assets all come from the Flash game "Splash Back".

![example](https://github.com/chyok/ten-drops/assets/32629225/b8409169-dd31-4912-a91e-5fed288a833c)

## How to play

- Clicking a drop makes it grow and costs one drop from your supply.
- A fully grown drop bursts into four droplets that fly up, down, left and right,
  growing (or bursting) every drop they hit.
- Clicking an empty cell places a new small drop, which also costs one drop.
- Long chain reactions earn extra drops: one for every third burst,
  and one for every burst after the 21st.
- Clear the board to reach the next level and get two more drops.
  The game is over when you run out of drops.

## Installation

### use pip

Requires Python 3.10 or later.

```bash
pip install ten-drops
```

Then start the game with:

```bash
ten-drops
```

### binary file

Binary files for Windows that can be directly executed to play the game.

| Platform | Download Link                                           |
|----------|---------------------------------------------------------|
| Windows  | [Download](https://github.com/chyok/ten-drops/releases) |

### from source

```bash
git clone https://github.com/chyok/ten-drops.git
cd ten-drops
pip install .
python main.py
```

## Release

Bump `version` in `pyproject.toml`, then push a matching tag:

```bash
git tag v1.0.4
git push origin v1.0.4
```

The release workflow builds the Windows binary, publishes the package to PyPI
and creates the GitHub release.

## License

This project is licensed under the [MIT License](LICENSE).
