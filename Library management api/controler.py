from fastapi import FastAPI
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional
import json
from fastapi.responses import JSONResponse
from datetime import date

class Book(BaseModel):
    Book_id:Annotated[str,Field(description="Book_id value store at here",examples=['SF076'])]
    Title:Annotated[str,Field(description="Title of Book",examples=['Nameless_moster'])]
    Author:Annotated[str,Field(description='Author Name of Book',examples=['Franz Bonaparta'])]
    Category:Annotated[str,Field(description="Book_types",examples=['picture_book'])]
    Total_copies:Annotated[int,Field(description="Book_copies",examples=[100])]

    @computed_field
    @property
    def book_label(self) -> str:
        return f"{self.Book_id} -- {self.Title}"
    
    @computed_field
    @property
    def is_available(self) -> bool:
        if self.Total_copies>0:
            return True
        return False
    
class Book_update(BaseModel):
    Title:Annotated[Optional[str],Field(default=None)]
    Author:Annotated[Optional[str],Field(default=None)]
    Category:Annotated[Optional[str],Field(default=None)]
    Total_copies:Annotated[Optional[int],Field(default=None)]
class Student(BaseModel):
    Student_ID:Annotated[str,Field(description='Student_id value store at here',examples=['SU148'])]
    Name:Annotated[str,Field(description='student_name',examples=['Jay'])]
    Class:Annotated[int,Field(...,gt=0,lt=13,description='student_class',examples=[12])]

    @computed_field
    @property
    def student_label(self)-> str:
        return f"{self.Student_ID}--{self.Name}"
class Student_update(BaseModel):
    Name:Annotated[Optional[str],Field(default=None)]
    Class:Annotated[Optional[int],Field(default=None)]
class Issue_Record(BaseModel):
    Transaction_id:Annotated[str,Field(examples=['T001'])]
    Student_ID:Annotated[str,Field(description="Student_id value store at here",examples=['SU148'])]
    Book_ID:Annotated[str,Field(description="Book_id value store at here",examples=['SF076'])]
    issuedate:date
    Due_date:date
    returndate:Optional[date]=None
    @computed_field
    @property
    def status(self)->str:
        if self.returndate:
            return f"returned at {self.returndate}"
        else:
            return "Active"
    @computed_field
    @property
    def Is_Overdue(self) -> bool:
        end_date = self.returndate if self.returndate else date.today()
        return end_date > self.Due_date
    @computed_field
    @property
    def Overdue_Days(self) -> int:
        if not self.Is_Overdue:
            return 0
        end_date = self.returndate if self.returndate else date.today()
        return (end_date - self.Due_date).days
    @computed_field
    @property
    def Late_Fee(self)->float:
        return float(self.Overdue_Days*5)
    @computed_field
    @property
    def Borrow_Duration(self) -> int:
        end_date = self.returndate if self.returndate else date.today()
        return (end_date - self.issuedate).days
    @computed_field
    @property
    def Day_remain(self) -> int:
        if self.returndate:
            return 0
        return (self.Due_date - date.today()).days

class Issue_Record_update(BaseModel):
    Student_ID:Annotated[Optional[str],Field(default=None)]
    Book_ID:Annotated[Optional[str],Field(default=None)]
    issuedate:Optional[date]=None
    Due_date:Optional[date]=None
    returndate:Optional[date]=None
app=FastAPI()
@app.get('/student_data')
def load_student_data():
    try:
        with open('student.json','r') as f:
            student_data=json.load(f)
        return student_data
    except FileNotFoundError:
        return {}
def save_student_data(data):
    with open('student.json','w') as f:
        json.dump(data,f)
@app.get('/books_data')
def load_books_data():
    try:
        with open('books.json','r') as f:
            books_data=json.load(f)
        return books_data
    except FileNotFoundError:
        return {}
def save_books_data(data):
    with open('books.json','w') as f:
        json.dump(data,f)
@app.get('/issue_data')
def load_issue_data():
    try:
        with open('Issue.json','r') as f:
            issue_data=json.load(f)
        return issue_data
    except FileNotFoundError:
        return {}
def save_issue_data(data):
    with open('Issue.json','w') as f:
        json.dump(data,f)
@app.get('/')
def home():
    return {'hello':'homepage'}
@app.get('/load_student_data/{student_id}')
def studentid_data_load(student_id:str):
    student_data=load_student_data()
    if student_id not in student_data:
        return JSONResponse(status_code=404,content='student id not found in database')
    return student_data[student_id]
@app.post('/create_student_data')
def create_student_data(student:Student):
    student_data=load_student_data()
    if student.Student_ID in student_data:
        return JSONResponse(status_code=400,content='student id already found in database')
    student_data[student.Student_ID]=student.model_dump(mode='json', exclude={'Student_ID'})
    save_student_data(student_data)
    return JSONResponse(status_code=201,content={'message': 'Student data created'})
@app.put('/update_student_data/{student_id}')
def update_student_data(update:Student_update,student_id:str):
    student_data=load_student_data()
    if student_id not in student_data:
        return JSONResponse(status_code=404,content='student id not found in database')
    student_Info=student_data[student_id]
    student_update=update.model_dump(mode='json', exclude_unset=True)
    for key,value in student_update.items():
        student_Info[key]=value
    student_Info['Student_ID']=student_id
    student_obj=Student(**student_Info)
    student_Info=student_obj.model_dump(mode='json', exclude={'Student_ID'})
    student_data[student_id]=student_Info
    save_student_data(student_data)
    return JSONResponse(status_code=200,content={'message': 'Student updated successfully'})
@app.delete('/delete/{Student_id}')
def delete_student_data(Student_id:str):
    data=load_student_data()
    if Student_id in data:
        del data[Student_id]
        save_student_data(data)
        return JSONResponse(status_code=200,content={'message':'student data sucessfuly deleted'})
    else:
        return JSONResponse(status_code=404,content={'message':'wrong student id'})
@app.get('/load_books_data/{book_id}')
def bookid_data_load(book_id:str):
    books_data=load_books_data()
    if book_id not in books_data:
        return JSONResponse(status_code=404,content='book id not found in database')
    return books_data[book_id]
@app.post('/create_book_data')
def create_books_data(book:Book):
    book_data=load_books_data()
    if book.Book_id in book_data:
        return JSONResponse(status_code=400,content='book_id already found in database')
    book_data[book.Book_id]=book.model_dump(mode='json', exclude={'Book_id'})
    save_books_data(book_data)
    return JSONResponse(status_code=201,content={'message': 'Book data created'})
@app.put('/update_book/{book_id}')
def update_book_detail(book_id:str,update:Book_update):
    book_data=load_books_data()
    if book_id not in book_data:
        return JSONResponse(status_code=404,content='book id not found in database')
    book_info=book_data[book_id]
    book_update=update.model_dump(mode='json', exclude_unset=True)
    for key,value in book_update.items():
        book_info[key]=value
    book_info['Book_id']=book_id
    book_obj=Book(**book_info)
    book_info=book_obj.model_dump(mode='json', exclude={'Book_id'})
    book_data[book_id]=book_info
    save_books_data(book_data)
    return JSONResponse(status_code=200,content={'message': 'Book updated successfully'})
@app.delete('/delete_book/{book_id}')
def delete_book(book_id:str):
    data=load_books_data()
    if book_id in data:
        del data[book_id]
        save_books_data(data)
        return JSONResponse(status_code=200,content='Book data deleted sucessfully')
    else:
        return JSONResponse(status_code=404,content="Book data not found in database")
@app.get('/issue/{Transaction_id}')
def Transaction_id_dataload(Transaction_id:str):
    issue_data=load_issue_data()
    if Transaction_id not in issue_data:
        return JSONResponse(status_code=404,content='Transaction_id not found in database')
    return issue_data[Transaction_id]
@app.post('/create_issue_data')
def create_Transaction_data(Transaction:Issue_Record):
    issue_data=load_issue_data()
    if Transaction.Transaction_id in issue_data:
        return JSONResponse(status_code=400,content='Transaction_id already in database')
    
    # Check book availability and decrement inventory
    books_data = load_books_data()
    if Transaction.Book_ID not in books_data:
        return JSONResponse(status_code=404, content='Book ID not found in database')
    
    book_info = books_data[Transaction.Book_ID]
    book_info['Book_id'] = Transaction.Book_ID
    book_obj = Book(**book_info)
    
    if not book_obj.is_available:
        return JSONResponse(status_code=400, content='Book is currently not available')
    
    book_obj.Total_copies -= 1
    books_data[Transaction.Book_ID] = book_obj.model_dump(mode='json', exclude={'Book_id'})
    save_books_data(books_data)

    issue_data[Transaction.Transaction_id]=Transaction.model_dump(mode='json', exclude={'Transaction_id'})
    save_issue_data(issue_data)
    return JSONResponse(status_code=201,content={'message': 'Issue record created'})
@app.put('/update_Transaction/{Transaction_id}')
def update_Transaction_data(Transaction_id:str,update:Issue_Record_update):
    issue_data=load_issue_data()
    if Transaction_id not in issue_data:
        return JSONResponse(status_code=404,content="Transaction_id not found in database")
    issue_info=issue_data[Transaction_id]
    
    # Check if the book was already returned prior to this update
    was_returned = issue_info.get('returndate') is not None

    issue_update=update.model_dump(mode='json', exclude_unset=True)
    for key,value in issue_update.items():
        issue_info[key]=value
    issue_info['Transaction_id']=Transaction_id
    issue_obj=Issue_Record(**issue_info)

    # Increment book copies if the book is being returned in this update
    if update.returndate and not was_returned:
        books_data = load_books_data()
        if issue_obj.Book_ID in books_data:
            book_info = books_data[issue_obj.Book_ID]
            book_info['Book_id'] = issue_obj.Book_ID
            book_obj = Book(**book_info)
            book_obj.Total_copies += 1
            books_data[issue_obj.Book_ID] = book_obj.model_dump(mode='json', exclude={'Book_id'})
            save_books_data(books_data)

    issue_info=issue_obj.model_dump(mode='json', exclude={"Transaction_id"})
    issue_data[Transaction_id]=issue_info
    save_issue_data(issue_data)
    return JSONResponse(status_code=200,content={'message': 'Transaction updated successfully'})
@app.delete('/delete_Transaction/{Transaction_id}')
def delete_issue_data(Transaction_id:str):
    data=load_issue_data()
    if Transaction_id in data:
        del data[Transaction_id]
        save_issue_data(data)
        return JSONResponse(status_code=200,content={'message':'Data sucessfully deleted'})
    else:
        return JSONResponse(status_code=404,content={'message':'Transaction id not found in database'})