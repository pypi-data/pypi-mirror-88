import argparse

from vscrap._sc import rap

par = argparse.ArgumentParser()
par.add_argument('extension_id', type=str, help="Extension ID for the extension to scrap")
args = par.parse_args()

try:
    details = rap(str(args.extension_id))
    dets = details.keys()
    if dets:
        message = []

        for det in dets:
            message.append(
                f"{det.title().replace('_', ' ')}: {details.get(det)}"
            )
        print('\n'.join(message))

    else:
        print('Could not retrieve extension details')

except TypeError:
    print('Enter a valid extension id/unique identifier')
