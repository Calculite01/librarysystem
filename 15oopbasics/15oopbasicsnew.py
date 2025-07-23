import pandas as pd
from validate_email_address import validate_email
import re
import ast
import bcrypt

class User():
    def __init__(self):
        self.accountLogged = None
        self.exitApplication = False

    def register(self):
        print("Select Account Type to Create")
        print("1. Customer")
        print("2. Librarian")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        if option == 1:
            accountType = "customer"
        elif option == 2:
            code = input("Security Code: ")
            if code != "1234":
                print("Incorrect Code!")
                return
            accountType = "librarian"
        else:
            print("Invalid option")
            return
        name = input("Username: ")
        for account in Account.accounts:
            if account.name == name:
                print("Name already in use")
                return
        password = input("Password: ")
        if len(password) < 8:
            print("Password needs to be atleast 8 characters long")
            return
        password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        email = input("Email: ")
        if not validate_email(email):
            print("Invalid Email")
            return
        phone = input("Phone Number: ")
        if not re.match(r'^\+?1?\d{10,15}$', phone) is not None:
            print("Invalid Phone Number")
            return
        if len(Account.accountsCreated) == 0:
            accID = 1
        else:
            for i in range(1,max(Account.accountsCreated)+2):
                if i not in Account.accountsCreated:
                    accID = i
                    break
        if accountType == "customer":
            accountObj = Customer(accID,name,password,email,phone,[])
        elif accountType == "librarian":
            accountObj = Librarian(accID,name,password,email,phone,[])
        self.accountLogged = accountObj
        #Account.accounts.append(accountObj) 

    def login(self):
        name = input("Username: ")
        password = input("Password: ")
        accountObj = None
        for account in Account.accounts:
            if account.name == name:
                accountObj = account
                break
        if accountObj == None:
            print("Incorrect username")
            return
        elif bcrypt.checkpw(password.encode('utf-8'),(accountObj.password).encode('utf-8')) == False:
            print("Incorrect password")
            return
        else:
            self.accountLogged = accountObj
             
    def exit(self):
        self.exitApplication = True
        print("Goodbye!")

class Account():
    accounts = []  #this stores the accounts
    accountsCreated = []   #this stores the ids
    def __init__(self,id,name,password,email,phone,booksBorrowed,accountType):
        self.id = int(id)
        self.name = str(name)
        self.password = str(password)
        self.email = str(email)
        self.phone = str(phone)
        self.booksBorrowed = booksBorrowed
        self.accountType = accountType
        Account.accounts.append(self)
        Account.accountsCreated.append(id)
    
    def logout(self):
        option = input("Are you sure you want to logout? Y/n")
        if option.capitalize() == 'Y':
            user.accountLogged = None
            print("Logged out")
        elif option.capitalize() == 'N':
            pass
        else:
            print("Invalid option")
        
    def deleteAccount(self):
        if len(self.booksBorrowed) != 0:
            print("You have to return your books before deleting account!")
            return
        option = input("Are you sure you want to delete account? Y/n")
        if option.capitalize() == 'Y':
            Account.accountsCreated.remove(user.accountLogged.id)
            Account.accounts.remove(user.accountLogged)
            user.accountLogged = None
            print("Account Deleted")
        elif option.capitalize() == 'N':
            pass
        else:
            print("Invalid option")

    def borrowBook(self,book):
        self.booksBorrowed.append(book.id)
        book.stock -= 1
        book.borrowedBy.append(self)
        print("Book borrowed")

    def returnBook(self,book):
        self.booksBorrowed.remove(book.id)
        book.stock += 1
        book.borrowedBy.remove(self)
        print("Book returned")

class Customer(Account):
    def __init__(self, id, name, password, email, phone, booksBorrowed):
        super().__init__(id, name, password, email, phone, booksBorrowed, "customer")

class Librarian(Account):
    def __init__(self, id, name, password, email, phone, booksBorrowed):
        super().__init__(id, name, password, email, phone, booksBorrowed, "librarian")

    def changeStock(self):
        for i in range(len(Book.books)):
            print(f"{i+1}. Title: {Book.books[i].title}{" "*(25-len(Book.books[i].title))}Author: {Book.books[i].author}{" "*(25-len(Book.books[i].author))}Genre: {Book.books[i].genre}{" "*(25-len(Book.books[i].genre))}Stock: {Book.books[i].stock}")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        if option > 0 and option <= len(Book.books):
            book = Book.books[option-1]
            print(f"Current stock for {book.title} is {book.stock}")
        else:
            print("Invalid option")
        print("1. Add to stock")
        print("2. Remove from stock")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        if option == 1:
            option = safe_int_input("Select option: ")
            if option == None:
                return
            book.stock += option
        elif option == 2:
            option = safe_int_input("Select option: ")
            if option == None:
                return
            if book.stock - option < 0:
                print("Cant remove that many")
                return
            else:
                book.stock -= option
        else:
            print("Invalid option")
            return
        print("Successfully changed stock!")
            
            

        

    def addBook(self):
        title = input("Book title: ")
        author = input("Book author: ")
        genre = input("Book genre: ")
        for i in range(1,max(Book.booksCreated)+2):
            if i not in Book.booksCreated:
                accID = i
                break
        Book(accID,title,author,genre,0)
        print(f"Successfully created book named '{title}'")

    def removeBook(self):
        for i in range(len(Book.books)):
            print(f"{i+1}. Title: {Book.books[i].title}{" "*(25-len(Book.books[i].title))}Author: {Book.books[i].author}{" "*(25-len(Book.books[i].author))}Genre: {Book.books[i].genre}{" "*(25-len(Book.books[i].genre))}Stock: {Book.books[i].stock}")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        if option > 0 and option <= len(Book.books):
            book = Book.books[option-1]
        if len(book.borrowedBy) != 0:
            print("Customers must return all books to delete!")
        else:
            Book.books.remove(book)
            print("Book successfully removed")

       
    
class Book():
    books = []   #book objects
    booksCreated = []   #book ids
    def __init__(self,id,title,author,genre,stock):
        self.id = int(id)
        self.title = str(title)
        self.author = str(author)
        self.genre = str(genre)
        self.stock = int(stock)
        self.borrowedBy = []
        Book.books.append(self)
        Book.booksCreated.append(id)
        for account in Account.accounts:
            for book in account.booksBorrowed:
                if book == self.id:
                    self.borrowedBy.append(account)


def accountsInitializer(df):
    df['booksborrowed'] = df['booksborrowed'].apply(ast.literal_eval)
    for row in df.itertuples(index=True):
        if row[7] == "customer":
            Customer(row[1],row[2],row[3],row[4],row[5],row[6])
        elif row[7] == "librarian":
            Librarian(row[1],row[2],row[3],row[4],row[5],row[6])
        else:
            print("Bad error occured")

def booksInitialzer(df):
    for row in df.itertuples(index=True):
        Book(row[1],row[2],row[3],row[4],row[5])

def accountDataframeCreator():
    dataframeDict = {"accountid":[],"accountname":[],"password":[],"email":[],"phonenum":[],"booksborrowed":[],"accounttype":[]}
    for account in Account.accounts:
        dataframeDict["accountid"].append(account.id)
        dataframeDict["accountname"].append(account.name)
        dataframeDict["password"].append(account.password)
        dataframeDict["email"].append(account.email)
        dataframeDict["phonenum"].append(account.phone)
        dataframeDict["booksborrowed"].append(account.booksBorrowed)
        dataframeDict["accounttype"].append(account.accountType)
    return pd.DataFrame(dataframeDict).sort_values(by="accountid")

def bookDataframeCreator():
    dataframeDict = {"bookid":[],"bookname":[],"authorname":[],"genre":[],"stock":[]}
    for book in Book.books:
        dataframeDict["bookid"].append(book.id)
        dataframeDict["bookname"].append(book.title)
        dataframeDict["authorname"].append(book.author)
        dataframeDict["genre"].append(book.genre)
        dataframeDict["stock"].append(book.stock)
    return pd.DataFrame(dataframeDict)
    
def safe_int_input(prompt):
    try:
        option = int(input(prompt))
        return option
    except ValueError:
        print("Invalid option")

def bookView(book):
    print(f"Book ID: {book.id}")
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"Stock: {book.stock}")
    print(" ")
    print("1. Borrow Book")
    print("2. Back to home page")
    option = safe_int_input("Select option: ")
    if option == None:
        return
    if option == 1:
        if book.stock == 0:
            print("Book out of stock!")
        else:
            user.accountLogged.borrowBook(book)
    elif option == 2:
        pass
    else:
        print("Invalid option")
        return
    

def filterPage():   #I could combine author and genre code into one function because it's repetitive but couldn't be bothered
    print("Filter by?")
    print("1. Author")
    print("2. Genre")
    option = safe_int_input("Select option: ")
    if option == None:
        return
    if option == 1:
        authors = []
        for book in Book.books:
            if book.author not in authors:
                authors.append(book.author)
        print("Select Author")
        for i in range(0,len(authors)):
            print(f"{i+1}. {authors[i]}")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        author = authors[option-1]
        bookList = []
        print("Select Book")
        for book in Book.books:
            if book.author == author:
                bookList.append(book)
        for i in range(len(bookList)):
            print(f"{i+1}. Title: {bookList[i].title}{" "*(25-len(bookList[i].title))}Author: {bookList[i].author}{" "*(25-len(bookList[i].author))}Genre: {bookList[i].genre}")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        bookView(bookList[option-1])
        
      
    elif option == 2:
        genres = []
        for book in Book.books:
            if book.genre not in genres:
                genres.append(book.genre)
        print("Select Genre")
        for i in range(0,len(genres)):
            print(f"{i+1}. {genres[i]}")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        genre = genres[option-1]
        bookList = []
        print("Select Book")
        for book in Book.books:
            if book.genre == genre:
                bookList.append(book)
        for i in range(len(bookList)):
            print(f"{i+1}. Title: {bookList[i].title}{" "*(25-len(bookList[i].title))}Author: {bookList[i].author}{" "*(25-len(bookList[i].author))}Genre: {bookList[i].genre}")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        bookView(bookList[option-1])
    else:
        print("Invalid option")
        return
      


def accountPage():
    print(f"Logged in as {user.accountLogged.name}")
    print("1. Account Details")
    print("2. Logout")
    print("3. Delete Account")
    print("4. Return to home page")
    option = safe_int_input("Select option: ")
    if option == None:
        return
    if option == 1:
        print(f"Account Type: {user.accountLogged.accountType}")
        print(f"Username: {user.accountLogged.name}")
        print(f"Email: {user.accountLogged.email}")
        print(f"Number of books borrowed: {len(user.accountLogged.booksBorrowed)}")
        if len(user.accountLogged.booksBorrowed) != 0:
            for id in user.accountLogged.booksBorrowed:
                for book in Book.books:
                    if id == book.id:
                        print(f"Title: {book.title}{" "*(25-len(book.title))}Author: {book.author}{" "*(25-len(book.author))}Genre: {book.genre}")
    elif option == 2:
        user.accountLogged.logout()
    elif option == 3:
        user.accountLogged.deleteAccount()
    elif option == 4:
        pass
    else:
        print("Invalid option")


def editBookpage():
    print("1. Add book")
    print("2. Remove book")
    print("3. Change stock")
    print("4. Back to home page")
    option = safe_int_input("Select option: ")
    if option == None:
        return
    if option == 1:
        user.accountLogged.addBook()
    elif option == 2:
        user.accountLogged.removeBook()
    elif option == 3:
        user.accountLogged.changeStock()
    elif option == 4:
        pass
    else:
        print("Invalid option")

def home():
    print(f"Logged in as {user.accountLogged.name}")   
    print("1. Borrow Book")
    print("2. Return Book")
    print("3. Account")
    if user.accountLogged.accountType == 'librarian':
        print("4. Edit Books")
        print("5. Exit")
    elif user.accountLogged.accountType == 'customer':
        print("4. Exit")
    option = safe_int_input("Select option: ")
    if option == None:
        return
    if user.accountLogged.accountType == 'librarian' and option > 3:
        if option == 4:
            editBookpage()
            return
        elif option == 5:
            user.exit()
            return
        else:
            print("Invalid option")
    if option == 1:
        print("Book Search")
        print("0. Filter results")
        for i in range(len(Book.books)):
            print(f"{i+1}. Title: {Book.books[i].title}{" "*(25-len(Book.books[i].title))}Author: {Book.books[i].author}{" "*(25-len(Book.books[i].author))}Genre: {Book.books[i].genre}")
        print(f"{len(Book.books)+1}. Back to home page")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        if option == 0:
            filterPage()
        elif option > 0 and option <= len(Book.books):
            bookView(Book.books[option-1])
        elif option == len(Book.books)+1:
            pass
        else:
            print("Invalid option")          
    elif option == 2:
        print("What book to return?")
        bookList = []
        for book in Book.books:
            if book.id in user.accountLogged.booksBorrowed:
                bookList.append(book)
        for i in range(len(bookList)):
            print(f"{i+1}. Title: {bookList[i].title}{" "*(25-len(bookList[i].title))}Author: {bookList[i].author}{" "*(25-len(bookList[i].author))}Genre: {bookList[i].genre}")
        option = safe_int_input("Select option: ")
        if option == None:
            return
        if option > 0 and option <= len(bookList):
            user.accountLogged.returnBook(bookList[option-1])
        else:
            print("Invalid option")
    elif option == 3:
        accountPage()
    elif option == 4:
        user.exit()
    else:
        print("Invalid option")
    

def login():
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    option = safe_int_input("Select option: ")
    if option == None:
        return
    if option == 1:
        user.register()
    elif option == 2:
        user.login()
    elif option == 3:
        user.exit()
    else:
        print("Invalid option")


    
def main():
    accountdf = pd.read_csv('15oopbasics/accounts.csv')
    accountsInitializer(accountdf)
    bookdf = pd.read_csv('15oopbasics/bookdata.csv')
    booksInitialzer(bookdf)
    print("Welcome!")
    while True:
        if user.accountLogged == None:
            login()
        else:
            home()
        if user.exitApplication:
            break
    accountDataframeCreator().to_csv('15oopbasics/accounts.csv',index=False)
    bookDataframeCreator().to_csv('15oopbasics/bookdata.csv',index=False)
user = User()
main()
