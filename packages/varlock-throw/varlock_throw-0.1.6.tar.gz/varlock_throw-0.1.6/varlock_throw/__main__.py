def main():
	import random
	def varlock_scramble(lister):
		return([''.join(random.sample(word, len(word))) for word in lister])

		
if __name__=='__main__':
	main()    