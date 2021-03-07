import argparse
import asyncio
import Scanner
import os

parser = argparse.ArgumentParser(description='Upload firmware on scanned label')
parser.add_argument('--ip', required=False, type=str)
parser.add_argument('--port', required=False, type=int)
parser.add_argument('--cmd', required=False, type=str)
args, args_other = parser.parse_known_args()


def on_new_label(label):
	print("label is", label)
	os.system("echo Hello world")  # Todo flash command


async def main():
	loop = asyncio.get_running_loop()
	barcode_reader = Scanner.Scanner(loop=loop, callback=on_new_label)
	await barcode_reader.connect()
	todo_fix = asyncio.Future()
	await todo_fix

asyncio.run(main())
