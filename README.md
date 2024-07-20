# Second Life Recycling
Few sites allow builders to list recycled items for sale at different facilities. These platforms are designed to connect sellers of recycled construction materials with potential buyers, fostering a marketplace for sustainable building practices.

# Project Setup Instructions for first time installation
Follow these steps to set up and run the project:

1. Install the required packages using Pipenv:
    ```sh
    pipenv install
    ```

2. Activate the virtual environment:
    ```sh
    pipenv shell
    ```

3. Create the database migrations:
    ```sh
    python manage.py makemigrations
    ```

4. Apply the migrations to the database:
    ```sh
    python manage.py migrate
    ```

5. Start the development server:
    ```sh
    python manage.py runserver
    ```


## HOW TO START THE SERVER FOR FRONT-END
1. Open Terminal:
    ```sh
    pipenv shell
    ```

2. Start Python Interpreter:
    ```sh
    CTRL + Shift + P and click Python: Select Interpreter
    ```    

3. Select the correct Python Interpreter:
    ```sh
    Python (version)(`file_name_server_randomString`:Pipenv) ~.\virtualenvs\sec...
    ```  

4. Open Terminal to Start Server:
    ```sh
    python manage.py runserver
    ```       

5. Verify server is running by clicking to open web page to see data:
    ```sh
    Starting development server at http://127.0.0.1:8000/
    ```
  ![Screenshot](assets/api_root.png "Screenshot 2024-07-15 192448") 


## TO LOAD FIXTURES 
1. Create the database migrations:
    ```sh
    python manage.py makemigrations
    ```

2. Apply the migrations to the database:
    ```sh
    python manage.py migrate
    ```

3. Load each fixtures into the database:
    ```sh
    python manage.py loaddata fixture_file_name.json
    ```

4. Verify the fixtures were loaded correctly:
    ``` sh
    CTRL + SHIFT + P to open SQllite: 
    Database and verify the data is in the explorer 
    click file_name_item_name
    click play to the right of item name
    ```

## HOW TO CALL ENDPOINTS IN REACT
1. Ensure that your .env file has the following items in it:
    ```sh
    NEXT_PUBLIC_FIREBASE_API_KEY=""
    NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=""
    NEXT_PUBLIC_DATABASE_URL="http://127.0.0.1:8000/"
    ```

2. At the top of your API page:
    ```sh
    const endpoint = process.env.NEXT_PUBLIC_DATABASE_URL;
    ```

3. Promise fetch call should look like this:
    ```sh
    fetch(`${endpoint}recyclable_items`, {
    ```        

# TESTING API'S IN POSTMAN
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/29856352-e6ef773b-5bc3-45ff-8c87-3095b75d3bd9?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D29856352-e6ef773b-5bc3-45ff-8c87-3095b75d3bd9%26entityType%3Dcollection%26workspaceId%3D55dfd999-82a1-4a30-8d1b-1231bbd0adb1)

# Tech / Framework Used

- [Design Doc](https://www.figma.com/board/kgmZK81UbmjyKW6mE7Ls4G/Second-Life-Recycling?node-id=0-1&t=5URe1Z2E3YmS0s5p-0)
- [Data Flow Chart](https://dbdiagram.io/d/Copy-of-recycle_app_2_v-669082739939893daeb7a84b)
- [Deployed Project](URL)
- [Issue Tickets](https://github.com/frankcampos/second-life-recycling-server/issues)
- [API Documentation](https://documenter.getpostman.com/view/29856352/2sA3kUGhS4)


### BUIT WITH 
- React
- Django
- SQL
- Firebase

# Credits

- Daun Kim - Full CRUD for Shopping Cart 
- Frank Campos - User login and Full CRUD 
- Jesse Ramirez - Full CRUD for items 
