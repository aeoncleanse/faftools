"""
Updates the version in the binary executable of the Forged Alliance game. Will write a new ForgedAlliance.version.exe
file.

Usage:
   update_version <version> [--file=<file>]

Options:
   --file=<file>   The binary file to update [default: ForgedAlliance.exe]
"""
import struct
import shutil
from docopt import docopt


def update_exe_version(source: Path, destination: Path, version: str):
    """
    :param source: Path to the static base copy of ForgedAlliance.exe - Hardcoded in API
    :param destination: Path this update is being copied to
    :param version: New mod version
    :return:
    """

    shutil.copyfile(source, "ForgedAlliance.%s.exe" % version)
    destination = destination / "ForgedAlliance.%s.exe" % version
    shutil.move(source, destination)

    addr = [0xd3d3f, 0x47612c, 0x476665]
    f = open("ForgedAlliance.%s.exe" % version, 'rb+')

    for a in addr:
        v = struct.pack("<L", int(version))
        f.seek(a+1, 0)
        f.write(v)
    f.close()
    print("Saved ForgedAlliance.%s.exe".format(version))
    return f

if __name__ == '__main__':
    arguments = docopt(__doc__)
    source, destination, version = arguments.get('--file'), arguments.get('destination'), arguments.get('<version>')
    create_version(source, version)
