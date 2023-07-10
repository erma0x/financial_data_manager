#!/bin/bash

# Lista degli elementi da sostituire
symbols=("SPY" "AAPL" "EURUSD=X" "NVDA" "QQQ")

mkdir -p logs

# Itera attraverso la lista
for symbol in "${symbols[@]}"
do
  # Percorsi dei file di log
  output_log="logs/${symbol}_1m_output.log"
  error_log="logs/${symbol}_1m_error.log"

  # Crea i file di log se non esistono
  touch "$output_log"
  touch "$error_log"

  # Esegui il comando sostituendo il valore "DOGEUSDT" con l'elemento corrente
  nohup python3 ./source/data_manager_yfinance.py "$symbol" 1m >> "./logs/${symbol}_1m_output.log" 2>> "./logs/${symbol}_1m_error.log" &
done
