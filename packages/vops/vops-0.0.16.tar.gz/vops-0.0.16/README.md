# Options
This python project uses data from yahoo finance to graph option profit-loss diagrams

## Installing
Installing with pip:
```bash
pip install gops
```

## Usage
Simple program graphing a long call option:
```python
import options

contractName = 'AMD201218C00040000'
optionObj = options.scrapeCallOptions('AMD')

options.graphLongCall(optionObj, contractName)
```
