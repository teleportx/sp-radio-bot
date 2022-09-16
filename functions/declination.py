exceptions = ('11', '12', '13', '14')


def seconds(number: int) -> str:
    if str(number).endswith(exceptions):
        return 'секунд'

    elif str(number).endswith('1'):
        return 'секунду'

    elif str(number).endswith(('2', '3', '4')):
        return 'секунды'

    else:
        return 'секунд'
