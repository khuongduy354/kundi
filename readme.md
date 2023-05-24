# Stack choosing
Nodejs has non blocking model, while Flask has bloking one 
Js ecosystem sucks   

Nodejs 
  + realtime socket apps   
Flask  
  + fast to setup / build 
FastAPI 
  + even faster than flask 
  + satisfying 

Django 
  + well organized  
  + Battery included 
  - fixed paradigm  

# Requirements 
- Auth  
- Parse quizlet format 
- Database (decks and cards) 
- Revision system for users  

# Learned 
- parsing strings: 
https://pythonspeed.com/articles/faster-text-processing/ 
python easier but rust faster 
https://www.reddit.com/r/rust/comments/dto1ew/rust_vs_other_for_text_processing/
https://stackoverflow.com/questions/76257409/rust-regex-performance-in-comparison-with-python
https://stackoverflow.com/questions/41390244/rust-slower-than-python-at-parsing-files 

- dependency injection  
https://fastapi.tiangolo.com/tutorial/dependencies/#import-depends  
python Depends accepts a callable
 
- Auth   
https://fastapi.tiangolo.com/tutorial/security/first-steps/ 
when use Depends OAuth in request -> FastAPI handle OAuth automatically 

- Middlewares and D.I
Dependency can has its own dependencies -> chain pretty much like Middlewares
https://stackoverflow.com/questions/66632841/fastapi-dependency-vs-middleware#:~:text=Dependency%3A%20you%20use%20it%20to,the%20request%20to%20your%20logic. 
-> few similar use cases
-> use D.I if handle request before route handler 
-> middlewares apply to all endpoints, which is VERY INCONVENIENT

- package
never runs a nested module, cuz weird behaviors :) py tests/test_db.py for example

- PIP SUCKS 
firebase-admin take hours to install, 
but after i run pip3 install --upgrade pip
it install like instantly

- Firebase docs is all over the place
https://firebase.google.com/docs/auth/web/password-auth
<!-- -> this for example, it returns a user, but idk what that user Object contains :) -->
<!-- -> dont know whether that has a token for me to verify in my FastAPI --> 
login firebase -> return a user object has a token -> send that token to FastAPI to auth 

- Firestore
document -> collection -> document 

# Design decisions 
Review sys: https://en.wikipedia.org/wiki/Leitner_system, overkill :) 
-> use a 5 box, simpler method 
5 box: 10m, 1day, 3d, 5d, 7d  
correct -> move right   
wrong -> move left  
wrong thrice -> return box1 

Firebase because sets, cards are simple  


