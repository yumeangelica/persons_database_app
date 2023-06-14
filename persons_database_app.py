import sqlite3
import random

#Adding a person to the database
def add_person(conn, first_name: str, last_name: str):

	cursor = conn.cursor() #conn.cursor() is a cursor object that allows you to execute SQL commands
	
	while True: #generate a random unique id for the agent
		id = random.randint(1, 9999999) # generate a random id
		ids_list = cursor.execute('SELECT id FROM Person').fetchall() #fetch all ids from the database to check if the generated id is unique
		
		if id not in ids_list: #if the generated id is unique, break the loop, if not, generate a new id
			break

	cursor.execute('INSERT INTO Person VALUES (?, ?, ?)', [int(id), first_name := first_name.split()[0].lower(), last_name := last_name.split()[0].lower()]) #insert new person to the database
	conn.commit() #commit the changes


#Deleting a person from the database
def delete_person(conn, id: int):

	cursor = conn.cursor()

	cursor.execute('DELETE FROM Person WHERE id = ?', [int(id)]) #delete the person from the database
	conn.commit()


def read_database(conn):

	persons_list = [] #list of all persons in the database
	cursor = conn.cursor()

	person_db_fetch = cursor.execute('SELECT * FROM Person ORDER by last_name, first_name').fetchall() #fetch all persons from the database

	for (id, first_name, last_name) in person_db_fetch: #loop through all persons in the database
		persons_list.append((id, last_name.capitalize(), first_name.capitalize())) #add the person to the persons_list and capitalize the first and last name

	return persons_list #return the persons_list


#Initialize the database if there is no table Person in database
def init_database(conn):
	conn.execute('CREATE TABLE IF NOT EXISTS Person (id INTEGER PRIMARY KEY UNIQUE, first_name TEXT, last_name TEXT)')
	conn.commit()
	

#Main function
def main():
	persons_db = 'persons.sqlite' #database name
	
	conn = sqlite3.connect(persons_db) #connect to the database
	init_database(conn) #initialize the database
	conn.isolation_level = None #set isolation level to None

	while True: #main loop
		persons = read_database(conn) #read the database and save the persons in the persons list
		print('\nPersons:\n')
		for person in persons: #print all persons in the persons list
			print(f'{person[0]}	  {person[1]}  {person[2]}')
		print()

		command = input('What would you like to do: [a]dd, [r]emove, or [q]uit?: ') #ask the user what she/he wants to do

		if command[0].startswith('a'): #if the user wants to add a person
			first_name = input('first name? ') 
			last_name = input('last name? ') 
			add_person(conn, first_name, last_name) #add the person to the database
			pass

		elif command[0].startswith('r'): #if the user wants to remove a person
			id = int(input('id? ')) #ask for the id of the person to remove
			delete_person(conn, id) #remove the person from the database with the given id
			pass

		elif command[0].startswith('q'): #if the user wants to quit
			break

	
#running the main function
if __name__ == "__main__": 
	
	main()


	