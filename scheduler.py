import time
import schedule
from bot import LunchBot

class Scheduler:
	def job(self):
		bot = LunchBot()
		bot.order()

	def run(self):
		schedule.every().monday.at('07:00').do(self.job)
		schedule.every().tuesday.at('07:00').do(self.job)
		schedule.every().wednesday.at('07:00').do(self.job)
		schedule.every().thursday.at('07:00').do(self.job)
		schedule.every().friday.at('07:00').do(self.job)
		while True:
			t = schedule.idle_seconds()
			if t > 0:
				print(t)
				time.sleep(t)
			schedule.run_pending()

if __name__ == '__main__':
	scheduler = Scheduler()
	scheduler.run()
