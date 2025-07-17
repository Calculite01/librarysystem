import sys
import pandas as pd
from validate_email_address import validate_email
import re
import ast

class User():
    def __init__(self):
        self.accountLogged = None

    def register(self):
        global accounts
        print("Select Account Type to Create")
        print("1. Customer")
        print("2. Librarian")
        try:
            option = int(input("Select option: "))
        except:
            print("Invalid option")
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
        name = input("Username: ")
        for account in accounts:
            if account.name == name:
                print("Name already in use")
                return
        password = input("Password: ")
        if len(password) < 8:
            print("Password needs to be atleast 8 characters long")
            return
        email = input("Email: ")
        if not validate_email(email):
            print("Invalid Email")
            return
        phone = input("Phone Number: ")
        if not re.match(r'^\+?1?\d{10,15}$', phone) is not None:
            print("Invalid Phone Number")
            return
        for i in range(1,max(Account.accountsCreated)+2):
            if i not in Account.accountsCreated:
                accID = i
                break
        if accountType == "customer":
            accountObj = Customer(accID,name,password,email,phone,[])
        elif accountType == "librarian":
            accountObj = Librarian(accID,name,password,email,phone,[])
        self.accountLogged = accountObj
        accounts.append(accountObj) 

    def login(self):
        name = input("Username: ")
        password = input("Password: ")
        accountObj = None
        for account in accounts:
            if account.name == name:
                accountObj = account
                break
        if accountObj == None:
            print("Incorrect username")
            return
        elif password != accountObj.password:
            print("Incorrect password")
            return
        else:
            self.accountLogged = accountObj
             
    def exit(self):
        global exitApplication
        exitApplication = True
        print("Goodbye!")

class Account():
    accountsCreated = []
    def __init__(self,id,name,password,email,phone,booksBorrowed,accountType):
        self.id = int(id)
        self.name = str(name)
        self.password = str(password)
        self.email = str(email)
        self.phone = str(phone)
        self.booksBorrowed = booksBorrowed
        self.accountType = accountType
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
            accounts.remove(user.accountLogged)
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
        for i in range(len(books)):
            print(f"{i+1}. Title: {books[i].title}{" "*(25-len(books[i].title))}Author: {books[i].author}{" "*(25-len(books[i].author))}Genre: {books[i].genre}{" "*(25-len(books[i].genre))}Stock: {books[i].stock}")
        try:
            option = int(input("Select option: "))
        except:
            print("Ivalid option")
            return
        if option > 0 and option <= len(books):
            book = books[option-1]
            print(f"Current stock for {book.title} is {book.stock}")
        else:
            print("Invalid option")
        print("1. Add to stock")
        print("2. Remove from stock")
        try:
            option = int(input("Select option: "))
        except:
            print("Ivalid option")
            return
        if option == 1:
            try:
                option = int(input("Amount to add: "))
            except:
                print("Ivalid option")
                return
            book.stock += option
        elif option == 2:
            try:
                option = int(input("Amount to remove: "))
            except:
                print("Ivalid option")
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
        books.append(Book(accID,title,author,genre,0))
        print(f"Successfully created book named '{title}'")

    def removeBook(self):
        for i in range(len(books)):
            print(f"{i+1}. Title: {books[i].title}{" "*(25-len(books[i].title))}Author: {books[i].author}{" "*(25-len(books[i].author))}Genre: {books[i].genre}{" "*(25-len(books[i].genre))}Stock: {books[i].stock}")
        try:
            option = int(input("Select option: "))
        except:
            print("Ivalid option")
            return
        if option > 0 and option <= len(books):
            book = books[option-1]
        if len(book.borrowedBy) != 0:
            print("Customers must return all books to delete!")
        else:
            books.remove(book)
            print("Book successfully removed")

       
    
class Book():
    booksCreated = []
    def __init__(self,id,title,author,genre,stock):
        self.id = int(id)
        self.title = str(title)
        self.author = str(author)
        self.genre = str(genre)
        self.stock = int(stock)
        self.borrowedBy = []
        Book.booksCreated.append(id)
        for account in accounts:
            for book in account.booksBorrowed:
                if book == self.id:
                    self.borrowedBy.append(account)


def accountsInitializer(df):
    df['booksborrowed'] = df['booksborrowed'].apply(ast.literal_eval)
    accounts = []
    for row in df.itertuples(index=True):
        if row[7] == "customer":
            accounts.append(Customer(row[1],row[2],row[3],row[4],row[5],row[6]))
        elif row[7] == "librarian":
            accounts.append(Librarian(row[1],row[2],row[3],row[4],row[5],row[6]))
        else:
            print("Bad error occured")
        Account.accountsCreated.append(int(row[1]))
    return accounts

def booksInitialzer(df):
    books = []
    for row in df.itertuples(index=True):
        books.append(Book(row[1],row[2],row[3],row[4],row[5]))
    return books

def accountDataframeCreator():
    dataframeDict = {"accountid":[],"accountname":[],"password":[],"email":[],"phonenum":[],"booksborrowed":[],"accounttype":[]}
    for account in accounts:
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
    for book in books:
        dataframeDict["bookid"].append(book.id)
        dataframeDict["bookname"].append(book.title)
        dataframeDict["authorname"].append(book.author)
        dataframeDict["genre"].append(book.genre)
        dataframeDict["stock"].append(book.stock)
    return pd.DataFrame(dataframeDict)
    
def bookView(book):
    print(f"Book ID: {book.id}")
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"Stock: {book.stock}")
    print(" ")
    print("1. Borrow Book")
    print("2. Back to home page")
    try:
        option = int(input("Select option"))
    except:
        print("Invalid option")
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
    try:
        option = int(input("Select option: "))
    except:
        print("Ivalid option")
        return
    if option == 1:
        authors = []
        for book in books:
            if book.author not in authors:
                authors.append(book.author)
        print("Select Author")
        for i in range(0,len(authors)):
            print(f"{i+1}. {authors[i]}")
        try:
            option = int(input("Select option: "))
        except:
            print("Invalid option")
            return
        author = authors[option-1]
        bookList = []
        print("Select Book")
        for book in books:
            if book.author == author:
                bookList.append(book)
        for i in range(len(bookList)):
            print(f"{i+1}. Title: {bookList[i].title}{" "*(25-len(bookList[i].title))}Author: {bookList[i].author}{" "*(25-len(bookList[i].author))}Genre: {bookList[i].genre}")
        try:
            option = int(input("Select option: "))
        except:
            print("Invalid option")
            return
        bookView(bookList[option-1])
        
      
    elif option == 2:
        genres = []
        for book in books:
            if book.genre not in genres:
                genres.append(book.genre)
        print("Select Genre")
        for i in range(0,len(genres)):
            print(f"{i+1}. {genres[i]}")
        try:
            option = int(input("Select option: "))
        except:
            print("Invalid option")
            return
        genre = genres[option-1]
        bookList = []
        print("Select Book")
        for book in books:
            if book.genre == genre:
                bookList.append(book)
        for i in range(len(bookList)):
            print(f"{i+1}. Title: {bookList[i].title}{" "*(25-len(bookList[i].title))}Author: {bookList[i].author}{" "*(25-len(bookList[i].author))}Genre: {bookList[i].genre}")
        try:
            option = int(input("Select option: "))
        except:
            print("Invalid option")
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
    try:
        option = int(input("Select option: "))
    except:
        print("Invalid option")
        return
    if option == 1:
        print(f"Account Type: {user.accountLogged.accountType}")
        print(f"Username: {user.accountLogged.name}")
        print(f"Email: {user.accountLogged.email}")
        print(f"Number of books borrowed: {len(user.accountLogged.booksBorrowed)}")
        if len(user.accountLogged.booksBorrowed) != 0:
            for id in user.accountLogged.booksBorrowed:
                for book in books:
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
    try:
        option = int(input("Select option: "))
    except:
        print("Invalid option")
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
    try:
        option = int(input("Select option: "))
    except:
        print("Invalid option")
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
        for i in range(len(books)):
            print(f"{i+1}. Title: {books[i].title}{" "*(25-len(books[i].title))}Author: {books[i].author}{" "*(25-len(books[i].author))}Genre: {books[i].genre}")
        print(f"{len(books)+1}. Back to home page")
        try:
            option = int(input("Select option: "))
        except:
            print("Ivalid option")
            return
        if option == 0:
            filterPage()
        elif option > 0 and option <= len(books):
            bookView(books[option-1])
        elif option == len(books)+1:
            pass
        else:
            print("Invalid option")          
    elif option == 2:
        print("What book to return?")
        bookList = []
        for book in books:
            if book.id in user.accountLogged.booksBorrowed:
                bookList.append(book)
        for i in range(len(bookList)):
            print(f"{i+1}. Title: {bookList[i].title}{" "*(25-len(bookList[i].title))}Author: {bookList[i].author}{" "*(25-len(bookList[i].author))}Genre: {bookList[i].genre}")
        try:
            option = int(input("Select option: "))
        except:
            print("Invalid option")
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
    try:
        option = int(input("Select option: "))
    except:
        print("Invalid option")
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
    global user,accountdf,accounts,bookdf,books,exitApplication
    user = User()
    exitApplication = False
    accountdf = pd.read_csv('15oopbasics/accounts.csv')
    accounts = accountsInitializer(accountdf)
    bookdf = pd.read_csv('15oopbasics/bookdata.csv')
    books = booksInitialzer(bookdf)
    print("Welcome!")
    while True:
        if user.accountLogged == None:
            login()
        else:
            home()
        if exitApplication:
            break
    accountDataframeCreator().to_csv('15oopbasics/accounts.csv',index=False)
    bookDataframeCreator().to_csv('15oopbasics/bookdata.csv',index=False)
main()