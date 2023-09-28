
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

#### gunicorn command
<pre><code># gunicorn -w 4 uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000</code></pre>

### Heroku
Create Procfile with below content:
<pre><code>web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}</code></pre>
Create app
<pre><code># heroku create [app-name]</code></pre>
Install postgresql add-on
<pre><code># heroku addons:create heroku-postgresql:mini</code></pre>
Set .env vars into heroku environment

Push app to heroku
<pre><code># git push heroku main</code></pre>
Create pgsql schema
<pre><code># heroku run "alembic upgrade head"</code></pre>
Restart app
<pre><code># heroku ps:restart</code></pre>
Check heroku logs
<pre><code># heroku logs -t</code></pre>

> **_NOTE:_** Update postman prod environment with new API URL every time the app is redeployed