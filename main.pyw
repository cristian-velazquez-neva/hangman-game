import tkinter as tk
import random, re, keyword

from tkinter import messagebox

class Hangman:
	def __init__(self, master):
		self.master = master
		self.letter = tk.StringVar()

		self.create_gui()
		self.new_word()

	def create_gui(self):
		self.frame = tk.Frame(self.master)
		self.frame.pack()

		tk.Label(self.frame, text='Python Keywords', font = ('Arial', 10, 'bold')).grid(row=0, sticky='w')

		self.show_lives = tk.Label(self.frame)
		self.show_lives.grid(row=1, sticky='w')

		self.show_my_word = tk.Label(self.frame)
		self.show_my_word.grid(row=2, sticky='w')

		self.entry = tk.Entry(self.frame, justify='center', textvariable=self.letter)
		self.entry.focus()
		self.entry.bind('<Return>', self.validating_letter)
		self.entry.bind('<KeyPress>', self.change_letter)
		self.entry.grid(row=3)

	def change_letter(self, e):
		if len(self.letter.get()) > 0:
			self.letter.set(self.letter.get()[1:1])

	def new_word(self):
		list_works = keyword.kwlist
		self.word = list_works[random.randrange(len(list_works))].lower()
		self.my_word = ''
		self.set_letter = []
		self.lives = 10

		self.status()

	def status(self):
		self.letter.set('')
		new_status = ''
		failures = 0

		for letter in self.word:
			if letter in self.my_word:
				new_status += letter
			else:
				new_status += '*'
				failures += 1
	
		self.show_lives.config(text='lives: '+str(self.lives))
		self.show_my_word.config(text='word: ' + new_status)

		self.check_win(failures)

	def check_win(self, failures):
		answer = 'Wait'
		if failures == 0:
			answer = self.show_message('Congratulations! You won the game!\nYou want to generate a new word?', True)
		elif self.lives == 0:
			self.show_my_word.config(text='word: ' + self.word)
			answer = self.show_message('You lost the game!\nYou want to generate a new word?', True)

		if answer == True:
			self.new_word()
		elif answer == False:
			self.master.destroy()

	def isNaL(self, letter):
		validate = re.compile(r'[a-z]{1,}').findall(letter)

		if validate == []: return True
		else: return False

	def validating_letter(self, event):
		letter = self.letter.get()

		if self.isNaL(letter) == False:
			if self.lives != 0:
				self.my_word += letter
				
				if letter not in self.set_letter:
					if letter not in self.word:
						self.lives -= 1
					self.set_letter.append(letter)
				else:
					self.show_message('The letter ' + letter + ' has already been entered.')

			self.status()
		else:
			self.letter.set('')
			self.show_message('You can only enter lowercase letters.')

	def show_message(self, message, ask_message=False):
		if ask_message:
			return messagebox.askokcancel('Game Over', message)
		else:
			messagebox.showwarning('Warning', message)

if __name__ == "__main__":
	root = tk.Tk()
	root.title('Hangman')
	root.resizable(False, False)
	game = Hangman(root)
	root.mainloop()