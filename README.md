# fast_api_intro
An intro to fastapi making a basic CRUD app for a users database

## Steps
### set up the virtual environment
in the root folder run the following script in the terminal to make a virtual environment

```
python3 -m venv venv
```

this will create a venv folder in your root folder. To access the virtual environment on a mac run the script:

```
source venv/bin/activate
```

once inside the virtual environment you can download the fastapi packages with the script:

```
pip install "fastapi[all]"
```

this will download all the packages you'll need for your project

### create gitignore file
go to toptal and get a template for python. fastapi was not there at the time of this repo

### start the server
create a new folder called app and put the main.py file inside. create a __init__.py file. to start the server type the script 

```commandline
uvicorn app.main:app --reload
```

### creating api routes
in the main.py file you import fastapi and then create a demo route by typing this:

```
from fastapi import Fastapi

app = Fastapi()

@app.get("/")
async def root:
  return {"message":"Hello World"}
```

the route uses the decorator for the type of route method and the path. the function will enable you to provide logic to perform the 
activity for that route. this is the same for all route methods and paths. for the get, post, put and delete methods you might need to use a parameter
in the path. you can do that using the {parameter} syntax then using the same name as a parameter for the function.

```
@app.get("/post/{post_id}")
async def get_post(post_id: int):
  #logic to get data from db
  return db data
  
  
@app.post("/post/create")
async def create_post(post: Post):
  # save data to the db
  return post that was saved
```

if you want to convert the payload data to a python dictionary then just do post.dict() and then it will be that data type in your function.

### set up schema or modal for the db and structure of data
using pydantic you can set up the schema, modal with the types. you can import this package then make the schema

```
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
```

optional fields can be done making a default value as shown with the boolean value. this can be for any other data type as well. the other way to do 
this is to use the Optional package from typing.

### making more robust api endpoints
now that the schema is made then you can make more robust api endpoints. you can make them based on the format below

```commandline
import any packages

@app.get("/posts")
async def get_posts():
    return {"detail": my_posts}


@app.get("/posts/{post_id}")
async def get_post(post_id: UUID):
    payload = find_post(post_id)
    if payload is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    else:
        return {"detail": payload}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = uuid4()
    my_posts.append(post_dict)
    return {"detail": post_dict}


@app.put("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post: Post, post_id: UUID):
    response = None
    for item in my_posts:
        if item.id == post_id:
            item.title = post.title
            item.content = post.content
            item.rating = post.rating
            item.published = post.published
            response = item
            break

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    else:
        return {"detail": response}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: UUID):
    payload = find_post(post_id)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    else:
        my_posts.remove(payload)
        return {"detail": f"item with id {post_id} has been removed"}


def find_post(post_id):
    payload = None
    for item in my_posts:
        if post_id == item.id:
            payload = item
            break
    return payload
```

you can make default status codes in the decorator. you can create helper functions to help with searching for the post. you can have
html exceptions to be raised when the desired activity does not happen.


### setup of psycopg2 for postgres database interaction
psycopg2 is a way for us to interact with the postgres database using SQL. In order to set this up you will need to first create
a .env file to store all the settings info that should not be exposed. go to this site to set up your environment 
variables: <a href="https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv">setup</a>. then for each 
of the crud activities along with the setup of the database, tables, etc you can use the instructions here: 
<a href="https://www.postgresqltutorial.com/postgresql-python/">Python Postgres setup</a>. This is useful for smaller scale 
projects where the work doesn't get as involved.

### setup of orm sqlalchemy 
<p>
an object relational manager is a way to take sql out of use. you talk to the orm and the orm does the rest in terms of interacting 
with the database. it uses object notation and other python features to make things easier. an orm being used more at the time 
of this repo is sqlalchemy. The setup can be found here: <a href="https://fastapi.tiangolo.com/advanced/async-sql-databases/">setup link</a>
</p>

<p>make sure to delete connect_args={"check_same_thread": False} from the engine if using a db other that sqlite and install the 
psycopg2 package.
</p>

### folder structure
<p>
the setup of the database will go into the database.py file. the endpoints will go in the main.py file. the models that 
sqlalchemy uses to connect to the database will go in the models.py file. the schema or shape of the data will go in the 
schema.py file. any logic you want to put into another file for the endpoints will go in the crud.py file.
</p>

<p>
If you don't want to use the crud file and want to use routers instead then create a subfolder named routers. Inside the 
routers folder add a file for each category of api endpoint. In each file you will need to import the necessary packages 
and also import the APIRouter package from fastapi. 
</p>

<p>
to complete the routers setup you will need to add the following in the main.py file:

```commandline
# routers
app.include_router(blog.router)
app.include_router(user.router)
```

then in the respective file in the routers folder you will need to add the following:

```commandline
router = APIRouter()

or 

# this is if you want to add a prefix if the route has repeated subpaths
router = APIRouter(
    prefix="/users",
    tags=['Users'] # this will organize the swaggerUI in docs for better readability
)
```

after that change the decorator so that it says router instead of app
</p>

### authentication
the fastapi has a good documentation for authentication <a href="https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=oau">found here</a>

### using postman
when using postman it can be very helpful to set up environment variables. this is especially helpful when you are authenticating 
users and have tokens to verify a user in other paths. go the side tab where it says environment variables and create a new one. 
then in the main area type in the name of the variables that you want. in the case of the token then make a name for that variable. 
you can type in the initial and current value the first time. to have this be dynamic then go to the login or register path. in 
the test subtab you will need to set the variable based on the response object. if you have done thing properly then the response 
for the login path should include a token. you can type in the following code to automatically update it for each login or register:

```commandline
var jsonData = pm.response.json()
pm.environment.set("token", jsonData.data[0].token);
```

the shape of the response will depend on your schema. you will need to make sure that the json object is pointing to the correct 
property and value within your response object. 

### relational database relations
in order to create a relationship between tables in your relational database you will need to adjust the tables accordingly. the 
sqlalchemy has documentation on how to do it <a href="https://docs.sqlalchemy.org/en/14/orm/relationships.html">here</a>. you 
can select the type of relationship you want and read the documentation. for a glimpse of how it would look in this project it 
would look like this:

```commandline
class Blog(Base):
    __tablename__ = "blogs"
    blog_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
```

the user_id column in the blogs table will connect to the users table. it is a one to many relation because one user can have 
many blogs. you can also add another line to each table that has a relationship in order to make it bidirectional. the response 
was tricky as i was not able to get the schema to work properly and had to make a helper function to choose what shape the 
response data had.


### search parameters
you can add query parameters to the path which can help in querying the database. in order to do this you just need to 
add each parameter to the path function. you can add defaults in case the search parameter is not mentioned in the url. then
in the path function you can use those parameters in the query to the database.

```commandline
@router.get("", status_code=status.HTTP_200_OK)
async def get_blogs(
        db: Session = Depends(get_db),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
        # current_user: user_schema.UserCreate = Depends(authentication.get_current_user)
):
    payload = db.query(models.Blog)\
        .filter(models.Blog.title.contains(search))\
        .order_by(models.Blog.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
```

the query can be chained for all the different parameters that you want to use. if the parameter is a string and has a space 
or whitespace separating the string then you can use <code>%20</code> as a space that will be recognized accordingly.

### environment variables
if you want to use environment variables using the fastapi tools then <a href="https://fastapi.tiangolo.com/advanced/settings/">read here</a> 
to see how that can be set up.

### sql join queries and translating that to sqlalchemy
see the utils file named queries to see the sql queries that use raw sql. these queries look to join different tables in 
order to retrieve data useful to the client. the main query that joins tables is the query that joins the blogs and votes 
to find how many likes or votes each blog has. the sqlalchemy equivalent can be found in the blogs and votes routers. you 
can also check out the documentation with sqlalchemy to learn more about joining tables in this syntax.

### alembic 
<p>
use a tool called alembic to make changes to the database. it can automatically pull database models from sqlalchemy and generate 
the proper tables. to use it you will need to install alembic and go through the documentation <a href="https://alembic.sqlalchemy.org/en/latest/">here</a>.
</p>
<p>
first do a pip install of alembic by running <code>pip install alembic</code>. make sure you are in the root folder before doing this 
so that it is outside the app folder. then initialize alembic by writing this <code>alembic init alembic</code> in the terminal. the last 
word in this command is the folder name so that can be whatever you want. go to the .env file in the alembic folder and import 
Base from the database file like this <code>from app.models import Base</code>. go to the metadata target and do this: 
<code>target_metadata = Base.metadata</code> then go to the alembic.ini file that is in the root directory. you will need to find 
the url for the database connection. enter the required data in <code>sqlalchemy.url = postgresql://user:pass@localhost/dbname</code>. this 
is the same as the other database connection using the environment variables. if you don't want to do this in the ini file 
then go back to the .env file and underneath the config variable type with your credentials

```commandline
config.set_main_option("sqlalchemy.url", 'postgresql://user:pass@localhost/dbname')
```

then you can use the environment variables already made to insert into this settings for the config. you can use the pydantic settings 
process or the dotenv process. this is similar to when we set up the database config.
</p>

### alembic functionality
you can access the commands from alembic by going in the terminal and typing alembic --help. 

#### revision
to revise any model you can use the revision command and you can use a flag to insert a message that will connect to the revision. 
it would look like this

```commandline
alembic revision -m "create blogs table"
```

after this is successful then you can look at the subfolder called versions to see the migrations. you can go the the file 
that was just created to put in the code. this is done in the upgrade function. the documentation for this can be found in the
 previous link.

#### commands
to create the first migration you can use the alembic revision -m "message here" then the file will show in the versions folder. 
go to the file and make the necessary adjustments in upgrade and downgrade. go back to the terminal and we can either do one 
of two commands. the first is <code>alembic upgrade <revision number></code> or you can type <code>alembic upgrade head</code>. if you 
need to downgrade you can do it one of two ways. first you can type <code>alembic downgrade <revision number></code> or you 
can type <code>alembic downgrade -1</code> the -1 can be replaced but it represents how many revisions backwards do you want 
to go. -1 means you will go back one revision. each subsequent number would be an additional downgrade further back. to see which 
revision you are on you can see the current revision <code>alembic current</code> or if you want to see the entire history then 
you can type <code>alembic history</code>

#### alembic guide for writing upgrades/downgrades
the documentation for how to write the upgrades and downgrades in the versions or migration it can be found 
<a href="https://alembic.sqlalchemy.org/en/latest/api/ddl.html">here</a>

 

