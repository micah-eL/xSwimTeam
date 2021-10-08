from flask import Flask, json, render_template, jsonify
from flask_restful import Resource, Api, reqparse, abort
import mysql.connector


# ==== Database connection setup ==== #

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="X_Swim_Team"
)

cursor = db.cursor()


# ==== Basic app and API setup ==== #

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")


# ==== Validation functions ==== #

def validateUserExists(position, uid):
    queryUserExists = "SELECT EXISTS(SELECT * FROM {} WHERE ID = {})"
    queryUserExists = queryUserExists.format(position, uid)
    cursor.execute(queryUserExists)
    userExists = cursor.fetchone()
    if not userExists[0]:
        abort(404, message="There is no user with the ID " + str(uid) + "!")

def validateIDNotInUse(position, uid):
    queryIDNotInUse = "SELECT EXISTS(SELECT * FROM {} WHERE ID = {})"
    queryIDNotInUse = queryIDNotInUse.format(position, uid)
    cursor.execute(queryIDNotInUse)
    idInUse = cursor.fetchone()
    if idInUse[0]:
        abort(409, message="There is already a user with the ID " + str(uid) + "!")


# ==== Argparse code for put and patch requests ==== #

# PUT Swimmer
swimmer_put_args = reqparse.RequestParser()
swimmer_put_args.add_argument("name", type=str, help="Name of new swimmer is required", required=True)
swimmer_put_args.add_argument("birthdate", type=str, help="Birthdate of new swimmer is required", required=True)
swimmer_put_args.add_argument("swimmer_group", type=str, help="Group of new swimmer is required", required=True)
swimmer_put_args.add_argument("main_event", type=str, help="Main event of new swimmer is required", required=True)

# PATCH Swimmer (assume birthdate will not be updated)
swimmer_patch_args = reqparse.RequestParser()
swimmer_patch_args.add_argument("name", type=str, help="Update name of swimmer")
swimmer_patch_args.add_argument("swimmer_group", type=str, help="Update group of swimmer")
swimmer_patch_args.add_argument("main_event", type=str, help="Update main event of swimmer")

# PUT Coach
coach_put_args = reqparse.RequestParser()
coach_put_args.add_argument("name", type=str, help="Name of new coach is required", required=True)
coach_put_args.add_argument("birthdate", type=str, help="Birthdate of new coach is required", required=True)
coach_put_args.add_argument("coach_group", type=str, help="Group of new coach is required", required=True)

# PATCH Coach (assume birthdate will not be updated)
coach_patch_args = reqparse.RequestParser()
coach_patch_args.add_argument("name", type=str, help="Update name of coach")
coach_patch_args.add_argument("coach_group", type=str, help="Update group of new coach")


# ==== Swimmer API ==== #

class Swimmers(Resource):
    def get(self, user_id):
        # Special GET request with user_id=0; list all IDs and associated swimmers
        if user_id == 0:
            querySwimmers = "SELECT ID, Name FROM Swimmers;"
            cursor.execute(querySwimmers)
            swimmers = cursor.fetchall()
            payload = []
            content = {}
            for swimmer in swimmers:
                content = {"ID": swimmer[0], "Name": swimmer[1]}
                payload.append(content)
                content = {}
            response = jsonify(payload)
            response.status_code = 200
            return response  
        
        validateUserExists("Swimmers", user_id)
        
        # Query swimmer data 
        querySwimmerData = "SELECT * FROM Swimmers WHERE ID = {};"
        querySwimmerData = querySwimmerData.format(user_id)
        cursor.execute(querySwimmerData)
        swimmerData = cursor.fetchone()
        
        # Calculate age from birthdate
        querySwimmerAge = "SELECT DATE_FORMAT(NOW(), '%Y') - DATE_FORMAT(Birthdate, '%Y') - (DATE_FORMAT(NOW(), '00-%m-%d') < DATE_FORMAT(Birthdate, '00-%m-%d')) AS Age FROM Swimmers WHERE ID = {};"
        querySwimmerAge = querySwimmerAge.format(user_id)
        cursor.execute(querySwimmerAge)
        swimmerAge = cursor.fetchone()
        
        content = {"ID": swimmerData[0], "Name": swimmerData[1], "Age": int(swimmerAge[0]), "SwimmerGroup": swimmerData[3], "MainEvent": swimmerData[4]}

        response = jsonify(content)
        response.status_code = 200
        return response  
    
    def put(self, user_id):
        validateIDNotInUse("Swimmers", user_id)
        
        args = swimmer_put_args.parse_args()
        name = args["name"]
        birthdate = args["birthdate"]
        swimmerGroup = args["swimmer_group"]
        mainEvent = args["main_event"]
        
        insertSwimmerQuery = "INSERT INTO Swimmers VALUES ({}, '{}', '{}', '{}', '{}');"
        insertSwimmerQuery = insertSwimmerQuery.format(user_id, name, birthdate, swimmerGroup, mainEvent)
        cursor.execute(insertSwimmerQuery)
        db.commit()

        querySwimmers = "SELECT ID, Name FROM Swimmers"
        cursor.execute(querySwimmers)
        swimmers = cursor.fetchall()
        payload = []
        content = {}
        for swimmer in swimmers:
            content = {"ID": swimmer[0], "Name": swimmer[1]}
            payload.append(content)
            content = {}
        response = jsonify(payload)
        response.status_code = 201
        return response 
    
    def patch(self, user_id):
        validateUserExists("Swimmers", user_id)

        args = swimmer_patch_args.parse_args()
        if args["name"]:
            newName = args["name"]
            updateSwimmerQuery = "UPDATE Swimmers SET Name = '{}' WHERE ID = {};"
            updateSwimmerQuery = updateSwimmerQuery.format(newName, user_id)
            cursor.execute(updateSwimmerQuery)
            db.commit()
        if args["swimmer_group"]:
            newSwimmerGroup = args["swimmer_group"]
            updateSwimmerQuery = "UPDATE Swimmers SET SwimmerGroup = '{}' WHERE ID = {};"
            updateSwimmerQuery = updateSwimmerQuery.format(newSwimmerGroup, user_id)
            cursor.execute(updateSwimmerQuery)
            db.commit()
        if args["main_event"]:
            newMainEvent = args["main_event"]
            updateSwimmerQuery = "UPDATE Swimmers SET MainEvent = '{}' WHERE ID = {};"
            updateSwimmerQuery = updateSwimmerQuery.format(newMainEvent, user_id)
            cursor.execute(updateSwimmerQuery)
            db.commit()

        # Query updated swimmer data 
        querySwimmerData = "SELECT * FROM Swimmers WHERE ID = {};"
        querySwimmerData = querySwimmerData.format(user_id)
        cursor.execute(querySwimmerData)
        swimmerData = cursor.fetchone()
        
        # Calculate age from birthdate
        querySwimmerAge = "SELECT DATE_FORMAT(NOW(), '%Y') - DATE_FORMAT(Birthdate, '%Y') - (DATE_FORMAT(NOW(), '00-%m-%d') < DATE_FORMAT(Birthdate, '00-%m-%d')) AS Age FROM Swimmers WHERE ID = {};"
        querySwimmerAge = querySwimmerAge.format(user_id)
        cursor.execute(querySwimmerAge)
        swimmerAge = cursor.fetchone()
        
        content = {"ID": swimmerData[0], "Name": swimmerData[1], "Age": int(swimmerAge[0]), "SwimmerGroup": swimmerData[3], "MainEvent": swimmerData[4]}

        response = jsonify(content)
        response.status_code = 202
        return response 
    
    def delete(self, user_id):
        validateUserExists("Swimmers", user_id)

        deleteSwimmerData = "DELETE FROM Swimmers WHERE ID = {};"
        deleteSwimmerData = deleteSwimmerData.format(user_id)
        cursor.execute(deleteSwimmerData)
        db.commit()

        return '', 204

api.add_resource(Swimmers, '/swimmer/<int:user_id>')


# ==== Coach API ==== #

class Coaches(Resource):
    def get(self, user_id):
        # Special GET request with user_id=0; list all IDs and associated coaches
        if user_id == 0:
            queryCoaches = "SELECT ID, Name FROM Coaches;"
            cursor.execute(queryCoaches)
            coaches = cursor.fetchall()
            payload = []
            content = {}
            for coach in coaches:
                content = {"ID": coach[0], "Name": coach[1]}
                payload.append(content)
                content = {}
            return jsonify(payload)
        
        validateUserExists("Coaches", user_id)
        
        # Query coach data (note: we don't care about a coach's age)
        queryCoachData = "SELECT * FROM Coaches WHERE ID = {};"
        queryCoachData = queryCoachData.format(user_id)
        cursor.execute(queryCoachData)
        coachData = cursor.fetchone()
        
        content = {"ID": coachData[0], "Name": coachData[1], "CoachGroup": coachData[3]}
        
        response = jsonify(content)
        response.status_code = 200
        return response  
    
    def put(self, user_id):
        validateIDNotInUse("Coaches", user_id)
        
        args = coach_put_args.parse_args()
        name = args["name"]
        birthdate = args["birthdate"]
        coachGroup = args["coach_group"]
        
        insertCoachQuery = "INSERT INTO Coaches VALUES ({}, '{}', '{}', '{}');"
        insertCoachQuery = insertCoachQuery.format(user_id, name, birthdate, coachGroup)
        cursor.execute(insertCoachQuery)
        db.commit()

        queryCoaches = "SELECT ID, Name FROM Coaches"
        cursor.execute(queryCoaches)
        coaches = cursor.fetchall()
        payload = []
        content = {}
        for coach in coaches:
            content = {"ID": coach[0], "Name": coach[1]}
            payload.append(content)
            content = {}
        response = jsonify(payload)
        response.status_code = 201
        return response 
    
    def patch(self, user_id):
        validateUserExists("Coaches", user_id)

        args = coach_patch_args.parse_args()
        if args["name"]:
            newName = args["name"]
            updateCoachQuery = "UPDATE Coaches SET Name = '{}' WHERE ID = {};"
            updateCoachQuery = updateCoachQuery.format(newName, user_id)
            cursor.execute(updateCoachQuery)
            db.commit()
        if args["coach_group"]:
            newCoachGroup = args["coach_group"]
            updateCoachQuery = "UPDATE Coaches SET CoachGroup = '{}' WHERE ID = {};"
            updateCoachQuery = updateCoachQuery.format(newCoachGroup, user_id)
            cursor.execute(updateCoachQuery)
            db.commit()
        
        # Query updated coach data (note: we don't care about a coach's age)
        queryCoachData = "SELECT * FROM Coaches WHERE ID = {};"
        queryCoachData = queryCoachData.format(user_id)
        cursor.execute(queryCoachData)
        coachData = cursor.fetchone()
        
        content = {"ID": coachData[0], "Name": coachData[1], "CoachGroup": coachData[3]}
        
        response = jsonify(content)
        response.status_code = 200
        return response 

    def delete(self, user_id):
        validateUserExists("Coaches", user_id)

        deleteCoachData = "DELETE FROM Coaches WHERE ID = {};"
        deleteCoachData = deleteCoachData.format(user_id)
        cursor.execute(deleteCoachData)
        db.commit()

        return '', 204

api.add_resource(Coaches, '/coach/<int:user_id>')


# ==== Run app ==== #

if __name__ == "__main__":
    app.run(host="0.0.0.0")