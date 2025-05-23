# SpeedTest++

A Python implementation of a command-line internet speed testing tool. This project is designed to provide accurate measurements of your internet connection's performance, including download speed, upload speed, and latency.

## Features

- 🚀 Fast and accurate speed testing
- 📊 Multi-threaded testing for better performance
- 🌐 Automatic server selection based on ping and location
- 📈 Detailed performance metrics
- 🔧 Configurable test parameters
- 📝 Multiple output formats (text, JSON)

## Installation

### Requirements
- Python 3.7 or higher
- pip package manager

### Install from source
```bash
git clone https://github.com/cociweb/speedtest-pypy.git
cd speedtest-pypy
pip install -e .
```

## Usage

Basic speed test:
```bash
speedtest++
```

Options:
```bash
speedtest++ --help                    # Show help message
speedtest++ --latency                # Test latency only
speedtest++ --download               # Test download only
speedtest++ --upload                 # Test upload only
speedtest++ --server SERVER_ID       # Use specific server
speedtest++ --threads N              # Set number of threads
speedtest++ --json                   # Output in JSON format
```

## Example Output
```
Server: New York City, NY
Latency: 15.23 ms
Download: 100.45 Mbps
Upload: 50.32 Mbps
```

## Development

### Setting up development environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running tests
```bash
python -m pytest speedtest-pypy/tests/
```

### Running tests with coverage
```bash
python -m pytest --cov=speedtest-pypy speedtest-pypy/tests/
```

## Project Structure
```
speedtest-pypy/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── speedtest-pypy/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── core.py
│   ├── models.py
│   ├── network.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_core.py
│   │   ├── test_network.py
│   │   └── test_utils.py
│   └── utils.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original C++ SpeedTest++ project
- Speedtest.net for their testing methodology
- Contributors and maintainers

## Author

cociweb

## Version

Current version: 1.0.0