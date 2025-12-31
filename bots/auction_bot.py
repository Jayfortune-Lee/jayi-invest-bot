name: Auction Jayi Bot Daily

on:
  schedule:
    - cron: '21 21 * * *' # UTC 21시 = KST 06시
  workflow_dispatch:

jobs:
  run-auction-bot:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.10.13
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run Auction Bot
        env:
          TG_TOKEN_AUCTION: ${{ secrets.TG_TOKEN_AUCTION }}
          TG_ID: ${{ secrets.TG_ID }}
          PYTHONPATH: ${{ github.workspace }}
        run: python -m bots.auction_bot
