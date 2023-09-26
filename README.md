
#### Project step by step course 
[Python API Development - Comprehensive Course for Begginners](https://www.youtube.com/watch?v=0sOvCWFmrtA)

#### API docs URL
http://localhost:8000/docs

#### Uvicorn
https://www.uvicorn.org/

#### pydantic
https://docs.pydantic.dev/latest/

#### FastAPI
https://fastapi.tiangolo.com/es/

#### SQLAlchemy
https://docs.sqlalchemy.org/en/20/

#### API server run:
<pre><code># uvicorn app.main:app --reload</code></pre>

#### C.R.U.D.

 - **C** reate     
<pre>     POST        /post       @app.post("/post")</pre>
 - **R** ead
<pre>     GET         /post/:id   @app.get("/post/{id}")
     GET         /post       @app.get("/post")</pre>
- **U** pdate     
<pre>     PUT/PATCH   /post/:id   @app.put("/post/{id}")</pre>
- **D** elete
<pre>     DELETE      /post/:id   @app.delete("/post/{id}")</pre>


#### Alembic Library
[Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/index.html)

##### Alembic Setup
<pre><code># pip install alembic
# alembic init [alembic_dir]</code></pre>
