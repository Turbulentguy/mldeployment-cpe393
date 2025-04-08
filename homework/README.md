## 🔹 Setup steps
1. Fork project from instructor's GitHub.
2. Run **train.py**.
3. Use command **docker build -t ml-model .** for building the Docker image.
4. Use command **docker run -p 9000:9000 ml-model** for running the docker container.
5. Request the API.

---

## 🔹 Sample API request and response
- **Exercise 1: Add Confidence Scores**
  
  **Task:**  
Update the `/predict` endpoint to return the prediction **and** the **confidence score** using `predict_proba()`.

  **Test API request command**

      curl -X POST http://localhost:9000/predict \
         -H "Content-Type: application/json" \
         -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

  **API request**

  **Input Example:**
  ```json
  {
    "features": [
      [5.1, 3.5, 1.4, 0.2],
    ]
  }
  ```

  **API respond**
  ```json
  {
    "prediction": 0,
    "confidence": 1
  }
  ```
##   
- **Exercise 2: Handle Multiple Inputs**

  **Task:**  
Allow the `/predict` endpoint to accept a list of inputs.

  **Test API request command**

      curl -X POST http://localhost:9000/predict \
         -H "Content-Type: application/json" \
         -d '{ "features": [ [5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3] ] }'

  **API request**

  **Input Example:**
  ```json
  {
    "features": [
      [5.1, 3.5, 1.4, 0.2],
      [6.2, 3.4, 5.4, 2.3]
    ]
  }
  ```

  **API respond**
  ```json
    {
      "predictions": [0, 2]
    }
    ``` 
##
- **Exercise 3: Add Input Validation**

  **Task:**  
  Ensure that:
  - The "features" key exists
  - Each input has exactly 4 float values
  - Invalid input returns a clear error message with HTTP 400
 
  **Test API request command**

      curl -X POST http://localhost:9000/predict \
          -H "Content-Type: application/json" \
          -d '{ "features": [ [5.1, 3.5, 1.4], [6.2, 3.4, 5.4, 2.3] ] }'

  **API request**

  **Input Example:**
   ```json
  {
    "features": [
      [5.1, 3.5, 1.4],
      [6.2, 3.4, 5.4, 2.3]
    ]
  }
  ```

  **API respond**
   ```json
    {
      "error":"Each input must have exactly 4 features"
    }
    ``` 
      172.17.0.1 - - [08/Apr/2025 04:41:30] "POST /predict HTTP/1.1" 400 -
  
##
- **Exercise 4: Add Health Check Endpoint**

  **Task:**  
Add an endpoint `/health` that returns a simple JSON indicating the API is live:

  **Test API request command**
  
      curl http://localhost:9000/health

  **API request**
  
      GET /health

  **API respond**
    ```json
    {
      "status": "ok"
    }
    ``` 
##
- **Exercise 5: Dockerize Your Own Model**
  
  **Task:**  
Train a new model on a provided housing dataset and deploy it using the same Docker structure. The task is to build a regression model to predict the housing price.

  - Linear Regression model fitting inside **train.py**.
  - In this assignment, I'm using feature columns by choosing **area** column, **bedrooms** column, and **bathrooms** column. For prediction the house price.

        housing = pd.read_csv("Housing.csv")
        
        feature = housing[['area', 'bedrooms', 'bathrooms']]
        target = housing['price']
        
        linear = LinearRegression()
        linear.fit(feature, target)
        
        with open('app/linear_model.pkl', 'wb') as f:
            pickle.dump(linear, f)
    
   - Open the model inside **app.py**,

         with open("linear_model.pkl", "rb") as f:
              linear_model = pickle.load(f)
     
   - Create the prediction.
     
          @app.route("/predict_price", methods=["POST"])
          def predict_price():
              data = request.get_json()
              try:
                  features = data["features"]
                  predictions = linear_model.predict(features)
                  return jsonify({"predictions": predictions.tolist()})
              except Exception as e:
                  return jsonify({"error": str(e)}), 400
     
   **Test API request command**

      curl -X POST http://localhost:9000/predict_price \
          -H "Content-Type: application/json" \
          -d '{"features": [[1200, 3, 2]]}'
  
  **API request**

  **Input Example:**
  ```json
  {
    "features": [
      [1200, 3, 2],
    ]
  }
  ```

  **API respond**
    ```json
      {
        "predictions":[4273902.793559029]
      }
    ``` 
  
