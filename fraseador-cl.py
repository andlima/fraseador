from syntax import clause


def main():
    n = 20
    lf = '\n'
    print lf.join([
        repr(clause()).capitalize() + '.'
        for i in range(n)
    ])


if __name__ == '__main__':
    main()
