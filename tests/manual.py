import requests
import json

# Define the GraphQL endpoint
url = "http://localhost:8081/graphql"

# Define headers for the request
headers = {
    "Content-Type": "application/json"
}


# Define a function to send GraphQL queries/mutations
def send_graphql_query(query):
    response = requests.post(url, headers=headers, data=json.dumps({"query": query}))
    return response.json()


# Test the createExercise mutation
create_exercise_mutation = """
mutation {
  createExercise(name: "Test exc", muscleGroupIds: [1, 2], engagements: [0.8, 0.5]) {
    exercise {
      id
      name
    }
  }
}
"""

if __name__ == '__main__':
    print("Testing createExercise mutation...")
    result = send_graphql_query(create_exercise_mutation)
    print(json.dumps(result, indent=2))
