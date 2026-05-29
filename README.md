# Oaksmith Multi-Threaded Code Generator & Validator

This repository contains a Python script designed to generate and validate codes for the Oaksmith campaign. It uses multi-threading to speed up the validation process.

## Features
- **Random Code Generation**: Generates codes with a specific prefix (`MGTQ`).
- **Multi-Threading**: Utilizes `concurrent.futures.ThreadPoolExecutor` for parallel processing.
- **Real-time Logging**: Prints the status of each code being tested.
- **Automatic Saving**: Saves valid codes to `valid_codes.txt`.

## Prerequisites
- Python 3.x
- `requests` library

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/zaidhu/campaign-script-repo.git
   cd campaign-script-repo
   ```
2. Install dependencies:
   ```bash
   pip install requests
   ```

## Usage
1. Open `campaign.py` and configure the following variables if needed:
   - `TEST_MOBILE`: The mobile number to use for validation.
   - `NUM_CODES`: The total number of codes to generate and test.
   - `MAX_WORKERS`: Number of concurrent threads (default is 10).
2. Run the script:
   ```bash
   python campaign.py
   ```

## Important Note
If you encounter **403 Forbidden** errors, it means the server has detected the high volume of requests and is rate-limiting or blocking your IP. Consider increasing `DELAY_PER_THREAD` or using a proxy if necessary.

---
*Made By Frozen @SpeakeMarin. Please share with full credit.*
