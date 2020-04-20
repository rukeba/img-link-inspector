import argparse

from inspector import ImgLinkInspector


def main():
    parser = argparse.ArgumentParser(description='Inspect page for broken image urls')
    parser.add_argument('url', help='url of page to inspect')
    parser.add_argument('--src-attr', dest='src_attr',
                        default='src', help='attribute name of <img> tag to find image url (useful for lazy loading)')
    parser.add_argument('--verbose', dest='verbose',
                        action='store_true', default=False, help='verbose output')
    args = parser.parse_args()

    inspector = ImgLinkInspector(args.url, src_attr=args.src_attr, verbose=args.verbose)
    statuses = inspector.inspect()
    for status in statuses:
        print(f'{status[0]}, {status[1]}')


if __name__ == '__main__':
    main()