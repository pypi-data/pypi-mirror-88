from enum import IntEnum


class Status(IntEnum):
    ok = 0
    success = 1

    empty = -10
    null = -11
    none = -12
    undefined = -13
    unknown = -14

    failed = -20
    retry = -21
    exit = -22

    passed = 20
    checked = 21
    marked = 22
    flagged = 23
    found = 24

    next = 30
    continuing = 31
    breaking = 32

    on = 40
    off = -40

    valid = 41
    invalid = -41

    auto = 42
    manual = -42

    enable = 43
    disable = -43

    start = 44
    pause = 45
    stop = -44

    init = 60
    first = 61
    last = 62
    default = 63
    others = 64

    connected = 70
    disconnected = -70
    timeout = -71
    free = 72
    busy = -72

    added = 80
    existing = 81
    removed = 82

    confirm = 90
    ignore = 91
    cancel = 92

    debug = 100
    info = 101
    warning = -102
    exception = -103
    error = -104

    level0 = 1000
    level1 = 1001
    level2 = 1002
    level3 = 1003
    level4 = 1004
    level5 = 1005
    level6 = 1006
    level7 = 1007
    level8 = 1008
    level9 = 1009

    index0 = 1100
    index1 = 1101
    index2 = 1102
    index3 = 1103
    index4 = 1104
    index5 = 1105
    index6 = 1106
    index7 = 1107
    index8 = 1108
    index9 = 1109
