# Calculations

```
WARNING = 93600s = 26h = 1d + 2h
CRITICAL = 187200s = 52h = 2d + 4h
```

```
LAST_RUN = 2017-09-01 09:55:34 = 1504252534
```

CURRENT

## CURRENT_OK

```
CURRENT_OK < LAST_RUN + CHECK_WARNING
```

## CURRENT_WARNING

```
CURRENT_WARNING > LAST_RUN + CHECK_WARNING and < LAST_RUN + CHECK_CRITICAL
```

# CURRENT_CRITICAL

```
CURRENT_CRITICAL > LAST_RUN + CHECK_CRITICAL
```

```
                                   CURRENT
--------------|----------|-----------|

< critical    |< warning |<   ok


                   |
                LAST_RUN

```
