import argparse
import sys

parser = argparse.ArgumentParser(description="Mario Kart Stat Tracker")
parser.add_argument('-i', '--input', help="Input video file or stream", required=True)
parser.add_argument('-d', '--debug', action="store_true", default=False, help="Enables error logging and shows video.")

args = parser.parse_args()

if __name__ == "__main__":
    print "\n***Debug args***\n"

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)


