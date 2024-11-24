#!/bin/bash
python -m prisma migrate deploy
python -m seeds.candles