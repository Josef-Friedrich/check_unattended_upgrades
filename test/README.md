# Calculations

```
WARNING = 93600s = 26h = 1d + 2h
CRITICAL = 187200s = 52h = 2d + 4h
```


CURRENT 1504523830

```
RUN_OK_FIRST = CURRENT = CURRENT
RUN_OK_LAST = CURRENT - WARNING + 1
RUN_WARNING_FIRST = CURRENT - WARNING
RUN_WARNING_LAST =  CURRENT - CRITICAL + 1
RUN_CRITICAL_FIRST = CURRENT - CRITICAL
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
