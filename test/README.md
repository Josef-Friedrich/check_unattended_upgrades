# Calculations

```
WARNING = 93600s = 26h = 1d + 2h
CRITICAL = 187200s = 52h = 2d + 4h
```

```
CURRENT = 1504523830 = 2017-09-04 13:17:10
```


```
OK_FIRST
  = CURRENT
  = 1504523830
  = 2017-09-04 13:17:10
  DIFF: 0

OK_LAST
  = CURRENT - WARNING + 1
  = 1504523830 - 93600 + 1
  = 1504430231
  = 2017-09-03 11:17:11
  DIFF: 93599

WARNING_FIRST
  = CURRENT - WARNING
  = 1504523830 - 93600
  = 1504430230
  = 2017-09-03 11:17:10
  DIFF: 93600

WARNING_LAST
  = CURRENT - CRITICAL + 1
  = 1504523830 - 187200 + 1
  = 1504336631
  = 2017-09-02 09:17:11
  DIFF: 187199

CRITICAL_FIRST
  = CURRENT - CRITICAL
  = 1504523830 - 187200
  = 1504336630
  = 2017-09-02 09:17:10
  DIFF: 187200
```

```
                                 CURRENT
-----------|-----------|-----------|
           ..          ..          .
           ^.          ..          ^
RUN_CRITICAL_FIRST     .^      RUN_OK_FIRST
            .          ^ RUN_OK_LAST
            ^  RUN_WARNING_FIRST
     RUN_WARNING_LAST

 CRITICAL <| WARNING <|   OK
```
