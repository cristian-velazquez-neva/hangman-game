from tkinter import *
from tkinter import messagebox
from io import open
import random
import re

class Game:
	def __init__(self, Root):
		self.Root = Root
		self.Root.title('Hangman Game')
		self.Root.resizable(False, False)

		self.VarLetter=StringVar()

		FontTitle=('Verdana', 16, 'bold')
		Font=('Consolas', 12)

		FrameGame=Frame(self.Root)
		FrameGame.pack(padx=15, pady=15)

		Label(FrameGame, text='Hangman\nGame', font=FontTitle).grid(sticky=W+E)

		self.LabelLives=Label(FrameGame)
		self.LabelLives.grid(row=1, sticky=W+E)

		self.LabelWord=Label(FrameGame, font=Font)
		self.LabelWord.grid(row=2, sticky=W+E)

		self.LabelTranslate=Label(FrameGame, font=Font)
		self.LabelTranslate.grid(row=3, sticky=W+E)

		self.EntryLetter=Entry(FrameGame, justify=CENTER, textvariable=self.VarLetter)
		self.EntryLetter.focus()
		self.EntryLetter.bind('<Return>', self.ValidatingLetter)
		self.EntryLetter.grid(row=4, padx=10, pady=10)

		self.VarLetter.trace_variable('w', self.OnWrite)
		self.ArchivesWorks()
		self.NewWord()

	def OnWrite(self, *args):
		Write=self.VarLetter.get()
		if len(Write) > 1: self.VarLetter.set(Write[1])

	def ArchivesWorks(self):
		ArchiveWorks=open('works.txt','r')
		TxtWorks=ArchiveWorks.read()
		ArchiveWorks.close()

		ArchiveTranslates=open('translates.txt','r')
		TxtTranslates=ArchiveTranslates.read()
		ArchiveTranslates.close()

		self.ListWorks=TxtWorks.split()
		self.ListTranslates=TxtTranslates.split()
	
	def NewWord(self):
		NumRandom=random.randrange(len(self.ListWorks))
		self.Word=self.ListWorks[NumRandom]
		self.Translate=self.ListTranslates[NumRandom]

		self.YouWord=''

		self.SetLetter=[]
		self.Lives=10
		self.LabelTranslate.config(text='')

		self.Status()

	def Status(self):
		self.VarLetter.set('')
		NewStatus=''
		Failures=0
		Answer='Wait'

		for Letter in self.Word:
			if Letter in self.YouWord:
				NewStatus+=Letter
			else:
				NewStatus+='*'
				Failures+=1
	
		self.LabelLives.config(text='Lives: '+str(self.Lives))
		self.LabelWord.config(text=NewStatus)

		if Failures==0:
			self.LabelTranslate.config(text=self.Translate)
			Answer=messagebox.askokcancel('Won','Congratulations you won\nYou want to generate a new word?')
		elif self.Lives==0:
			self.LabelTranslate.config(text=self.Translate)
			self.LabelWord.config(text=self.Word)
			Answer=messagebox.askokcancel('Loser','You want to generate a new word?')

		if Answer==True: self.NewWord()
		elif Answer==False: Root.destroy()

	def isNaL(self, Letter):
		Validate = re.compile(r'[a-z]{1,}').findall(Letter)

		if Validate == []: return True
		else: return False
	
	def ValidatingLetter(self, event):
		Letter = self.EntryLetter.get()

		if self.isNaL(Letter) == False:
			if self.Lives!=0:
				self.YouWord+=Letter
				
				if Letter not in self.SetLetter:
					if Letter not in self.Word: self.Lives-=1
					self.SetLetter.append(Letter)
				else:
					messagebox.showwarning('Warning','The letter '+Letter+' has already been entered.')

			self.Status()
		else:
			self.VarLetter.set('')
			messagebox.showwarning('Warning','You can only enter lowercase letters.')

if __name__ == "__main__":
	Root = Tk()
	Game(Root)
	Root.mainloop()