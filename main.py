from re import L, U
from fastapi import FastAPI, HTTPException
from models import LoginCredentials, Suggestion, SuggestionPayload, TechRequest, TechReview, User, UserInfo
from random import randint
from time import time

app = FastAPI()

users: list[User] = [User(employeeId=101,firstName="Adam", lastName="Ranieri", username="AdamGator", password="pass123", role="Admin")]
suggestions: list[Suggestion] = []
tech_reviews: list[TechReview] = []


@app.patch("/login", response_model=UserInfo)
def login(credentials: LoginCredentials) -> UserInfo:
    user:User | None = next((u for u in users if u.username == credentials.username), None)

    if user is None:
        raise HTTPException(status_code=404, detail=f'no user with username of {credentials.username}')
    elif user.password != credentials.password:
        raise  HTTPException(status_code=400, detail=f"Incorrect Password for user {credentials.username}")

    return UserInfo(**user.dict())

@app.post("/users", response_model=User)
def add_user(user: User) -> User:
    user.employeeId = randint(100000,900000)
    users.append(user)
    return user



@app.put("/users/{employeeId}", response_model=User)
def update_user(employeeId: int, user: User) -> User:
    user.employeeId = employeeId

    for i, u in enumerate(users):
        
        if u.employeeId == user.employeeId:
            users[i] = user
            return user
    
    raise HTTPException(404,detail=f'No user found with id')



@app.get("/suggestions", response_model=list[Suggestion])
def all_suggestions() -> list[Suggestion]:
    return suggestions

@app.get("/suggestions/{suggestionId}", response_model=Suggestion)
def get_suggestion(suggestionId: int) -> Suggestion:
    suggestion: Suggestion | None = next((s for s in suggestions if s.suggestionId == suggestionId),None)

    if suggestion is None:
        raise HTTPException(status_code=404, detail=f"Sugestion {suggestionId} was not found")

    return suggestion

@app.post("/suggestions", response_model=Suggestion, status_code=201)
def add_suggestion(payload:SuggestionPayload) -> Suggestion:
    randId = randint(100000,900000)
    timestamp = int(time())
    suggestion: Suggestion = Suggestion(**payload.dict(), suggestionId=randId, createdAt=timestamp)
    suggestions.append(suggestion)
    return suggestion

@app.patch("/suggestions/{suggestionId}/upvote", response_model=Suggestion)
def upvote(suggestionId: int) -> Suggestion:
    suggestion: Suggestion | None = next((s for s in suggestions if s.suggestionId == suggestionId),None)

    if suggestion is None:
        raise HTTPException(status_code=404, detail=f"Sugestion {suggestionId} was not found")
    
    suggestion.upVotes += 1
    return suggestion

    
@app.patch("/suggestions/{suggestionId}/downvote", response_model=Suggestion)
def downvote(suggestionId: int):
    suggestion: Suggestion | None = next((s for s in suggestions if s.suggestionId == suggestionId),None)

    if suggestion is None:
        raise HTTPException(status_code=404, detail=f"Sugestion {suggestionId} was not found")
    
    suggestion.downVotes += 1
    return suggestion



@app.delete("/suggestions/{suggestionId}", status_code=204)
def delete_suggestion(suggestionId: int):
    try:
        suggestions.remove(get_suggestion(suggestionId))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"Sugestion {suggestionId} was not found")


@app.post("/techrequests")
def add_tech_request(tech_request: TechRequest) -> TechReview:
    randId = randint(100000,900000)
    timestamp = int(time())
    review: TechReview = TechReview(reviewId=randId,createdAt=timestamp,isClosed=False,requestor=tech_request.requestor, message=tech_request.message)
    tech_reviews.append(review)
    return review

@app.get("/techreviews", response_model=list[TechReview])
def all_tech_review() -> list[TechReview]:
    return tech_reviews

@app.patch("/techreviews/{reviewId}/close", response_model=TechReview)
def close_tech_review(reviewId: int) -> TechReview:

    for r in tech_reviews:

        if r.reviewId == reviewId:
            r.isClosed = True
            return r

    raise HTTPException(status_code=404, detail=f"Sugestion {reviewId} was not found")
 

@app.delete("/users/nuke")
def nuke_users():
    users.clear()

@app.delete("/suggestions/nuke")
def nuke_suggestions():
    suggestions.clear()

@app.delete("/techrequests/nuke")
def nuke_tech_reviews():
    tech_reviews.clear()