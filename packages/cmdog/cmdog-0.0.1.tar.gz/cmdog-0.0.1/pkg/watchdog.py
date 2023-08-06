"""cmdog CLI

Usage:
  cmdog <cmd>
  cmdog <cmd> -i <interval>

Options:
  -h --help         Show this screen.
  -v --version      Show version.
  -i --interval     Set Check interval.
"""
from docopt import docopt
import asyncio
import subprocess
import psutil
import logging
import datetime


class Watcher():

  def __init__(self,  args):
    self.start_time = datetime.datetime.now()
    interval = args.get('<interval>')
    self.interval = 1 if interval is None else int(interval)
    self.error = False
    self.last_run_time = None
    self.run_count = 0
    self.cmd = args.get('<cmd>',  '')

  def run_cmd(self):
    run_time = datetime.datetime.now()
    if self.last_run_time != None and (run_time - self.start_time).total_seconds() < self.interval * 2:
      self.error = True
      pass
    self.last_run_time = run_time
    proc = subprocess.Popen(f'{self.cmd} >out.log 2>&1'.split(' '), shell=True)
    self.pid = proc.pid

    self.run_count += 1
    print(self.run_count)

  def watch(self):
    self.run_cmd()

  async def check(self):
    while not self.error:
      try:
        proc = psutil.Process(self.pid)
        if proc.status() == 'zombie':
          proc.wait()
          self.run_cmd()
      except Exception as e:
        self.run_cmd()
        logging.error(e)
        pass
      finally:
        await asyncio.sleep(self.interval)


async def main():
  arguments = docopt(__doc__, version='cmdog 0.0.1')
  w = Watcher(arguments)
  w.watch()
  await w.check()
  logging.error('Rapid failure')


def cmd():
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())


if __name__ == "__main__":
  cmd()
