# Recipe Assistant README
**Project**: Recipe Assistant<br>
 **Contributers**: Raymond Gu<br>

## Introduction
This project is a recipe assistant API built to explore how GraphQL can be used as a structured interface on top of LLM-powered reasoning. The API allows clients to query exactly the recipe information they need, while using an LLM to perform higher-level tasks such as summarization and recommendation.<br>

The backend is implemented using GraphQL, LangChain, and Phi-3 via Microsoft Azure OpenAI, with a small SQLite recipe dataset used as a controlled knowledge source. Rather than returning raw database rows, GraphQL resolvers orchestrate database retrieval and LLM calls, demonstrating how typed schemas can constrain and guide LLM inputs.<br>

The service is deployed using Azure Web App Service and is designed to scale to larger databases and more complex reasoning pipelines.

## How To Set Up Project (Local)
There is a `requirements.txt` file that contains all the dependencies needed to run this project. To create a virtual environment for this project, you can run the following code shown below:

```
$ python3 -m venv Virtual_Environment
$ .\Virtual_Environment\Scripts\Activate
$ pip install -r requirements.txt
```

### | Database Setup
The dataset used for this project was manually created using a few recipes from `simplyrecipes.com`. The JSON file for this dataset can be found in the `Recipes.JSON` file in the `Data_Files` folder. The code used to create the SQLite database is in `setup.py` in the `Database` folder. This code can be run using the following command:

```
$ python .\Database\setup.py
```

### | LLM Setup
For this project, I used `Phi-4-mini-instruct` via Microsoft Azure OpenAI to generate summaries and recommendations for each recipe. The main reason why I chose to use this model was because its an inexpensive model is allowed in student Azure subscription regions. To run this project, you'll need to obtain an API key.<br>

1. Navigate to the search bar and search for "Foundry resource".
2. Create a Foundry resource and go to the "Foundry portal".
3. Navigate to "Model catalog" and search for "Phi-4-mini-instruct".
4. Go to "Existing Deployments” and click “Create a Deployment”.
    - For `deployment_name`, make sure to name it “Recipe_Assistant”.
4. After it's deployed, copy the key and put it in the `.env` file.

### | Running API Locally
To run the API locally on your own computer, you can use the following command:

```
$ uvicorn main:app --reload
```

This should start the API and give you a link that looks like `http://127.0.0.1:8000`. To interact with the API, add `/graphql` to the end of the link.

## How To Set Up Project (Azure)
There is an `Azure_Deployment.zip` file that contains everything needed and can be manually deployed to Microsoft Azure App Service. The ZIP file contains the following folder and files:

- 📂 Database
  - 🛢️Recipes.db
  - ⚙️ setup.py
- 📂 Domain
  - ⚙️ ingredient.py
  - ⚙️ nutrition.py
  - ⚙️ recipe.py
  - ⚙️ step.py
- 📂 GraphQL
  - ⚙️ query.py
  - ⚙️ schema.py
  - 📂 Strawberry_Types
    - ⚙️ ingredient_type.py
    - ⚙️ nutrition_type.py
    - ⚙️ recipe_type.py
    - ⚙️ step_type.py
- 📂 Infrastructure
  - ⚙️ recipe_service.py
  - ⚙️ strawberry_mappings.py
  - 📂 Utils
    - ⚙️ database_utils.py
    - ⚙️ llm_utils.py
- ⚙️ main.py
- 📄 requirements.txt

**Note**: When creating the `requirements.txt` file, I ran into many issues because I generated it on Windows. To avoid any issues when deploying to Azure, make sure this file uses `UTF-8` text encodings and `LF` line endings.

### | Creating Web App Service
First, we need to create the web app service.
1. Navigate to the search bar and search for "App Services".
2. Click on the "Create" button and select the "Web App" option.
3. Fill in the fields (the relevant ones are shown below):
    - Publish = Code
    - Runtime Stack = Python 3.11
    - Operating System = Linux
4. Review and create the web app.

Once the web app service is successfully deployed, we need to setup a few settings before manually deploying the ZIP file. In the "Environment variables" section, create 5 new variables.

1. We need to ensure that an environment for the web app service is built using Oryx during deployment (this does NOT happen by default).
    - `SCM_DO_BUILD_DURING_DEPLOYMENT` = true
    - `WEBSITE_RUN_FROM_PACKAGE` = 0
2. Since the ZIP file does not contain the `.env` file, we need to manually define them in the environment. Copy all the variables from the `.env` file.
    - `KEY`
    - `ENDPOINT`
    - `DEPLOYMENT_NAME`


After that, we can manually deploy the ZIP file and run the app.
1. Navigate to the "Deployment" section and go to "Deployment Center".
2. For the "Source", choose "Publish files (new)".
3. Select the `Azure_Deployment.zip` file and click "Save".
4. Navigate to the "Settings" section and go to "Configuration".
5. Select the "Stack settings" tab and enter the "Startup command" shown below:
    - python -m uvicorn main:app --host 0.0.0.0 --port 8000
6. After that, click "Apply" and the API is all set up.

## Recipes Dataset
As stated previously, this project uses a small collection of recipes taken from a cooking website. A table of recipe features and descriptions is shown below.<br>

<table cellpadding="8" border="1">
  <tr>
    <th>Features</th>
    <th>Subfeatures</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>name</td>
    <td>---</td>
    <td>The name of the recipe.</td>
  </tr>
  <tr>
    <td>ingredients</td>
    <td>name, quantity, unit</td>
    <td>The ingredients needed for the recipe. Each ingredient has a name, quantity (optional), and unit (optional).</td>
  </tr>
  <tr>
    <td>steps</td>
    <td>---</td>
    <td>This is a dictionary where the key is the step number and the value is the instruction.</td>
  </tr>
  <tr>
    <td>nutrition_facts</td>
    <td>calories, fat, carbs, protein</td>
    <td>The nutrition facts for the recipe. This includes calories, fat, carbs, and protein (in grams).</td>
  </tr>

</table><br>

When setting up the SQLite recipe database, I decided to use 3 different tables (recipes, ingredients, and steps). An entity relationship diagram for the database is shown below.

<br><img src="Images/Entity Relationship Diagram.png" width=800><br>

## Recipe Assistant
As stated previously, this project is a recipe assistant API built to explore how GraphQL can be used as a structured interface on top of LLM-powered reasoning.

### | Domain
The domain of this project is recipe assistance. Since recipes naturally combine deterministic information (ingredients, instructions) with higher-level tasks such as summarization and recommendations, we need to balance structured data retrieval with open-ended reasoning.<br>

Rather than treating the LLM as a replacement for the database, the system treats it as a reasoning layer on top of structured data. GraphQL queries retrieve or filter relevant recipe data first, which is then selectively passed into the LLM to perform tasks such as summarization or recommendation.

### | GraphQL Schema Design
The GraphQL schema is designed to act as a typed contract between the client, the database, and the LLM. Rather than exposing raw database tables, the schema defines domain-level types that represent how recipe information is queried and reasoned about.<br>

At the core of the schema is the `Recipe` type, which models structured recipe data such as:
  - Names
  - Ingredients
  - Nutrition Facts
  - Steps
  
This allows clients to request only the fields they need, while also giving resolvers a predictable structure to feed into downstream LLM prompts.

The `Query` type exposes high-level operations such as retrieving recipes or requesting recommendations. These queries can combine SQLite retrieval with LLM reasoning (via LangChain and Phi-3) which keeps the schema clean while allowing complex logic behind the scenes.

### | Infrastructure
The API is deployed using `Azure Web App Service`, providing a managed and scalable environment suitable for production-style deployments. This allows the GraphQL server to be exposed as a persistent service rather than a local or notebook-based prototype.

LLM capabilities are provided via `Microsoft Azure OpenAI` and orchestrated using `LangChain`. LangChain is responsible for model interaction while GraphQL resolvers determine when and how the model is invoked. This keeps model usage explicit and controlled.

A lightweight `SQLite` database is used to simplify setup while still practicing real database access patterns. Although SQLite is used here, the architecture is designed to support swapping in a larger relational database without changing the GraphQL interface.

### | Methods
The API exposes three categories of GraphQL queries, each handled through dedicated resolvers that coordinate database access and LLM reasoning.

1. `Data Retrieval Queries`: These types of queries are capable of retrieving recipe information directly through the service layer. These queries involve no LLM calls and demonstrate traditional GraphQL-style data access.

2. `Summarization Queries`: These types of queries retrieve a specific recipe from the database and pass its structured fields into the LLM via LangChain to generate a concise summary.

3. `Evaluation Queries`: These types of queries follow a similar pattern, but task the LLM with rating the recipe rather than summarizing it. The resolver controls prompt structure and output formatting before returning a scalar response to the client.
