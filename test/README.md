# Calculations

```
WARNING = 93600s = 26h = 1d + 2h
CRITICAL = 187200s = 52h = 2d + 4h
```


CURRENT 1504523830

```
RUN_OK_FIRST = CURRENT = 1504523830
RUN_OK_LAST = CURRENT - WARNING + 1 = 1504523830 - 93600 + 1 = 1504430231
RUN_WARNING_FIRST = CURRENT - WARNING = 1504523830 - 93600 = 1504430230
RUN_WARNING_LAST = CURRENT - CRITICAL + 1 = 1504523830 - 187200 + 1 = 1504336631
RUN_CRITICAL_FIRST = CURRENT - CRITICAL = 1504523830 - 187200 = 1504336630
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

                   |
                  RUN

```
